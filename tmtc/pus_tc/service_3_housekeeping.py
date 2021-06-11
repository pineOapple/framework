from tmtccmd.config.definitions import QueueCommands
from tmtccmd.pus_tc.service_200_mode import pack_mode_data
from tmtccmd.pus_tc.service_20_parameter import pack_boolean_parameter_command
from tmtccmd.pus_tc.service_3_housekeeping import make_sid, generate_one_hk_command, \
    Srv3Subservice
from tmtccmd.ecss.tc import PusTelecommand
from tmtccmd.pus_tc.definitions import TcQueueT
from tmtccmd.pus_tc.service_8_functional_cmd import generate_action_command

from config.object_ids import TEST_DEVICE_0_ID, TEST_DEVICE_1_ID


# Set IDs
TEST_SET_ID = 0

# Action IDs
TEST_NOTIFICATION_ACTION_ID = 3

# Parameters
PARAM_ACTIVATE_CHANGING_DATASETS = 4


def pack_service_3_commands_into(tc_queue: TcQueueT, op_code: str):
    current_ssc = 3000
    # TODO: Import this from config instead
    device_idx = 0
    if device_idx == 0:
        object_id = TEST_DEVICE_0_ID
    else:
        object_id = TEST_DEVICE_1_ID

    if op_code == "0":
        # This will pack all the tests
        pack_service_3_test_info(tc_queue=tc_queue, init_ssc=current_ssc, object_id=object_id,
                                 device_idx=device_idx)
    elif op_code == "1":
        # Extremely simple, generate one HK packet
        pack_gen_one_hk_command(tc_queue=tc_queue, device_idx=device_idx, init_ssc=current_ssc,
                                object_id=object_id)
    elif op_code == "2":
        # Housekeeping basic test
        pack_housekeeping_basic_test(tc_queue=tc_queue, object_id=object_id, init_ssc=current_ssc)
    elif op_code == "3":
        # Notification demo
        pack_notification_basic_test(tc_queue=tc_queue, object_id=object_id, init_ssc=current_ssc)


def pack_service_3_test_info(tc_queue: TcQueueT, device_idx: int, object_id: bytearray,
                             init_ssc: int):
    tc_queue.appendleft((QueueCommands.PRINT, "Service 3 (Housekeeping Service): All tests"))
    current_ssc = init_ssc

    current_ssc += pack_gen_one_hk_command(
        tc_queue=tc_queue, device_idx=device_idx, object_id=object_id, init_ssc=current_ssc
    )
    current_ssc += pack_housekeeping_basic_test(
       tc_queue=tc_queue, object_id=object_id, init_ssc=current_ssc
    )
    current_ssc += pack_notification_basic_test(
        tc_queue=tc_queue, object_id=object_id, init_ssc=current_ssc, enable_normal_mode=False
    )


def pack_gen_one_hk_command(
        tc_queue: TcQueueT, device_idx: int, init_ssc: int, object_id: bytearray
) -> int:
    test_sid = make_sid(object_id=object_id, set_id=TEST_SET_ID)
    tc_queue.appendleft(
        (QueueCommands.PRINT, f"Service 3 Test: Generate one test set packet for "
                              f"test device {device_idx}")
    )
    command = generate_one_hk_command(ssc=init_ssc, sid=test_sid)
    init_ssc += 1
    tc_queue.appendleft(command.pack_command_tuple())
    return init_ssc


def pack_housekeeping_basic_test(
        tc_queue: TcQueueT, object_id: bytearray, init_ssc: int, enable_normal_mode: bool = True
) -> int:
    """
    This basic test will request one HK packet, then it will enable periodic packets and listen
    to the periodic packets for a few seconds. After that, HK packets will be disabled again.
    """
    test_sid = make_sid(object_id=object_id, set_id=TEST_SET_ID)
    current_ssc = init_ssc
    # Enable changing datasets via parameter service (Service 20)
    tc_queue.appendleft((QueueCommands.PRINT, "Service 3 Test: Performing basic HK tests"))

    if enable_normal_mode:
        # Set mode normal so that sets are changed/read regularly
        tc_queue.appendleft((QueueCommands.PRINT, "Service 3 Test: Set Normal Mode"))
        mode_data = pack_mode_data(object_id, 2, 0)
        command = PusTelecommand(service=200, subservice=1, ssc=current_ssc, app_data=mode_data)
        current_ssc += 1
        tc_queue.appendleft(command.pack_command_tuple())

    tc_queue.appendleft((QueueCommands.PRINT, "Enabling changing datasets"))
    command = pack_boolean_parameter_command(
        object_id=object_id, domain_id=0, unique_id=PARAM_ACTIVATE_CHANGING_DATASETS,
        parameter=True, ssc=current_ssc
    )
    current_ssc += 1
    tc_queue.appendleft(command.pack_command_tuple())

    # Enable periodic reporting
    tc_queue.appendleft((QueueCommands.PRINT,
                         "Enabling periodic thermal sensor packet generation: "))
    command = PusTelecommand(service=3, subservice=Srv3Subservice.ENABLE_PERIODIC_HK_GEN.value,
                             ssc=current_ssc, app_data=test_sid)
    current_ssc += 1
    tc_queue.appendleft(command.pack_command_tuple())

    tc_queue.appendleft((QueueCommands.WAIT, 2.0))

    # Disable periodic reporting
    tc_queue.appendleft((QueueCommands.PRINT,
                         "Disabling periodic thermal sensor packet generation: "))
    command = PusTelecommand(service=3, subservice=Srv3Subservice.DISABLE_PERIODIC_HK_GEN.value,
                             ssc=current_ssc, app_data=test_sid)
    current_ssc += 1
    tc_queue.appendleft(command.pack_command_tuple())

    # Disable changing datasets via parameter service (Service 20)
    tc_queue.appendleft((QueueCommands.PRINT, "Disabling changing datasets"))
    command = pack_boolean_parameter_command(
        object_id=object_id, domain_id=0, unique_id=PARAM_ACTIVATE_CHANGING_DATASETS,
        parameter=False, ssc=current_ssc
    )
    current_ssc += 1
    tc_queue.appendleft(command.pack_command_tuple())
    return current_ssc


def pack_notification_basic_test(tc_queue: TcQueueT, object_id: bytearray, init_ssc: int,
                                 enable_normal_mode: bool = True) -> int:
    current_ssc = init_ssc
    tc_queue.appendleft((QueueCommands.PRINT, "Service 3 Test: Performing notification tests"))

    if enable_normal_mode:
        # Set mode normal so that sets are changed/read regularly
        tc_queue.appendleft((QueueCommands.PRINT, "Service 3 Test: Set Normal Mode"))
        mode_data = pack_mode_data(object_id, 2, 0)
        command = PusTelecommand(service=200, subservice=1, ssc=current_ssc, app_data=mode_data)
        current_ssc += 1
        tc_queue.appendleft(command.pack_command_tuple())

    tc_queue.appendleft((QueueCommands.PRINT, "Triggering notification"))
    command = generate_action_command(
        object_id=object_id, action_id=TEST_NOTIFICATION_ACTION_ID, ssc=current_ssc
    )
    tc_queue.appendleft(command.pack_command_tuple())
    current_ssc += 1
    return current_ssc
