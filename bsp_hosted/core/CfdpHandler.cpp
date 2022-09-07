#include "CfdpHandler.h"

#include "fsfw/ipc/QueueFactory.h"

using namespace returnvalue;
using namespace cfdp;

CfdpHandler::CfdpHandler(const HandlerCfg& cfg)
    : SystemObject(cfg.objectId),
      UserBase(cfg.vfs),
      destHandler(
          DestHandlerParams(cfg.cfg, *this, *this, cfg.packetInfoList, cfg.lostSegmentsList),
          FsfwParams(cfg.packetDest, nullptr, this)) {
  // TODO: Make queue params configurable, or better yet, expect it to be passed externally
  msgQueue = QueueFactory::instance()->createMessageQueue();
  destHandler.setMsgQueue(*msgQueue);
}

[[nodiscard]] const char* CfdpHandler::getName() const { return "CFDP Handler"; }

[[nodiscard]] uint32_t CfdpHandler::getIdentifier() const {
  // TODO: Return local entity ID? Which will probably be equal to APID
  return 0;
}

[[nodiscard]] MessageQueueId_t CfdpHandler::getRequestQueue() const { return msgQueue->getId(); }

ReturnValue_t CfdpHandler::initialize() {
  ReturnValue_t result = destHandler.initialize();
  if (result != OK) {
    return result;
  }
  return SystemObject::initialize();
}

ReturnValue_t CfdpHandler::performOperation(uint8_t operationCode) {
  // TODO: Receive TC packets and route them to source and dest handler, depending on which is
  //       correct or more appropriate
  return OK;
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
