#include "ObjectFactory.h"

#include "CfdpHandler.h"
#include "OBSWConfig.h"
#include "bsp_hosted/fsfwconfig/objects/systemObjectList.h"
#include "commonConfig.h"
#include "example/core/GenericFactory.h"
#include "example/test/FsfwTestTask.h"
#include "example/utility/TmFunnel.h"
#include "fsfw/storagemanager/PoolManager.h"
#include "fsfw/tmtcservices/CommandingServiceBase.h"
#include "fsfw_hal/host/HostFilesystem.h"

#if OBSW_USE_TCP_SERVER == 0
#include <fsfw/osal/common/UdpTcPollingTask.h>
#include <fsfw/osal/common/UdpTmTcBridge.h>
#else
#include "fsfw/osal/common/TcpTmTcBridge.h"
#include "fsfw/osal/common/TcpTmTcServer.h"
#endif

void ObjectFactory::produce(void* args) {
  Factory::setStaticFrameworkObjectIds();
  StorageManagerIF* tcStore = nullptr;
  StorageManagerIF* tmStore = nullptr;
#if OBSW_ADD_CORE_COMPONENTS == 1
  {
    LocalPool::LocalPoolConfig poolCfg = {{16, 100}, {32, 50},   {64, 40},
                                          {128, 30}, {1024, 20}, {2048, 10}};
    tcStore = new PoolManager(objects::TC_STORE, poolCfg);
  }

  {
    LocalPool::LocalPoolConfig poolCfg = {{16, 100}, {32, 50},   {64, 40},
                                          {128, 30}, {1024, 20}, {2048, 10}};
    tmStore = new PoolManager(objects::TM_STORE, poolCfg);
  }

  {
    LocalPool::LocalPoolConfig poolCfg = {{16, 100}, {32, 50},   {64, 40},
                                          {128, 30}, {1024, 20}, {2048, 10}};
    new PoolManager(objects::IPC_STORE, poolCfg);
  }
  TmFunnel* funnel;
  ObjectFactory::produceGenericObjects(&funnel);
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
  auto* hostFs = new HostFilesystem();
  FsfwHandlerParams params(objects::CFDP_HANDLER, *hostFs, *funnel, *tcStore, *tmStore);
  cfdp::IndicationCfg indicationCfg;
  UnsignedByteField<uint16_t> apid(COMMON_APID);
  cfdp::EntityId localId(apid);
  cfdp::RemoteEntityCfg cfg;
  cfdp::OneRemoteConfigProvider remoteCfgProvider(cfg);
  // CfdpHandlerCfg cfg(localId, indicationCfg);
  // new CfdpHandler();
}
