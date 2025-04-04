"""
@file Logger.py
@brief Contains the Logger class for universal colored logging configuration.
"""

import sys
import logging


class PrettyLogger:
    """
    @class PrettyLogger
    @brief A logger class that provides pretty-printed and colored logging output.

    This class configures a logger with a specific format and outputs logs to the standard output.
    It is designed to enhance the readability of log messages by including timestamps and log levels.
    """

    def __init__(self, name):
        """
        @brief Constructs a new PrettyLogger object.

        Initializes the logger with the specified name, sets the log level to INFO,
        and configures the log output format.

        @param name The name of the logger.
        """
        self.logger = logging.getLogger(name)
        self.formatter = logging.Formatter('(%(asctime)s) [%(levelname)s] %(message)s')
        self.logger.setLevel(logging.INFO)

        # Add a stream handler to output logs to the console
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)
