#!/usr/bin/env python3
"""TMTC commander for FSFW Example"""
import sys
import time
from pathlib import Path
from typing import Sequence

from spacepackets.cfdp import ConditionCode, TransmissionModes
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


class CfdpHandler(CfdpUserBase):
    def __init__(
        self,
        cfg: LocalEntityCfg,
        seq_cnt_provider: ProvidesSeqCount,
        remote_cfg: Sequence[RemoteEntityCfg],
    ):
        vfs = HostFilestore()
        super().__init__(vfs)
        self.dest_id = UnsignedByteField(EXAMPLE_APID, 2)
        self.remote_cfg_table = RemoteEntityCfgTable()
        self.remote_cfg_table.add_remote_entities(remote_cfg)
        self.dest_handler = DestHandler(cfg, self, self.remote_cfg_table)
        self.source_handler = SourceHandler(cfg, seq_cnt_provider, self)

    def put_request_file(
        self,
        source_path: Path,
        dest_path: Path,
        trans_mode: TransmissionModes,
        closure_requested: bool,
    ):
        put_request_cfg = PutRequestCfg(
            destination_id=self.dest_id,
            source_file=source_path,
            dest_file=dest_path.as_posix(),
            trans_mode=trans_mode,
            closure_requested=closure_requested,
        )
        put_request = PutRequest(put_request_cfg)
        self.source_handler.put_request(
            put_request, self.remote_cfg_table.get_remote_entity(self.dest_id)
        )

    def transaction_indication(self, transaction_id: TransactionId):
        pass

    def eof_sent_indication(self, transaction_id: TransactionId):
        pass

    def transaction_finished_indication(self, params: TransactionFinishedParams):
        pass

    def metadata_recv_indication(self, params: MetadataRecvParams):
        pass

    def file_segment_recv_indication(self, params: FileSegmentRecvdParams):
        pass

    def report_indication(self, transaction_id: TransactionId, status_report: any):
        pass

    def suspended_indication(
        self, transaction_id: TransactionId, cond_code: ConditionCode
    ):
        pass

    def resumed_indication(self, transaction_id: TransactionId, progress: int):
        pass

    def fault_indication(
        self, transaction_id: TransactionId, cond_code: ConditionCode, progress: int
    ):
        pass

    def abandoned_indication(
        self, transaction_id: TransactionId, cond_code: ConditionCode, progress: int
    ):
        pass

    def eof_recv_indication(self, transaction_id: TransactionId):
        pass


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
