"""
@brief      This file transfers control of TM parsing to the user
@details    Template configuration file. Copy this folder to the TMTC commander root and adapt
            it to your needs.
"""

from tmtccmd.ecss.tm import PusTelemetry
from tmtccmd.utility.logger import get_logger
from tmtccmd.pus_tm.service_1_verification import Service1TM
from tmtccmd.pus_tm.service_2_raw_cmd import Service2TM
from tmtccmd.pus_tm.service_3_housekeeping import Service3TM
from tmtccmd.pus_tm.service_5_event import Service5TM
from tmtccmd.pus_tm.service_8_functional_cmd import Service8TM
from tmtccmd.pus_tm.service_17_test import Service17TM
from tmtccmd.pus_tm.service_20_parameters import Service20TM
from tmtccmd.pus_tm.service_200_mode import Service200TM

LOGGER = get_logger()


def tm_user_factory_hook(raw_tm_packet: bytearray) -> PusTelemetry:
    service_type = raw_tm_packet[7]
    if service_type == 1:
        return Service1TM(raw_tm_packet)
    if service_type == 2:
        return Service2TM(raw_tm_packet)
    if service_type == 3:
        return Service3TM(raw_tm_packet)
    if service_type == 8:
        return Service8TM(raw_tm_packet)
    if service_type == 5:
        return Service5TM(raw_tm_packet)
    if service_type == 17:
        return Service17TM(raw_tm_packet)
    if service_type == 20:
        return Service20TM(raw_tm_packet)
    if service_type == 200:
        return Service200TM(raw_tm_packet)
    LOGGER.info("The service " + str(service_type) + " is not implemented in Telemetry Factory")
    return PusTelemetry(raw_tm_packet)
