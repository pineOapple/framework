#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Part of the MIB export tools for the FSFW project by
"""
from fsfwgen.core import get_console_logger
from fsfwgen.utility.file_management import copy_file
from fsfwgen.parserbase.file_list_parser import FileListParser
from fsfwgen.returnvalues.returnvalues_parser import InterfaceParser, ReturnValueParser
from fsfwgen.utility.sql_writer import SqlWriter
from fsfwgen.utility.printer import PrettyPrinter

from definitions import BSP_HOSTED, DATABASE_NAME, ROOT_DIR, OBSW_ROOT_DIR, EXAMPLE_COMMON_DIR

LOGGER = get_console_logger()
EXPORT_TO_FILE = True
COPY_CSV_FILE = True
EXPORT_TO_SQL = True
PRINT_TABLES = True


FILE_SEPARATOR = ";"
MAX_STRING_LENGTH = 32

CSV_RETVAL_FILENAME = f"{ROOT_DIR}/{BSP_HOSTED}_returnvalues.csv"
CSV_COPY_DEST = f"{OBSW_ROOT_DIR}/tmtc/config/returnvalues.csv"
ADD_LINUX_FOLDER = False
FSFW_CONFIG_ROOT = f"{BSP_HOSTED}/fsfwconfig"

INTERFACE_DEFINITION_FILES = [
    f"{OBSW_ROOT_DIR}/fsfw/src/fsfw/returnvalues/FwClassIds.h",
    f"{EXAMPLE_COMMON_DIR}/config/commonClassIds.h",
    f"{FSFW_CONFIG_ROOT}/returnvalues/classIds.h",
]
RETURNVALUE_SOURCES = [
    f"{BSP_HOSTED}/",
    f"{OBSW_ROOT_DIR}/fsfw/",
    f"{EXAMPLE_COMMON_DIR}/",
]

SQL_DELETE_RETURNVALUES_CMD = """
    DROP TABLE IF EXISTS Returnvalues
"""

SQL_CREATE_RETURNVALUES_CMD = """
    CREATE TABLE IF NOT EXISTS Returnvalues (
    id              INTEGER PRIMARY KEY,
    code            TEXT,
    name            TEXT,
    interface       TEXT,
    file            TEXT,
    description     TEXT
    )
"""

SQL_INSERT_RETURNVALUES_CMD = """
INSERT INTO Returnvalues(code,name,interface,file,description)
VALUES(?,?,?,?,?)
"""


def parse_returnvalues():
    returnvalue_table = generate_returnvalue_table()
    if EXPORT_TO_FILE:
        ReturnValueParser.export_to_file(
            CSV_RETVAL_FILENAME, returnvalue_table, FILE_SEPARATOR
        )
        if COPY_CSV_FILE:
            copy_file(
                filename=CSV_RETVAL_FILENAME,
                destination=CSV_COPY_DEST,
                delete_existing_file=True,
            )
    if EXPORT_TO_SQL:
        LOGGER.info("ReturnvalueParser: Exporting to SQL")
        sql_retval_exporter(
            returnvalue_table, db_filename=f"{ROOT_DIR}/{DATABASE_NAME}"
        )


def generate_returnvalue_table():
    """Core function to parse for the return values"""
    interface_parser = InterfaceParser(
        file_list=INTERFACE_DEFINITION_FILES, print_table=PRINT_TABLES
    )
    interfaces = interface_parser.parse_files()
    header_parser = FileListParser(RETURNVALUE_SOURCES)
    header_list = header_parser.parse_header_files(True, "Parsing header file list: ")
    returnvalue_parser = ReturnValueParser(interfaces, header_list, PRINT_TABLES)
    returnvalue_parser.obsw_root_path = OBSW_ROOT_DIR
    returnvalue_parser.set_moving_window_mode(moving_window_size=7)
    returnvalue_table = returnvalue_parser.parse_files(True)
    LOGGER.info(f"ReturnvalueParser: Found {len(returnvalue_table)} returnvalues")
    return returnvalue_table


def sql_retval_exporter(returnvalue_table, db_filename: str):
    sql_writer = SqlWriter(db_filename=db_filename)
    sql_writer.open(SQL_CREATE_RETURNVALUES_CMD)
    for entry in returnvalue_table.items():
        sql_writer.write_entries(
            SQL_INSERT_RETURNVALUES_CMD,
            (entry[0], entry[1][2], entry[1][4], entry[1][3], entry[1][1]),
        )
    sql_writer.commit()
    sql_writer.close()
