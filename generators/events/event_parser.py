"""Part of the Mission Operation Database Exporter for the FSFW project.
Event exporter.
"""
import datetime
import time
import os

from fsfwgen.events.event_parser import (
    handle_csv_export,
    handle_cpp_export,
    SubsystemDefinitionParser,
    EventParser,
)
from fsfwgen.parserbase.file_list_parser import FileListParser
from fsfwgen.utility.printer import PrettyPrinter
from fsfwgen.utility.file_management import copy_file
from fsfwgen.core import get_console_logger
from definitions import BSP_HOSTED, ROOT_DIR, OBSW_ROOT_DIR, EXAMPLE_COMMON_DIR

LOGGER = get_console_logger()
DATE_TODAY = datetime.datetime.now()
DATE_STRING_FULL = DATE_TODAY.strftime("%Y-%m-%d %H:%M:%S")

GENERATE_CPP = True
GENERATE_CPP_H = True
GENERATE_CSV = True
COPY_CPP_FILE = True
COPY_CPP_H_FILE = True
MOVE_CSV_FILE = True

PARSE_HOST_BSP = True

# Store these files relative to the events folder
CPP_FILENAME = f"{os.path.dirname(os.path.realpath(__file__))}/translateEvents.cpp"
CPP_H_FILENAME = f"{os.path.dirname(os.path.realpath(__file__))}/translateEvents.h"

# Store this file in the root of the generators folder
CSV_FILENAME = f"{ROOT_DIR}/{BSP_HOSTED}_events.csv"
CSV_COPY_DEST = f"{OBSW_ROOT_DIR}/tmtc/config/events.csv"
FSFW_CONFIG_ROOT = f"{OBSW_ROOT_DIR}/bsp_hosted/fsfwconfig"
CPP_COPY_DESTINATION = f"{FSFW_CONFIG_ROOT}/events/"

FILE_SEPARATOR = ";"
SUBSYSTEM_DEFINITION_DESTINATIONS = [
    f"{FSFW_CONFIG_ROOT}/events/subsystemIdRanges.h",
    f"{OBSW_ROOT_DIR}/fsfw/src/fsfw/events/fwSubsystemIdRanges.h",
    f"{EXAMPLE_COMMON_DIR}/config/commonSubsystemIds.h",
]
HEADER_DEFINITION_DESTINATIONS = [
    f"{OBSW_ROOT_DIR}/bsp_hosted",
    f"{OBSW_ROOT_DIR}/fsfw/",
    f"{FSFW_CONFIG_ROOT}",
]


def parse_events(
    generate_csv: bool = True, generate_cpp: bool = True, print_events: bool = True
):
    LOGGER.info("EventParser: Parsing events: ")
    # Small delay for clean printout
    time.sleep(0.01)
    event_list = generate_event_list()
    if print_events:
        PrettyPrinter.pprint(event_list)
        # Delay for clean printout
        time.sleep(0.1)
    # xml_test()
    if generate_csv:
        handle_csv_export(
            file_name=CSV_FILENAME, event_list=event_list, file_separator=FILE_SEPARATOR
        )
        LOGGER.info(f"Copying CSV file to {CSV_COPY_DEST}")
        copy_file(
            filename=CSV_FILENAME, destination=CSV_COPY_DEST, delete_existing_file=True
        )

    if generate_cpp:
        handle_cpp_export(
            event_list=event_list,
            date_string=DATE_STRING_FULL,
            file_name=CPP_FILENAME,
            generate_header=GENERATE_CPP_H,
            header_file_name=CPP_H_FILENAME,
        )
        if COPY_CPP_FILE:
            LOGGER.info(
                f"EventParser: Copying CPP translation file to {CPP_COPY_DESTINATION}"
            )
            copy_file(CPP_FILENAME, CPP_COPY_DESTINATION)
            copy_file(CPP_H_FILENAME, CPP_COPY_DESTINATION)


def generate_event_list() -> list:
    subsystem_parser = SubsystemDefinitionParser(SUBSYSTEM_DEFINITION_DESTINATIONS)
    subsystem_table = subsystem_parser.parse_files()
    LOGGER.info(f"Found {len(subsystem_table)} subsystem definitions.")
    PrettyPrinter.pprint(subsystem_table)
    event_header_parser = FileListParser(HEADER_DEFINITION_DESTINATIONS)
    event_headers = event_header_parser.parse_header_files(
        True, "Parsing event header file list:\n", True
    )
    # PrettyPrinter.pprint(event_headers)
    # myEventList = parseHeaderFiles(subsystem_table, event_headers)
    event_parser = EventParser(event_headers, subsystem_table)
    event_parser.obsw_root_path = OBSW_ROOT_DIR
    event_parser.set_moving_window_mode(moving_window_size=7)
    event_table = event_parser.parse_files()
    event_list = sorted(event_table.items())
    LOGGER.info(f"Found {len(event_list)} entries")
    return event_list
