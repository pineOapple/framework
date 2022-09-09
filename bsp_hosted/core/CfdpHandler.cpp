#include "CfdpHandler.h"

#include "fsfw/cfdp/pdu/AckPduReader.h"
#include "fsfw/cfdp/pdu/PduHeaderReader.h"
#include "fsfw/ipc/QueueFactory.h"
#include "fsfw/tmtcservices/TmTcMessage.h"

using namespace returnvalue;
using namespace cfdp;

CfdpHandler::CfdpHandler(const FsfwHandlerParams& fsfwParams, const CfdpHandlerCfg& cfdpCfg)
    : SystemObject(fsfwParams.objectId),
      UserBase(fsfwParams.vfs),
      destHandler(DestHandlerParams(LocalEntityCfg(cfdpCfg.id, cfdpCfg.indicCfg, *this), *this,
                                    cfdpCfg.remoteCfgProvider, cfdpCfg.packetInfoList,
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
  auto& fsmRes = destHandler.performStateMachine();
  // TODO: Error handling?
  while (fsmRes.callStatus == CallStatus::CALL_AGAIN) {
    destHandler.performStateMachine();
    // TODO: Error handling?
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

ReturnValue_t CfdpHandler::handleCfdpPacket(TmTcMessage& msg) {
  auto accessorPair = tcStore->getData(msg.getStorageId());
  PduHeaderReader reader(accessorPair.second.data(), accessorPair.second.size());
  ReturnValue_t result = reader.parseData();
  if (result != returnvalue::OK) {
    return INVALID_PDU_FORMAT;
  }
  // The CFDP distributor should have taken care of ensuring the destination ID is correct
  PduTypes type = reader.getPduType();
  // Only the destination handler can process these PDUs
  if (type == PduTypes::FILE_DATA) {
    // Disable auto-deletion of packet
    accessorPair.second.release();
    PacketInfo info(type, msg.getStorageId());
    result = destHandler.passPacket(info);
  } else {
    // Route depending on PDU type and directive type if applicable. It retrieves directive type
    // from the raw stream for better performance (with sanity and directive code check).
    // The routing is based on section 4.5 of the CFDP standard which specifies the PDU forwarding
    // procedure.

    // PDU header only. Invalid supplied data. A directive packet should have a valid data field
    // with at least one byte being the directive code
    const uint8_t* pduDataField = reader.getPduDataField();
    if (pduDataField == nullptr) {
      return INVALID_PDU_FORMAT;
    }
    if (not FileDirectiveReader::checkFileDirective(pduDataField[0])) {
      return INVALID_DIRECTIVE_FIELD;
    }
    auto directive = static_cast<FileDirectives>(pduDataField[0]);

    auto passToDestHandler = [&]() {
      accessorPair.second.release();
      PacketInfo info(type, msg.getStorageId(), directive);
      result = destHandler.passPacket(info);
    };
    auto passToSourceHandler = [&]() {

    };
    if (directive == FileDirectives::METADATA or directive == FileDirectives::EOF_DIRECTIVE or
        directive == FileDirectives::PROMPT) {
      // Section b) of 4.5.3: These PDUs should always be targeted towards the file receiver a.k.a.
      // the destination handler
      passToDestHandler();
    } else if (directive == FileDirectives::FINISH or directive == FileDirectives::NAK or
               directive == FileDirectives::KEEP_ALIVE) {
      // Section c) of 4.5.3: These PDUs should always be targeted towards the file sender a.k.a.
      // the source handler
      passToSourceHandler();
    } else if (directive == FileDirectives::ACK) {
      // Section a): Recipient depends of the type of PDU that is being acknowledged. We can simply
      // extract the PDU type from the raw stream. If it is an EOF PDU, this packet is passed to
      // the source handler, for a Finished PDU, it is passed to the destination handler.
      FileDirectives ackedDirective;
      if (not AckPduReader::checkAckedDirectiveField(pduDataField[1], ackedDirective)) {
        return INVALID_ACK_DIRECTIVE_FIELDS;
      }
      if (ackedDirective == FileDirectives::EOF_DIRECTIVE) {
        passToSourceHandler();
      } else if (ackedDirective == FileDirectives::FINISH) {
        passToDestHandler();
      }
    }
  }
  return result;
}

void CfdpHandler::noticeOfSuspensionCb(cfdp::ConditionCode code) {}
void CfdpHandler::noticeOfCancellationCb(cfdp::ConditionCode code) {}
void CfdpHandler::abandonCb(cfdp::ConditionCode code) {}
void CfdpHandler::ignoreCb(cfdp::ConditionCode code) {}
