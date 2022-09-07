#ifndef FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H
#define FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H

#include "fsfw/cfdp/handler/DestHandler.h"
#include "fsfw/objectmanager/SystemObject.h"
#include "fsfw/tmtcservices/AcceptsTelecommandsIF.h"

class CfdpHandler : public SystemObject, public AcceptsTelecommandsIF {
 public:
  CfdpHandler(object_id_t objectId, AcceptsTelemetryIF& packetDest,
              const cfdp::DestHandlerParams& destParams);
  [[nodiscard]] const char* getName() const override;
  [[nodiscard]] uint32_t getIdentifier() const override;
  [[nodiscard]] MessageQueueId_t getRequestQueue() const override;

  ReturnValue_t initialize() override;

 private:
  MessageQueueIF* msgQueue = nullptr;
  cfdp::DestHandler destHandler;
};

#endif  // FSFW_EXAMPLE_HOSTED_CFDPHANDLER_H
