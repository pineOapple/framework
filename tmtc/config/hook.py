from common_tmtc.config.hook_implementation import CommonFsfwHookBase
from tmtccmd.tc.definitions import TcQueueT


class FsfwHookBase(CommonFsfwHookBase):
    def pack_service_queue(self, service: int, op_code: str, service_queue: TcQueueT):
        from common_tmtc.pus_tc.tc_packing import common_service_queue_user

        common_service_queue_user(
            service=service, op_code=op_code, tc_queue=service_queue
        )
