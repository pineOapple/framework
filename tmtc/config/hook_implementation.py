import argparse
from typing import Dict, Tuple, Optional

from tmtccmd.com_if.com_interface_base import CommunicationInterface
from tmtccmd.config.definitions import ServiceOpCodeDictT
from tmtccmd.config.hook import TmTcHookBase
from tmtccmd.core.backend import TmTcHandler
from tmtccmd.ecss.tm import PusTelemetry
from tmtccmd.pus_tc.definitions import TcQueueT
from tmtccmd.pus_tm.service_3_base import Service3Base
from tmtccmd.ecss.conf import PusVersion
from tmtccmd.utility.tmtc_printer import TmTcPrinter

from config.definitions import PUS_APID


class FsfwHookBase(TmTcHookBase):

    def get_version(self) -> str:
        from config.version import SW_NAME, SW_VERSION, SW_SUBVERSION, SW_SUBSUBVERSION
        return f"{SW_NAME} {SW_VERSION}.{SW_SUBVERSION}.{SW_SUBSUBVERSION}"

    def get_json_config_file_path(self) -> str:
        return "config/tmtc_config.json"

    def get_service_op_code_dictionary(self) -> ServiceOpCodeDictT:
        from tmtccmd.config.globals import get_default_service_op_code_dict
        return get_default_service_op_code_dict()

    def add_globals_pre_args_parsing(self, gui: bool = False):
        from tmtccmd.config.globals import set_default_globals_pre_args_parsing
        set_default_globals_pre_args_parsing(
            gui=gui, pus_tm_version=PusVersion.PUS_C, pus_tc_version=PusVersion.PUS_C, apid=PUS_APID
        )

    def add_globals_post_args_parsing(self, args: argparse.Namespace):
        from tmtccmd.config.globals import set_default_globals_post_args_parsing
        set_default_globals_post_args_parsing(args=args, json_cfg_path=self.get_json_config_file_path())

    def assign_communication_interface(
            self, com_if_key: str, tmtc_printer: TmTcPrinter
    ) -> Optional[CommunicationInterface]:
        from tmtccmd.config.com_if import create_communication_interface_default
        return create_communication_interface_default(
            com_if_key=com_if_key, tmtc_printer=tmtc_printer,
            json_cfg_path=self.get_json_config_file_path()
        )

    def perform_mode_operation(self, tmtc_backend: TmTcHandler, mode: int):
        print("No custom mode operation implemented")

    def pack_service_queue(self, service: int, op_code: str, service_queue: TcQueueT):
        from pus_tc.tc_packing import pack_service_queue_user
        pack_service_queue_user(service=service, op_code=op_code, tc_queue=service_queue)

    def get_object_ids(self) -> Dict[bytes, list]:
        from config.object_ids import get_object_ids
        return get_object_ids()

    @staticmethod
    def handle_service_8_telemetry(
            object_id: int, action_id: int, custom_data: bytearray
    ) -> Tuple[list, list]:
        from pus_tm.service_8_handling import custom_service_8_handling
        return custom_service_8_handling(
            object_id=object_id, action_id=action_id, custom_data=custom_data
        )

    @staticmethod
    def handle_service_3_housekeeping(
        object_id: bytes, set_id: int, hk_data: bytearray, service3_packet: Service3Base
    ) -> Tuple[list, list, bytearray, int]:
        from pus_tm.service_3_hk_handling import service_3_hk_handling
        return service_3_hk_handling(
            object_id=object_id, set_id=set_id, hk_data=hk_data, service3_packet=service3_packet
        )
