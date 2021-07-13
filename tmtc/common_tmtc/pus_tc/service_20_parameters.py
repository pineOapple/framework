import struct

from tmtccmd.config.definitions import QueueCommands
from tmtccmd.ecss.tc import PusTelecommand
from tmtccmd.pus_tc.definitions import TcQueueT
from tmtccmd.pus_tc.service_20_parameter import pack_type_and_matrix_data, \
    pack_parameter_id
from tmtccmd.pus_tc.service_200_mode import pack_mode_data
from tmtccmd.utility.logger import get_console_logger

from common_tmtc.config.object_ids import TEST_DEVICE_0_ID

LOGGER = get_console_logger()


def pack_service20_commands_into(tc_queue: TcQueueT, op_code: str):
    if op_code == "0":
        pack_service20_test_into(tc_queue=tc_queue)


def pack_service20_test_into(tc_queue: TcQueueT, called_externally: bool = False):
    if called_externally is False:
        tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 20"))
    object_id = TEST_DEVICE_0_ID

    # set mode normal
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 20: Set Normal Mode"))
    mode_data = pack_mode_data(object_id, 2, 0)
    command = PusTelecommand(service=200, subservice=1, ssc=2000, app_data=mode_data)
    tc_queue.appendleft(command.pack_command_tuple())

    load_param_0_simple_test_commands(tc_queue=tc_queue)
    load_param_1_simple_test_commands(tc_queue=tc_queue)
    load_param_2_simple_test_commands(tc_queue=tc_queue)

    if called_externally is False:
        tc_queue.appendleft((QueueCommands.EXPORT_LOG, "log/tmtc_log_service20.txt"))


def load_param_0_simple_test_commands(tc_queue: TcQueueT):
    object_id = TEST_DEVICE_0_ID
    parameter_id_0 = pack_parameter_id(domain_id=0, unique_id=0, linear_index=0)
    # test checking Load for uint32_t
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 20: Load uint32_t"))
    type_and_matrix_data = pack_type_and_matrix_data(3, 14, 1, 1)
    parameter_data = struct.pack("!I", 42)
    payload = object_id + parameter_id_0 + type_and_matrix_data + parameter_data
    command = PusTelecommand(service=20, subservice=128, ssc=2010, app_data=payload)
    tc_queue.appendleft(command.pack_command_tuple())

    # test checking Dump for uint32_t
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 20: Dump uint32_t"))
    payload = object_id + parameter_id_0
    command = PusTelecommand(service=20, subservice=129, ssc=2020, app_data=payload)
    tc_queue.appendleft(command.pack_command_tuple())


def load_param_1_simple_test_commands(tc_queue: TcQueueT):
    object_id = TEST_DEVICE_0_ID
    parameter_id_1 = pack_parameter_id(domain_id=0, unique_id=1, linear_index=0)
    # test checking Load for int32_t
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 20: Load int32_t"))
    type_and_matrix_data = pack_type_and_matrix_data(4, 14, 1, 1)
    parameter_data = struct.pack("!i", -42)
    payload = object_id + parameter_id_1 + type_and_matrix_data + parameter_data
    command = PusTelecommand(service=20, subservice=128, ssc=2030, app_data=payload)
    tc_queue.appendleft(command.pack_command_tuple())

    # test checking Dump for int32_t
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 20: Dump int32_t"))
    payload = object_id + parameter_id_1
    command = PusTelecommand(service=20, subservice=129, ssc=2040, app_data=payload)
    tc_queue.appendleft(command.pack_command_tuple())


def load_param_2_simple_test_commands(tc_queue: TcQueueT):
    object_id = TEST_DEVICE_0_ID
    parameter_id_2 = pack_parameter_id(domain_id=0, unique_id=2, linear_index=0)
    # test checking Load for float
    tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 20: Load float"))
    type_and_matrix_data = pack_type_and_matrix_data(ptc=5, pfc=1, rows=1, columns=3)
    parameter_data = struct.pack("!fff", 4.2, -4.2, 49)
    payload = object_id + parameter_id_2 + type_and_matrix_data + parameter_data
    command = PusTelecommand(service=20, subservice=128, ssc=2050, app_data=payload)
    tc_queue.appendleft(command.pack_command_tuple())

    # test checking Dump for float
    # Skip dump for now, still not properly implemented
    # tc_queue.appendleft((QueueCommands.PRINT, "Testing Service 20: Dump float"))
    # payload = object_id + parameter_id_2
    # command = PusTelecommand(service=20, subservice=129, ssc=2060, app_data=payload)
    # tc_queue.appendleft(command.pack_command_tuple())

