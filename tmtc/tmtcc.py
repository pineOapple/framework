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


class CfdpCcsdsWrapper:
    def __init__(
        self,
        cfg: LocalEntityCfg,
        cfdp_seq_cnt_provider: ProvidesSeqCount,
        remote_cfg: Sequence[RemoteEntityCfg],
        ccsds_seq_cnt_provider: ProvidesSeqCount,
        ccsds_apid: int,
    ):
        self.handler = CfdpHandler(cfg, cfdp_seq_cnt_provider, remote_cfg)
        self.ccsds_seq_cnt_provider = ccsds_seq_cnt_provider
        self.ccsds_apid = ccsds_apid

    def pull_next_dest_packet(self) -> Optional[SpacePacket]:
        """Retrieves the next PDU to send and wraps it into a space packet"""
        next_packet = self.handler.pull_next_dest_packet()
        if next_packet is None:
            return next_packet
        sp_header = SpacePacketHeader(
            packet_type=PacketTypes.TC,
            apid=self.ccsds_apid,
            seq_count=self.ccsds_seq_cnt_provider.get_and_increment(),
            data_len=next_packet.packet_len - 1,
        )
        return SpacePacket(sp_header, None, next_packet.pack())

    def confirm_dest_packet_sent(self):
        self.handler.confirm_dest_packet_sent()

    def pass_packet(self, packet: SpacePacket):
        # Unwrap the user data and pass it to the handler
        pdu_raw = packet.user_data
        pdu_base = PduFactory.from_raw(pdu_raw)
        self.handler.pass_packet(pdu_base)


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

    def pull_next_dest_packet(self) -> Optional[PduHolder]:
        res = self.dest_handler.state_machine()
        if res.states.packet_ready:
            return self.dest_handler.pdu_holder
        return None

    def confirm_dest_packet_sent(self):
        self.dest_handler.confirm_packet_sent_advance_fsm()

    def pass_packet(self, packet: GenericPduPacket):
        """This function routes the packets based on PDU type and directive type if applicable.

        The routing is based on section 4.5 of the CFDP standard whcih specifies the PDU forwarding
        procedure.
        """
        if packet.pdu_type == PduType.FILE_DATA:
            self.dest_handler.pass_packet(packet)
        else:
            if packet.directive_type in [
                DirectiveType.METADATA_PDU,
                DirectiveType.EOF_PDU,
                DirectiveType.PROMPT_PDU,
            ]:
                # Section b) of 4.5.3: These PDUs should always be targeted towards the file
                # receiver a.k.a. the destination handler
                self.dest_handler.pass_packet(packet)
            elif packet.directive_type in [
                DirectiveType.FINISHED_PDU,
                DirectiveType.NAK_PDU,
                DirectiveType.KEEP_ALIVE_PDU,
            ]:
                # Section c) of 4.5.3: These PDUs should always be targeted towards the file sender
                # a.k.a. the source handler
                self.source_handler.pass_packet(packet)
            elif packet.directive_type == DirectiveType.ACK_PDU:
                # Section a): Recipient depends on the type of PDU that is being acknowledged.
                # We can simply extract the PDU type from the raw stream. If it is an EOF PDU,
                # this packet is passed to the source handler. For a finished PDU, it is
                # passed to the destination handler
                pdu_holder = PduHolder(packet)
                ack_pdu = pdu_holder.to_ack_pdu()
                if ack_pdu.directive_code_of_acked_pdu == DirectiveType.EOF_PDU:
                    self.source_handler.pass_packet(packet)
                elif ack_pdu.directive_code_of_acked_pdu == DirectiveType.FINISHED_PDU:
                    self.dest_handler.pass_packet(packet)

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
