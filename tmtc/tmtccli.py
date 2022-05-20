#!/usr/bin/env python3
"""TMTC commander for FSFW Example"""
from common_tmtc.tmtcc import (
    tmtcc_post_args,
    tmtcc_pre_args,
    create_default_args_parser,
    add_default_tmtccmd_args,
    parse_default_input_arguments,
)
from config.hook import FsfwHookBase


def main():
    tmtcc_pre_args()
    hook_obj = FsfwHookBase(json_cfg_path="tmtc_conf.json")
    arg_parser = create_default_args_parser()
    add_default_tmtccmd_args(arg_parser)
    args = parse_default_input_arguments(arg_parser, hook_obj)
    tmtcc_post_args(hook_obj=hook_obj, use_gui=False, args=args)


if __name__ == "__main__":
    main()
