#include "missionMessageTypes.h"

#include <fsfw/ipc/CommandMessage.h>
#include <fsfw/ipc/CommandMessageCleaner.h>

void messagetypes::clearMissionMessage(CommandMessage* message) {
  switch ((message->getMessageType())) {
    default:
      message->setCommand(CommandMessage::CMD_NONE);
      break;
  }
}
