#!/usr/bin/env python3
import time

from objects.objects import parse_objects
from events.event_parser import parse_events
from returnvalues.returnvalues_parser import parse_returnvalues
from fsfwgen.core import (
    return_generic_args_parser,
    init_printout,
    get_console_logger,
    ParserTypes,
)


LOGGER = get_console_logger()


def main():
    init_printout(project_string="FSFW")
    parser = return_generic_args_parser()
    args = parser.parse_args()
    if args.type == "objects":
        LOGGER.info(f"Generating objects data..")
        time.sleep(0.05)
        parse_objects()
    elif args.type == "events":
        LOGGER.info(f"Generating event data")
        time.sleep(0.05)
        parse_events()
    elif args.type == "returnvalues" or args.type == "retvals":
        LOGGER.info("Generating returnvalue data")
        time.sleep(0.05)
        parse_returnvalues()
    elif args.type == "all":
        LOGGER.info("Generating all data")
        parse_objects()
        parse_events()
        # parse_returnvalues()


if __name__ == "__main__":
    main()
