from tmtccmd.pus_tc.definitions import TcQueueT
from tmtccmd.pus_tc.service_17_test import pack_service17_ping_command, pack_generic_service17_test


def pack_service_17_commands(op_code: str, init_ssc: int, tc_queue: TcQueueT):
    if op_code == "0":
        tc_queue.appendleft(pack_service17_ping_command(ssc=init_ssc).pack_command_tuple())
    else:
        pack_generic_service17_test(tc_queue=tc_queue, init_ssc=init_ssc)
