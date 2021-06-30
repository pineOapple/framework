"""
@brief      This file transfers control of TC packing to the user
@details    Template configuration file. Copy this folder to the TMTC commander root and adapt
            it to your needs.
"""

import os
from collections import deque
from typing import Union

from pus_tc.service_20_parameters import pack_service20_commands_into
from pus_tc.service_2_raw_cmd import pack_service_2_commands_into
from pus_tc.service_3_housekeeping import pack_service_3_commands_into
from pus_tc.service_8_func_cmd import pack_service_8_commands_into
from tmtccmd.utility.logger import get_console_logger
from tmtccmd.pus_tc.definitions import TcQueueT
from tmtccmd.config.definitions import CoreServiceList
from tmtccmd.pus_tc.service_5_event import pack_generic_service5_test_into
from tmtccmd.pus_tc.service_17_test import pack_generic_service17_test
from pus_tc.service_200_mode import pack_service_200_commands_into

LOGGER = get_console_logger()


def pack_service_queue_user(service: Union[str, int], op_code: str, service_queue: TcQueueT):
    if service == CoreServiceList.SERVICE_2.value:
        return pack_service_2_commands_into(op_code=op_code, tc_queue=service_queue)
    if service == CoreServiceList.SERVICE_3.value:
        return pack_service_3_commands_into(op_code=op_code, tc_queue=service_queue)
    if service == CoreServiceList.SERVICE_5.value:
        return pack_generic_service5_test_into(tc_queue=service_queue)
    if service == CoreServiceList.SERVICE_8.value:
        return pack_service_8_commands_into(op_code=op_code, tc_queue=service_queue)
    if service == CoreServiceList.SERVICE_17.value:
        return pack_generic_service17_test(init_ssc=1700, tc_queue=service_queue)
    if service == CoreServiceList.SERVICE_20.value:
        return pack_service20_commands_into(tc_queue=service_queue, op_code=op_code)
    if service == CoreServiceList.SERVICE_200.value:
        return pack_service_200_commands_into(tc_queue=service_queue, op_code=op_code)
    LOGGER.warning("Invalid Service !")


def create_total_tc_queue_user() -> TcQueueT:
    if not os.path.exists("log"):
        os.mkdir("log")
    tc_queue = deque()
    pack_service_2_commands_into(op_code="0", tc_queue=tc_queue)
    pack_generic_service17_test(init_ssc=1700, tc_queue=tc_queue)
    return tc_queue
