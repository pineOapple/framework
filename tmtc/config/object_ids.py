"""
@brief      This file transfers control of the object IDs to the user.
@details    Template configuration file. Copy this folder to the TMTC commander root and adapt
            it to your needs.
"""
from typing import Dict

PUS_SERVICE_17_ID = bytes([0x53, 0x00, 0x00, 0x17])
TEST_DEVICE_0_ID = bytes([0x44, 0x01, 0xAF, 0xFE])
TEST_DEVICE_1_ID = bytes([0x44, 0x02, 0xAF, 0xFE])


def get_object_ids() -> Dict[bytes, list]:
    object_id_dict = {
            PUS_SERVICE_17_ID: ["PUS Service 17"],
            TEST_DEVICE_0_ID: ["Test Device 0"],
            TEST_DEVICE_1_ID: ["Test Device 1"]
    }
    return object_id_dict
