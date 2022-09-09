#!/usr/bin/env python3
"""TMTC commander for FSFW Example"""
import sys
import time
from pathlib import Path
from typing import Sequence, Optional

from spacepackets import SpacePacket, SpacePacketHeader, PacketTypes
from spacepackets.cfdp import ConditionCode, TransmissionModes, PduType, DirectiveType
from spacepackets.cfdp.pdu import AbstractFileDirectiveBase, PduHolder, PduFactory
from spacepackets.cfdp.pdu.helper import GenericPduPacket
from spacepackets.ecss import PusVerificator

import tmtccmd
from common_tmtc.common import (
    setup_params,
    setup_tmtc_handlers,
    setup_backend,
    EXAMPLE_APID,
)
from config.hook import FsfwHookBase
from spacepackets.util import UnsignedByteField
from tmtccmd import get_console_logger
from tmtccmd.cfdp import (
    LocalEntityCfg,
    CfdpUserBase,
    TransactionId,
    RemoteEntityCfg,
    RemoteEntityCfgTable,
    HostFilestore,
)
from tmtccmd.cfdp.request import PutRequestCfg, PutRequest
from tmtccmd.cfdp.user import (
    FileSegmentRecvdParams,
    MetadataRecvParams,
    TransactionFinishedParams,
)
from tmtccmd.core import BackendRequest
from tmtccmd.logging.pus import (
    RegularTmtcLogWrapper,
    RawTmtcTimedLogWrapper,
    TimedLogWhen,
)
from tmtccmd.pus import VerificationWrapper
from tmtccmd.util import ProvidesSeqCount
from tmtccmd.util.tmtc_printer import FsfwTmTcPrinter
from tmtccmd.cfdp.handler import DestHandler, SourceHandler

LOGGER = get_console_logger()


def main():
    setup_wrapper = setup_params(FsfwHookBase())
    tmtc_logger = RegularTmtcLogWrapper()
    printer = FsfwTmTcPrinter(tmtc_logger.logger)
    raw_logger = RawTmtcTimedLogWrapper(when=TimedLogWhen.PER_HOUR, interval=2)
    pus_verificator = PusVerificator()
    verif_wrapper = VerificationWrapper(
        console_logger=get_console_logger(),
        file_logger=printer.file_logger,
        pus_verificator=pus_verificator,
    )
    ccsds_handler, tc_handler = setup_tmtc_handlers(
        verif_wrapper=verif_wrapper, raw_logger=raw_logger, printer=printer
    )
    tmtccmd.setup(setup_wrapper)
    backend = setup_backend(
        setup_wrapper=setup_wrapper, ccsds_handler=ccsds_handler, tc_handler=tc_handler
    )
    try:
        while True:
            state = backend.periodic_op(None)
            if state.request == BackendRequest.TERMINATION_NO_ERROR:
                sys.exit(0)
            elif state.request == BackendRequest.DELAY_IDLE:
                LOGGER.info("TMTC Client in IDLE mode")
                time.sleep(3.0)
            elif state.request == BackendRequest.DELAY_LISTENER:
                time.sleep(0.8)
            elif state.request == BackendRequest.DELAY_CUSTOM:
                if state.next_delay.total_seconds() < 0.5:
                    time.sleep(state.next_delay.total_seconds())
                else:
                    time.sleep(0.5)
            elif state.request == BackendRequest.CALL_NEXT:
                pass
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
