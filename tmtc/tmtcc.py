#!/usr/bin/env python3
"""TMTC commander for FSFW Example"""
import tmtccmd
from common_tmtc.common import (
    tmtcc_post_args,
    tmtcc_pre_args
)
from config.hook import FsfwHookBase
from examples.tmtcc import EXAMPLE_APID
from tmtccmd.config import SetupParams, ArgParserWrapper, SetupWrapper


def main():
    tmtcc_pre_args()
    hook_obj = FsfwHookBase(json_cfg_path="tmtc_conf.json")
    params = SetupParams()
    parser_wrapper = ArgParserWrapper(hook_obj)
    parser_wrapper.parse()
    tmtccmd.init_printout(parser_wrapper.use_gui)
    parser_wrapper.set_params(params)
    params.apid = EXAMPLE_APID
    setup_wrapper = SetupWrapper(hook_obj, params)

    tmtcc_post_args(hook_obj=hook_obj, use_gui=False, args=args)


if __name__ == "__main__":
    main()
