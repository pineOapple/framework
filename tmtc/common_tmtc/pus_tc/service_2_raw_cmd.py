# -*- coding: utf-8 -*-
"""
@file   tmtcc_tc_service_2_raw_cmd.py
@brief  PUS Service 2: Device Access, native low-level commanding
@author R. Mueller
@date   01.11.2019
"""
import struct

from tmtccmd.config.definitions import QueueCommands
from tmtccmd.ecss.tc import PusTelecommand
from tmtccmd.pus_tc.definitions import TcQueueT
from common_tmtc.pus_tc.service_200_mode import pack_mode_data

from common_tmtc import pus_tc as cmd_data
from common_tmtc.config.object_ids import TEST_DEVICE_0_ID


def pack_service_2_commands_into(tc_queue: TcQueueT, op_code: str):
    if op_code == "0":
        pack_generic_service_2_test_into(0, tc_queue)
    else:
        print(f"pack_service_2_test: Operation code {op_code} unknown!")


def pack_generic_service_2_test_into(init_ssc: int, tc_queue: TcQueueT) -> int:
    new_ssc = init_ssc
    object_id = TEST_DEVICE_0_ID  # dummy device
    # Set Raw Mode
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 2: Setting Raw Mode"))
    mode_data = pack_mode_data(object_id, 3, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=new_ssc, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())
    new_ssc += 1
    # toggle wiretapping raw
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 2: Toggling Wiretapping Raw"))
    wiretapping_toggle_data = pack_wiretapping_mode(object_id, 1)
    toggle_wiretapping_on_command = PusTelecommand(
        service=2, subservice=129, ssc=new_ssc, app_data=wiretapping_toggle_data
    )
    tc_queue.appendleft(toggle_wiretapping_on_command.pack_command_tuple())
    new_ssc += 1
    # send raw command, wiretapping should be returned via TM[2,130] and TC[2,131]
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 2: Sending Raw Command"))
    raw_command = cmd_data.TEST_COMMAND_0
    raw_data = object_id + raw_command
    raw_command = PusTelecommand(service=2, subservice=128, ssc=new_ssc, app_data=raw_data)
    tc_queue.appendleft(raw_command.pack_command_tuple())
    new_ssc += 1
    # toggle wiretapping off
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 2: Toggle Wiretapping Off"))
    wiretapping_toggle_data = pack_wiretapping_mode(object_id, 0)
    toggle_wiretapping_off_command = PusTelecommand(service=2, subservice=129, ssc=new_ssc,
                                                    app_data=wiretapping_toggle_data)
    tc_queue.appendleft(toggle_wiretapping_off_command.pack_command_tuple())
    new_ssc += 1
    # send raw command which should be returned via TM[2,130]
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 2: Send second raw command"))
    command = PusTelecommand(service=2, subservice=128, ssc=new_ssc, app_data=raw_data)
    tc_queue.appendleft(command.pack_command_tuple())
    new_ssc += 1

    # Set mode off
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 2: Setting Off Mode"))
    mode_data = pack_mode_data(object_id, 0, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=new_ssc, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())
    new_ssc += 1
    tc_queue.appendleft((QueueCommands.EXPORT_LOG, "log/tmtc_log_service_2.txt"))
    return new_ssc


# wiretappingMode = 0: MODE_OFF, wiretappingMode = 1: MODE_RAW
def pack_wiretapping_mode(object_id, wiretapping_mode_):
    wiretapping_mode = struct.pack(">B", wiretapping_mode_)  # MODE_OFF : 0x00, MODE_RAW: 0x01
    wiretapping_toggle_data = object_id + wiretapping_mode
    return wiretapping_toggle_data
