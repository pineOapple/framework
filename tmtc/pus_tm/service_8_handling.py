from typing import Tuple


def custom_service_8_handling(
        object_id: int, action_id: int, custom_data: bytearray) -> Tuple[list, list]:
    """
    This function is called by the TMTC core if a Service 8 data reply (subservice 130)
    is received. The user can return a tuple of two lists, where the first list
    is a list of header strings to print and the second list is a list of values to print.
    The TMTC core will take care of printing both lists and logging them.

    @param object_id:
    @param action_id:
    @param custom_data:
    @return:
    """
    header_list = []
    content_list = []
    return header_list, content_list
