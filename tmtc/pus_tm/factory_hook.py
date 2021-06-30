"""
@brief      This file transfers control of TM parsing to the user
@details    Template configuration file. Copy this folder to the TMTC commander root and adapt
            it to your needs.
"""

from tmtccmd.ecss.tm import PusTelemetry
from tmtccmd.utility.logger import get_console_logger
from tmtccmd.pus_tm.service_1_verification import Service1TM
from tmtccmd.pus_tm.service_2_raw_cmd import Service2TM
from tmtccmd.pus_tm.service_3_housekeeping import Service3TM
from tmtccmd.pus_tm.service_5_event import Service5TM
from tmtccmd.pus_tm.service_8_functional_cmd import Service8TM
from tmtccmd.pus_tm.service_17_test import Service17TM
from tmtccmd.pus_tm.service_20_parameters import Service20TM
from tmtccmd.pus_tm.service_200_mode import Service200TM
from tmtccmd.utility.tmtc_printer import TmTcPrinter

from config.definitions import PUS_APID


LOGGER = get_console_logger()


def ccsds_tm_handler(apid: int, raw_tm_packet: bytearray, tmtc_printer: TmTcPrinter) -> None:
    if apid == PUS_APID:
        pus_packet_factory(raw_tm_packet=raw_tm_packet, tmtc_printer=tmtc_printer)


def pus_packet_factory(raw_tm_packet: bytearray, tmtc_printer: TmTcPrinter):
    service_type = raw_tm_packet[7]
    tm_packet = None
    if service_type == 1:
        tm_packet = Service1TM(raw_tm_packet)
    if service_type == 2:
        tm_packet = Service2TM(raw_tm_packet)
    if service_type == 3:
        tm_packet = Service3TM(raw_tm_packet)
    if service_type == 8:
        tm_packet = Service8TM(raw_tm_packet)
    if service_type == 5:
        tm_packet = Service5TM(raw_tm_packet)
    if service_type == 17:
        tm_packet = Service17TM(raw_tm_packet)
    if service_type == 20:
        tm_packet = Service20TM(raw_tm_packet)
    if service_type == 200:
        tm_packet = Service200TM(raw_tm_packet)
    if tm_packet is None:
        LOGGER.info("The service " + str(service_type) + " is not implemented in Telemetry Factory")
        tm_packet = PusTelemetry(raw_tm_packet)
    tmtc_printer.print_telemetry(packet=tm_packet)
