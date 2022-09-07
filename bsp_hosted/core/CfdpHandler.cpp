#include "CfdpHandler.h"

#include "fsfw/ipc/QueueFactory.h"

using namespace returnvalue;
CfdpHandler::CfdpHandler(object_id_t objectId, AcceptsTelemetryIF& packetDest,
                         const cfdp::DestHandlerParams& destParams)
    : SystemObject(objectId), destHandler(destParams, cfdp::FsfwParams(packetDest, nullptr, this)) {
  // TODO: Make configurable?
  msgQueue = QueueFactory::instance()->createMessageQueue();
  destHandler.setMsgQueue(*msgQueue);
}

[[nodiscard]] const char* CfdpHandler::getName() const { return "CFDP Handler"; }

[[nodiscard]] uint32_t CfdpHandler::getIdentifier() const { return 0; }

[[nodiscard]] MessageQueueId_t CfdpHandler::getRequestQueue() const {
  // TODO: return TC queue here
  return 0;
}

ReturnValue_t CfdpHandler::initialize() {
  ReturnValue_t result = destHandler.initialize();
  if (result != OK) {
    return result;
  }
  return SystemObject::initialize();
}
