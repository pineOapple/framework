"""
@brief      This file transfers control of housekeeping handling (PUS service 3) to the
            developer
@details    Template configuration file. Copy this folder to the TMTC commander root and adapt
            it to your needs.
"""
import struct
from typing import Tuple
from tmtccmd.pus_tm.service_3_housekeeping import Service3Base
from tmtccmd.utility.logger import get_console_logger

from common_tmtc.config.object_ids import TEST_DEVICE_0_ID, TEST_DEVICE_1_ID
LOGGER = get_console_logger()


def service_3_hk_handling(
        object_id: bytes, set_id: int, hk_data: bytearray, service3_packet: Service3Base
) -> Tuple[list, list, bytearray, int]:
    """
    This function is called when a Service 3 Housekeeping packet is received.

    Please note that the object IDs should be compared by value because direct comparison of
    enumerations does not work in Python. For example use:

        if object_id.value == ObjectIds.TEST_OBJECT.value

    to test equality based on the object ID list.

    @param object_id:
    @param set_id:
    @param hk_data:
    @param service3_packet:
    @return: Expects a tuple, consisting of two lists, a bytearray and an integer
    The first list contains the header columns, the second list the list with
    the corresponding values. The bytearray is the validity buffer, which is usually appended
    at the end of the housekeeping packet. The last value is the number of parameters.
    """
    if object_id == TEST_DEVICE_0_ID or object_id == TEST_DEVICE_1_ID:
        return handle_test_set_deserialization(hk_data=hk_data)
    else:
        LOGGER.info("Service3TM: Parsing for this SID has not been implemented.")
    return [], [], bytearray(), 0


def handle_test_set_deserialization(hk_data: bytearray) -> Tuple[list, list, bytearray, int]:
    header_list = []
    content_list = []
    validity_buffer = bytearray()
    # uint8 (1) + uint32_t (4) + float vector with 3 entries (12) + validity buffer (1)
    if len(hk_data) < 18:
        LOGGER.warning("Invalid HK data format for test set reply!")
        return header_list, content_list, validity_buffer, 0
    uint8_value = struct.unpack('!B', hk_data[0:1])[0]
    uint32_value = struct.unpack('!I', hk_data[1:5])[0]
    float_value_1 = struct.unpack('!f', hk_data[5:9])[0]
    float_value_2 = struct.unpack('!f', hk_data[9:13])[0]
    float_value_3 = struct.unpack('!f', hk_data[13:17])[0]
    validity_buffer.append(hk_data[17])
    header_list.append("uint8 value")
    header_list.append("uint32 value")
    header_list.append("float vec value 1")
    header_list.append("float vec value 2")
    header_list.append("float vec value 3")

    content_list.append(uint8_value)
    content_list.append(uint32_value)
    content_list.append(float_value_1)
    content_list.append(float_value_2)
    content_list.append(float_value_3)
    return header_list, content_list, validity_buffer, 3
