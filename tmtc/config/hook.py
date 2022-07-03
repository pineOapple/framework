from typing import Optional

from common_tmtc.config.definitions import TM_SP_IDS
from common_tmtc.config.hook_implementation import CommonFsfwHookBase
from common_tmtc.pus_tc.cmd_definitions import common_fsfw_service_op_code_dict
from tmtccmd.com_if import ComInterface
from tmtccmd.config import TmTcDefWrapper


class FsfwHookBase(CommonFsfwHookBase):
    def get_tmtc_definitions(self) -> TmTcDefWrapper:
        return common_fsfw_service_op_code_dict()

    def assign_communication_interface(self, com_if_key: str) -> Optional[ComInterface]:
        from tmtccmd.config.com_if import create_communication_interface_default

        return create_communication_interface_default(
            com_if_key=com_if_key,
            json_cfg_path=self.json_cfg_path,
            space_packet_ids=TM_SP_IDS,
        )
