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
from config.hook_implementation import FsfwHookBase
try:
    from tmtccmd.runner import run_tmtc_commander, initialize_tmtc_commander
except ImportError:
    run_tmtc_commander = None
    initialize_tmtc_commander = None
    print("Python tmtccmd submodule not installed")
    print("Install with \"cd tmtccmd && python3 -m pip install -e .\" for interactive installation")
    sys.exit(0)


def main():
    hook_obj = FsfwHookBase()
    initialize_tmtc_commander(hook_object=hook_obj)
    run_tmtc_commander(use_gui=False, app_name="TMTC Commander FSFW")


if __name__ == "__main__":
    main()
