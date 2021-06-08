#ifndef FSFWCONFIG_OBJECTS_SYSTEMOBJECTLIST_H_
#define FSFWCONFIG_OBJECTS_SYSTEMOBJECTLIST_H_

#include <commonSystemObjects.h>

namespace objects {
enum mission_objects {
    /* 0x62 ('b') Board and mission specific objects */
	UDP_BRIDGE = 0x62000300,
	UDP_POLLING_TASK = 0x62000400,
	/* Generic name for FSFW static ID setter */
	DOWNLINK_DESTINATION = UDP_BRIDGE
};
}

#endif /* FSFWCONFIG_OBJECTS_SYSTEMOBJECTLIST_H_ */
