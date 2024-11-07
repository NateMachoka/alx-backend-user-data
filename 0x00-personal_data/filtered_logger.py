#!/usr/bin/env python3
"""
Module for logging with data redaction and PII filtering.
"""

import logging
from typing import List, Tuple
import re

# Define PII fields
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


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


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class to filter sensitive info in log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with specific fields to redact.

        Args:
            fields (List[str]): List of field names to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record to redact specified fields.
        Args:
            record (logging.LogRecord): The log record to format.
        Returns:
            str: The formatted and redacted log message.
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates a logger for user data with sensitive information redacted.

    Returns:
        logging.Logger: Configured logger with a redacting formatter.
    """
    # Create logger
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Set up stream handler with redacting formatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger
