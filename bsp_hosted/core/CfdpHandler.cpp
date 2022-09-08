#include "CfdpHandler.h"

#include "fsfw/cfdp/pdu/PduHeaderReader.h"
#include "fsfw/ipc/QueueFactory.h"
#include "fsfw/tmtcservices/TmTcMessage.h"

using namespace returnvalue;
using namespace cfdp;

CfdpHandler::CfdpHandler(const FsfwHandlerParams& fsfwParams, const CfdpHandlerCfg& cfdpCfg)
    : SystemObject(fsfwParams.objectId),
      UserBase(fsfwParams.vfs),
      destHandler(DestHandlerParams(cfdpCfg.cfg, *this, *this, cfdpCfg.packetInfoList,
                                    cfdpCfg.lostSegmentsList),
                  FsfwParams(fsfwParams.packetDest, nullptr, this, fsfwParams.tcStore,
                             fsfwParams.tmStore)) {
  // TODO: Make queue params configurable, or better yet, expect it to be passed externally
  msgQueue = QueueFactory::instance()->createMessageQueue();
  destHandler.setMsgQueue(*msgQueue);
}

[[nodiscard]] const char* CfdpHandler::getName() const { return "CFDP Handler"; }

[[nodiscard]] uint32_t CfdpHandler::getIdentifier() const {
  return destHandler.getDestHandlerParams().cfg.localId.getValue();
}

[[nodiscard]] MessageQueueId_t CfdpHandler::getRequestQueue() const { return msgQueue->getId(); }

ReturnValue_t CfdpHandler::initialize() {
  ReturnValue_t result = destHandler.initialize();
  if (result != OK) {
    return result;
  }
  tcStore = destHandler.getTcStore();
  tmStore = destHandler.getTmStore();

  return SystemObject::initialize();
}

ReturnValue_t CfdpHandler::performOperation(uint8_t operationCode) {
  // TODO: Receive TC packets and route them to source and dest handler, depending on which is
  //       correct or more appropriate
  ReturnValue_t status;
  ReturnValue_t result = OK;
  TmTcMessage tmtcMsg;
  for (status = msgQueue->receiveMessage(&tmtcMsg); status == returnvalue::OK;
       status = msgQueue->receiveMessage(&tmtcMsg)) {
    result = handleCfdpPacket(tmtcMsg);
    if (result != OK) {
      status = result;
    }
  }
  return status;
}

void CfdpHandler::transactionIndication(const cfdp::TransactionId& id) {}
void CfdpHandler::eofSentIndication(const cfdp::TransactionId& id) {}
void CfdpHandler::transactionFinishedIndication(const cfdp::TransactionFinishedParams& params) {}
void CfdpHandler::metadataRecvdIndication(const cfdp::MetadataRecvdParams& params) {}
void CfdpHandler::fileSegmentRecvdIndication(const cfdp::FileSegmentRecvdParams& params) {}
void CfdpHandler::reportIndication(const cfdp::TransactionId& id, cfdp::StatusReportIF& report) {}
void CfdpHandler::suspendedIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code) {}
void CfdpHandler::resumedIndication(const cfdp::TransactionId& id, size_t progress) {}
void CfdpHandler::faultIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code,
                                  size_t progress) {}
void CfdpHandler::abandonedIndication(const cfdp::TransactionId& id, cfdp::ConditionCode code,
                                      size_t progress) {}
void CfdpHandler::eofRecvIndication(const cfdp::TransactionId& id) {}

bool CfdpHandler::getRemoteCfg(const cfdp::EntityId& remoteId, cfdp::RemoteEntityCfg** cfg) {
  return false;
}

ReturnValue_t CfdpHandler::handleCfdpPacket(TmTcMessage& msg) {
  auto accessorPair = tcStore->getData(msg.getStorageId());
  PduHeaderReader reader(accessorPair.second.data(), accessorPair.second.size());
  ReturnValue_t result = reader.parseData();
  if (result != returnvalue::OK) {
    return result;
  }
  // The CFDP distributor should have taken care of ensuring the destination ID is correct
  PduTypes type = reader.getPduType();
  // Only the destination handler can process these PDUs
  if (type == PduTypes::FILE_DATA) {
  } else {
    // Route depending on directive type. Retrieve directive type from raw stream for better
    // performance (with size check)
  }
  return OK;
}
