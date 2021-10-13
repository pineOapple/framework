#!/usr/bin/env python3
"""
@brief      TMTC Commander entry point for command line mode.
@details
This client was developed by KSat for the SOURCE project to test the on-board software but
has evolved into a more generic tool for satellite developers to perform TMTC (Telemetry and Telecommand)
handling and testing via different communication interfaces. Currently, only the PUS standard is
implemented as a packet standard.

Run this file with the -h flag to display options.

@license
Copyright 2020 KSat e.V. Stuttgart

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author     R. Mueller
"""
import sys

from spacepackets.log import set_custom_console_logger_name
from common_tmtc.config.hook_implementation import FsfwHookBase
from common_tmtc.config.definitions import PUS_APID
from common_tmtc.pus_tm.factory_hook import ccsds_tm_handler
try:
    from tmtccmd.runner import run_tmtc_commander, initialize_tmtc_commander, add_ccsds_handler
    from tmtccmd.ccsds.handler import CcsdsTmHandler
    from tmtccmd.utility.logger import TMTC_LOGGER_NAME
except ImportError as error:
    run_tmtc_commander = None
    initialize_tmtc_commander = None
    print(error)
    print("Python tmtccmd submodule could not be imported")
    print("Install with \"cd tmtccmd && python3 -m pip install -e .\" for interactive installation")
    sys.exit(0)


def main():
    hook_obj = FsfwHookBase()
    initialize_tmtc_commander(hook_object=hook_obj)
    ccsds_handler = CcsdsTmHandler()
    ccsds_handler.add_tm_handler(apid=PUS_APID, pus_tm_handler=ccsds_tm_handler, max_queue_len=50)
    add_ccsds_handler(ccsds_handler)
    set_custom_console_logger_name(TMTC_LOGGER_NAME)
    run_tmtc_commander(use_gui=False, app_name="TMTC Commander FSFW")


if __name__ == "__main__":
    main()
