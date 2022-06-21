#!/usr/bin/env python3
"""TMTC commander for the FSFW Example"""
from common_tmtc.tmtcc import tmtcc_post_args, tmtcc_pre_args


def main():
    hook_obj = tmtcc_pre_args()
    tmtcc_post_args(hook_obj=hook_obj, use_gui=True, args=None)


if __name__ == "__main__":
    main()
