from tmtccmd.config.definitions import QueueCommands
from tmtccmd.ecss.tc import PusTelecommand
from tmtccmd.pus_tc.definitions import TcQueueT

import pus_tc.command_data as cmd_data
from pus_tc.service_200_mode import pack_mode_data

from config.object_ids import TEST_DEVICE_0_ID


def pack_service_8_commands_into(tc_queue: TcQueueT, op_code: str):
    if op_code == "0":
        pack_generic_service_8_test_into(tc_queue=tc_queue)
    else:
        print(f"pack_service_8_test: Operation code {op_code} unknown!")


def pack_generic_service_8_test_into(tc_queue: TcQueueT):
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 8"))
    object_id = TEST_DEVICE_0_ID

    # set mode on
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 8: Set On Mode"))
    mode_data = pack_mode_data(object_id, 1, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=800, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())

    # set mode normal
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 8: Set Normal Mode"))
    mode_data = pack_mode_data(object_id, 2, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=810, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())

    # Direct command which triggers completion reply
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 8: Trigger Step and Completion Reply"))
    action_id = cmd_data.TEST_COMMAND_0
    direct_command = object_id + action_id
    command = PusTelecommand(service=8, subservice=128, ssc=820, app_data=direct_command)
    tc_queue.appendleft(command.pack_command_tuple())

    # Direct command which triggers _tm_data reply
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 8: Trigger Data Reply"))
    action_id = cmd_data.TEST_COMMAND_1
    command_param1 = cmd_data.TEST_COMMAND_1_PARAM_1
    command_param2 = cmd_data.TEST_COMMAND_1_PARAM_2
    direct_command = object_id + action_id + command_param1 + command_param2
    command = PusTelecommand(service=8, subservice=128, ssc=830, app_data=direct_command)
    tc_queue.appendleft(command.pack_command_tuple())

    # Set mode off
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 8: Set Off Mode"))
    mode_data = pack_mode_data(object_id, 0, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=800, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())

    tc_queue.appendleft((QueueCommands.EXPORT_LOG, "log/tmtc_log_service_8.txt"))
