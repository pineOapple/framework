# -*- coding: utf-8 -*-
"""
@file   tmtcc_tc_service_200_mode.py
@brief  PUS Service 200:  PUS custom service 200: Mode commanding
@author R. Mueller
@date   02.05.2020
"""
from tmtccmd.config.definitions import QueueCommands
from tmtccmd.ecss.tc import PusTelecommand
from tmtccmd.pus_tc.packer import TcQueueT
from tmtccmd.pus_tc.service_200_mode import pack_mode_data

from config.object_ids import TEST_DEVICE_0_ID


def pack_service_200_commands_into(tc_queue: TcQueueT, op_code: str):
    if op_code == "0":
        pack_service_200_test_into(tc_queue=tc_queue, init_ssc=2000)


def pack_service_200_test_into(init_ssc: int, tc_queue: TcQueueT) -> int:
    new_ssc = init_ssc
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 200"))
    # Object ID: DUMMY Device
    object_id = TEST_DEVICE_0_ID
    # Set On Mode
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 200: Set Mode On"))
    mode_data = pack_mode_data(object_id, 1, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=new_ssc, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())
    new_ssc += 1
    # Set Normal mode
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 200: Set Mode Normal"))
    mode_data = pack_mode_data(object_id, 2, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=new_ssc, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())
    new_ssc += 1
    # Set Raw Mode
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 200: Set Mode Raw"))
    mode_data = pack_mode_data(object_id, 3, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=new_ssc, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())
    new_ssc += 1
    # Set Off Mode
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 200: Set Mode Off"))
    mode_data = pack_mode_data(object_id, 0, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=new_ssc, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())
    new_ssc += 1
    tc_queue.appendleft((QueueCommands.EXPORT_LOG, "log/tmtc_log_service200.txt"))
    return new_ssc

