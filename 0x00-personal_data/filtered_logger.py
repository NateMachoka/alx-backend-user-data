#!/usr/bin/env python3
"""
Module that provides functions for filtering log data.
"""

import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscates specific fields in a log message.
    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): The original log message.
        separator (str): The character used to separate fields in the message.
    Returns:
        str: The obfuscated log message.
    """
    pattern = '|'.join([f"{field}=[^;]*" for field in fields])
    return re.sub(
        pattern, lambda x: f"{x.group().split('=')[0]}={redaction}", message)
