/**
 * @brief	Auto-generated object translation file.
 * @details
 * Contains 37 translations.
 * Generated on: 2021-05-28 18:12:56
 */
#include "translateObjects.h"

const char *TEST_ASSEMBLY_STRING = "TEST_ASSEMBLY";
const char *TEST_CONTROLLER_STRING = "TEST_CONTROLLER";
const char *TEST_DEVICE_HANDLER_0_STRING = "TEST_DEVICE_HANDLER_0";
const char *TEST_DEVICE_HANDLER_1_STRING = "TEST_DEVICE_HANDLER_1";
const char *TEST_ECHO_COM_IF_STRING = "TEST_ECHO_COM_IF";
const char *FSFW_OBJECTS_START_STRING = "FSFW_OBJECTS_START";
const char *PUS_SERVICE_1_VERIFICATION_STRING = "PUS_SERVICE_1_VERIFICATION";
const char *PUS_SERVICE_2_DEVICE_ACCESS_STRING = "PUS_SERVICE_2_DEVICE_ACCESS";
const char *PUS_SERVICE_3_HOUSEKEEPING_STRING = "PUS_SERVICE_3_HOUSEKEEPING";
const char *PUS_SERVICE_5_EVENT_REPORTING_STRING = "PUS_SERVICE_5_EVENT_REPORTING";
const char *PUS_SERVICE_8_FUNCTION_MGMT_STRING = "PUS_SERVICE_8_FUNCTION_MGMT";
const char *PUS_SERVICE_9_TIME_MGMT_STRING = "PUS_SERVICE_9_TIME_MGMT";
const char *PUS_SERVICE_17_TEST_STRING = "PUS_SERVICE_17_TEST";
const char *PUS_SERVICE_20_PARAMETERS_STRING = "PUS_SERVICE_20_PARAMETERS";
const char *PUS_SERVICE_200_MODE_MGMT_STRING = "PUS_SERVICE_200_MODE_MGMT";
const char *PUS_SERVICE_201_HEALTH_STRING = "PUS_SERVICE_201_HEALTH";
const char *HEALTH_TABLE_STRING = "HEALTH_TABLE";
const char *MODE_STORE_STRING = "MODE_STORE";
const char *EVENT_MANAGER_STRING = "EVENT_MANAGER";
const char *INTERNAL_ERROR_REPORTER_STRING = "INTERNAL_ERROR_REPORTER";
const char *TC_STORE_STRING = "TC_STORE";
const char *TM_STORE_STRING = "TM_STORE";
const char *IPC_STORE_STRING = "IPC_STORE";
const char *TIME_STAMPER_STRING = "TIME_STAMPER";
const char *FSFW_OBJECTS_END_STRING = "FSFW_OBJECTS_END";
const char *UDP_BRIDGE_STRING = "UDP_BRIDGE";
const char *UDP_POLLING_TASK_STRING = "UDP_POLLING_TASK";
const char *CCSDS_DISTRIBUTOR_STRING = "CCSDS_DISTRIBUTOR";
const char *PUS_DISTRIBUTOR_STRING = "PUS_DISTRIBUTOR";
const char *TM_FUNNEL_STRING = "TM_FUNNEL";
const char *TEST_DUMMY_1_STRING = "TEST_DUMMY_1";
const char *TEST_DUMMY_2_STRING = "TEST_DUMMY_2";
const char *TEST_DUMMY_3_STRING = "TEST_DUMMY_3";
const char *TEST_DUMMY_4_STRING = "TEST_DUMMY_4";
const char *TEST_DUMMY_5_STRING = "TEST_DUMMY_5";
const char *TEST_TASK_STRING = "TEST_TASK";
const char *NO_OBJECT_STRING = "NO_OBJECT";

const char* translateObject(object_id_t object) {
	switch( (object & 0xFFFFFFFF) ) {
	case 0x4100CAFE:
		return TEST_ASSEMBLY_STRING;
	case 0x4301CAFE:
		return TEST_CONTROLLER_STRING;
	case 0x4401AFFE:
		return TEST_DEVICE_HANDLER_0_STRING;
	case 0x4402AFFE:
		return TEST_DEVICE_HANDLER_1_STRING;
	case 0x4900AFFE:
		return TEST_ECHO_COM_IF_STRING;
	case 0x53000000:
		return FSFW_OBJECTS_START_STRING;
	case 0x53000001:
		return PUS_SERVICE_1_VERIFICATION_STRING;
	case 0x53000002:
		return PUS_SERVICE_2_DEVICE_ACCESS_STRING;
	case 0x53000003:
		return PUS_SERVICE_3_HOUSEKEEPING_STRING;
	case 0x53000005:
		return PUS_SERVICE_5_EVENT_REPORTING_STRING;
	case 0x53000008:
		return PUS_SERVICE_8_FUNCTION_MGMT_STRING;
	case 0x53000009:
		return PUS_SERVICE_9_TIME_MGMT_STRING;
	case 0x53000017:
		return PUS_SERVICE_17_TEST_STRING;
	case 0x53000020:
		return PUS_SERVICE_20_PARAMETERS_STRING;
	case 0x53000200:
		return PUS_SERVICE_200_MODE_MGMT_STRING;
	case 0x53000201:
		return PUS_SERVICE_201_HEALTH_STRING;
	case 0x53010000:
		return HEALTH_TABLE_STRING;
	case 0x53010100:
		return MODE_STORE_STRING;
	case 0x53030000:
		return EVENT_MANAGER_STRING;
	case 0x53040000:
		return INTERNAL_ERROR_REPORTER_STRING;
	case 0x534f0100:
		return TC_STORE_STRING;
	case 0x534f0200:
		return TM_STORE_STRING;
	case 0x534f0300:
		return IPC_STORE_STRING;
	case 0x53500010:
		return TIME_STAMPER_STRING;
	case 0x53ffffff:
		return FSFW_OBJECTS_END_STRING;
	case 0x62000300:
		return UDP_BRIDGE_STRING;
	case 0x62000400:
		return UDP_POLLING_TASK_STRING;
	case 0x63000000:
		return CCSDS_DISTRIBUTOR_STRING;
	case 0x63000001:
		return PUS_DISTRIBUTOR_STRING;
	case 0x63000002:
		return TM_FUNNEL_STRING;
	case 0x74000001:
		return TEST_DUMMY_1_STRING;
	case 0x74000002:
		return TEST_DUMMY_2_STRING;
	case 0x74000003:
		return TEST_DUMMY_3_STRING;
	case 0x74000004:
		return TEST_DUMMY_4_STRING;
	case 0x74000005:
		return TEST_DUMMY_5_STRING;
	case 0x7400CAFE:
		return TEST_TASK_STRING;
	case 0xFFFFFFFF:
		return NO_OBJECT_STRING;
	default:
		return "UNKNOWN_OBJECT";
	}
	return 0;
}
