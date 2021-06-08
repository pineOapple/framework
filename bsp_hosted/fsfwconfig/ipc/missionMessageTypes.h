#ifndef FSFWCONFIG_IPC_MISSIONMESSAGETYPES_H_
#define FSFWCONFIG_IPC_MISSIONMESSAGETYPES_H_

#include <fsfw/ipc/FwMessageTypes.h>

class CommandMessage;

namespace messagetypes {
/* First type must have number MESSAGE_TYPE::FW_MESSAGES_COUNT! */
/* Remember to add new message types to the clearMissionMessage function below! */
enum MISSION_MESSAGE_TYPE {
	COSTUM_MESSAGE = FW_MESSAGES_COUNT,
};

void clearMissionMessage(CommandMessage* message);

}

#endif /* FSFWCONFIG_IPC_MISSIONMESSAGETYPES_H_ */
