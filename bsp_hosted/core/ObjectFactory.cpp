#include "ObjectFactory.h"

#include "OBSWConfig.h"
#include "bsp_hosted/fsfwconfig/objects/systemObjectList.h"
#include "common/definitions.h"
#include "commonConfig.h"
#include "example/core/GenericFactory.h"
#include "example/test/FsfwTestTask.h"
#include "example/utility/TmFunnel.h"
#include "fsfw/cfdp.h"
#include "fsfw/storagemanager/PoolManager.h"
#include "fsfw/tcdistribution/CcsdsDistributor.h"
#include "fsfw/tcdistribution/CcsdsDistributorIF.h"
#include "fsfw/tmtcservices/CommandingServiceBase.h"
#include "fsfw_hal/host/HostFilesystem.h"

#if OBSW_USE_TCP_SERVER == 0
#include <fsfw/osal/common/UdpTcPollingTask.h>
#include <fsfw/osal/common/UdpTmTcBridge.h>
#else
#include "fsfw/osal/common/TcpTmTcBridge.h"
#include "fsfw/osal/common/TcpTmTcServer.h"
#endif

class CfdpExampleUserHandler : public cfdp::UserBase {
 public:
  explicit CfdpExampleUserHandler(HasFileSystemIF& vfs) : cfdp::UserBase(vfs) {}

  void transactionIndication(const cfdp::TransactionId& id) override {}
  void eofSentIndication(const cfdp::TransactionId& id) override {}
  void transactionFinishedIndication(const cfdp::TransactionFinishedParams& params) override {
    sif::info << "File transaction finished for transaction with " << params.id << std::endl;
  }
  void metadataRecvdIndication(const cfdp::MetadataRecvdParams& params) override {
    sif::info << "Metadata received for transaction with " << params.id << std::endl;
  }
  void fileSegmentRecvdIndication(const cfdp::FileSegmentRecvdParams& params) override {}
  void reportIndication(const cfdp::TransactionId& id, cfdp::StatusReportIF& report) override {}
  void suspendedIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code) override {}
  void resumedIndication(const cfdp::TransactionId& id, size_t progress) override {}
  void faultIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code,
                       size_t progress) override {}
  void abandonedIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code,
                           size_t progress) override {}
  void eofRecvIndication(const cfdp::TransactionId& id) override {
    sif::info << "EOF PDU received for transaction with " << id << std::endl;
  }
};

class CfdpExampleFaultHandler : public cfdp::FaultHandlerBase {
 public:
  void noticeOfSuspensionCb(cfdp::TransactionId& id, cfdp::ConditionCode code) override {
    sif::warning << "Notice of suspension detected for transaction " << id
                 << " with condition code: " << cfdp::getConditionCodeString(code) << std::endl;
  }
  void noticeOfCancellationCb(cfdp::TransactionId& id, cfdp::ConditionCode code) override {
    sif::warning << "Notice of suspension detected for transaction " << id
                 << " with condition code: " << cfdp::getConditionCodeString(code) << std::endl;
  }
  void abandonCb(cfdp::TransactionId& id, cfdp::ConditionCode code) override {
    sif::warning << "Transaction " << id
                 << " was abandoned, condition code : " << cfdp::getConditionCodeString(code)
                 << std::endl;
  }
  void ignoreCb(cfdp::TransactionId& id, cfdp::ConditionCode code) override {
    sif::warning << "Fault ignored for transaction " << id
                 << ", condition code: " << cfdp::getConditionCodeString(code) << std::endl;
  }
};

void ObjectFactory::produce(void* args) {
  Factory::setStaticFrameworkObjectIds();
  StorageManagerIF* tcStore = nullptr;
  StorageManagerIF* tmStore = nullptr;
#if OBSW_ADD_CORE_COMPONENTS == 1
  {
    LocalPool::LocalPoolConfig poolCfg = {{100, 16}, {50, 32},   {40, 64},
                                          {30, 128}, {20, 1024}, {10, 2048}};
    tcStore = new PoolManager(objects::TC_STORE, poolCfg);
  }

  {
    LocalPool::LocalPoolConfig poolCfg = {{100, 16}, {50, 32},   {40, 64},
                                          {30, 128}, {20, 1024}, {10, 2048}};
    tmStore = new PoolManager(objects::TM_STORE, poolCfg);
  }

  {
    LocalPool::LocalPoolConfig poolCfg = {{100, 16}, {50, 32},   {40, 64},
                                          {30, 128}, {20, 1024}, {10, 2048}};
    new PoolManager(objects::IPC_STORE, poolCfg);
  }
  TmFunnel* funnel;
  CcsdsDistributor* ccsdsDistrib;
  ObjectFactory::produceGenericObjects(&funnel, &ccsdsDistrib, *tcStore);
  // TMTC Reception via TCP/IP socket
#if OBSW_USE_TCP_SERVER == 0
  auto tmtcBridge = new UdpTmTcBridge(objects::TCPIP_TMTC_BRIDGE, objects::CCSDS_DISTRIBUTOR);
  tmtcBridge->setMaxNumberOfPacketsStored(50);
  sif::info << "Opening UDP TMTC server on port " << tmtcBridge->getUdpPort() << std::endl;
  new UdpTcPollingTask(objects::TCPIP_TMTC_POLLING_TASK, objects::TCPIP_TMTC_BRIDGE);
#else
  auto tmtcBridge = new TcpTmTcBridge(objects::TCPIP_TMTC_BRIDGE, objects::CCSDS_DISTRIBUTOR);
  tmtcBridge->setMaxNumberOfPacketsStored(50);
  auto tmtcServer = new TcpTmTcServer(objects::TCPIP_TMTC_POLLING_TASK, objects::TCPIP_TMTC_BRIDGE);
  sif::info << "Opening TCP TMTC server on port " << tmtcServer->getTcpPort() << std::endl;
#endif

#endif /* OBSW_ADD_CORE_COMPONENTS == 1 */

  bool periodicEvent = false;
#if OBSW_TASK_PERIODIC_EVENT == 1
  periodicEvent = true;
#endif
  new FsfwTestTask(objects::TEST_TASK, periodicEvent);

#if OBSW_ADD_CFDP_COMPONENTS == 1
  auto* hostFs = new HostFilesystem();
  FsfwHandlerParams params(objects::CFDP_HANDLER, *hostFs, *funnel, *tcStore, *tmStore);
  cfdp::IndicationCfg indicationCfg;
  UnsignedByteField<uint16_t> apid(common::COMMON_CFDP_APID);
  cfdp::EntityId localId(apid);
  UnsignedByteField<uint16_t> remoteEntityId(common::COMMON_CFDP_CLIENT_ENTITY_ID);
  cfdp::EntityId remoteId(remoteEntityId);
  cfdp::RemoteEntityCfg remoteCfg(remoteId);
  remoteCfg.defaultChecksum = cfdp::ChecksumType::CRC_32;
  auto* remoteCfgProvider = new cfdp::OneRemoteConfigProvider(remoteCfg);
  auto* cfdpUserHandler = new CfdpExampleUserHandler(*hostFs);
  auto* cfdpFaultHandler = new CfdpExampleFaultHandler();
  cfdp::PacketInfoList<64> packetList;
  cfdp::LostSegmentsList<128> lostSegments;
  CfdpHandlerCfg cfg(localId, indicationCfg, *cfdpUserHandler, *cfdpFaultHandler, packetList,
                     lostSegments, *remoteCfgProvider);
  auto* cfdpHandler = new CfdpHandler(params, cfg);
  CcsdsDistributorIF::DestInfo info("CFDP Destination", common::COMMON_CFDP_APID,
                                    cfdpHandler->getRequestQueue(), true);
  ccsdsDistrib->registerApplication(info);
#endif
}
