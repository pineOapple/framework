"""Part of the Mission Information Base Exporter for the SOURCE project by KSat.
Object exporter.
"""
import datetime
import os

from fsfwgen.core import get_console_logger
from fsfwgen.objects.objects import (
    sql_object_exporter,
    ObjectDefinitionParser,
    write_translation_file,
    export_object_file,
    write_translation_header_file,
)
from fsfwgen.utility.printer import PrettyPrinter
from fsfwgen.utility.file_management import copy_file

from definitions import (
    BSP_HOSTED,
    DATABASE_NAME,
    OBSW_ROOT_DIR,
    ROOT_DIR,
    EXAMPLE_COMMON_DIR,
)

LOGGER = get_console_logger()
DATE_TODAY = datetime.datetime.now()
DATE_STRING_FULL = DATE_TODAY.strftime("%Y-%m-%d %H:%M:%S")

GENERATE_CSV = True
MOVE_CSV = True

GENERATE_CPP = True
COPY_CPP = True

GENERATE_HEADER = True

FSFW_CONFIG_ROOT = f"{BSP_HOSTED}/fsfwconfig"

EXPORT_TO_SQL = True

CPP_COPY_DESTINATION = f"{FSFW_CONFIG_ROOT}/objects/"
CPP_FILENAME = f"{os.path.dirname(os.path.realpath(__file__))}//translateObjects.cpp"
CPP_H_FILENAME = f"{os.path.dirname(os.path.realpath(__file__))}//translateObjects.h"
CSV_OBJECT_FILENAME = f"{ROOT_DIR}/{BSP_HOSTED}_objects.csv"
CSV_COPY_DEST = f"{OBSW_ROOT_DIR}/tmtc/config/objects.csv"
FILE_SEPARATOR = ";"


OBJECTS_PATH = f"{FSFW_CONFIG_ROOT}/objects/systemObjectList.h"
FRAMEWORK_OBJECT_PATH = (
    f"{OBSW_ROOT_DIR}/fsfw/src/fsfw/objectmanager/frameworkObjects.h"
)
COMMON_OBJECTS_PATH = f"{EXAMPLE_COMMON_DIR}/config/commonObjects.h"
OBJECTS_DEFINITIONS = [OBJECTS_PATH, FRAMEWORK_OBJECT_PATH, COMMON_OBJECTS_PATH]

SQL_DELETE_OBJECTS_CMD = """
    DROP TABLE IF EXISTS Objects
    """

SQL_CREATE_OBJECTS_CMD = """
    CREATE TABLE IF NOT EXISTS Objects(
    id              INTEGER PRIMARY KEY,
    objectid        TEXT,
    name            TEXT
    )
    """

SQL_INSERT_INTO_OBJECTS_CMD = """
INSERT INTO Objects(objectid, name)
VALUES(?,?)
"""


def parse_objects(print_object_list: bool = True):
    # fetch objects
    object_parser = ObjectDefinitionParser(OBJECTS_DEFINITIONS)
    subsystem_definitions = object_parser.parse_files()
    # id_subsystem_definitions.update(framework_subsystem_definitions)
    list_items = sorted(subsystem_definitions.items())
    LOGGER.info(f"ObjectParser: Number of objects: {len(list_items)}")

    if print_object_list:
        PrettyPrinter.pprint(list_items)

    handle_file_export(list_items)
    if EXPORT_TO_SQL:
        LOGGER.info("ObjectParser: Exporting to SQL")
        sql_object_exporter(
            object_table=list_items,
            delete_cmd=SQL_DELETE_OBJECTS_CMD,
            insert_cmd=SQL_INSERT_INTO_OBJECTS_CMD,
            create_cmd=SQL_CREATE_OBJECTS_CMD,
            db_filename=f"{ROOT_DIR}/{DATABASE_NAME}",
        )


def handle_file_export(list_items):
    if GENERATE_CPP:
        LOGGER.info("ObjectParser: Generating C++ translation file")
        write_translation_file(
            filename=CPP_FILENAME,
            list_of_entries=list_items,
            date_string_full=DATE_STRING_FULL,
        )
        if COPY_CPP:
            LOGGER.info("ObjectParser: Copying object file to " + CPP_COPY_DESTINATION)
            copy_file(CPP_FILENAME, CPP_COPY_DESTINATION)
    if GENERATE_HEADER:
        write_translation_header_file(filename=CPP_H_FILENAME)
        copy_file(filename=CPP_H_FILENAME, destination=CPP_COPY_DESTINATION)
    if GENERATE_CSV:
        LOGGER.info("ObjectParser: Generating text export")
        export_object_file(
            filename=CSV_OBJECT_FILENAME,
            object_list=list_items,
            file_separator=FILE_SEPARATOR,
        )
        copy_file(
            filename=CSV_OBJECT_FILENAME,
            destination=CSV_COPY_DEST,
            delete_existing_file=True,
        )
