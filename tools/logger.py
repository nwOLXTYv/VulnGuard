"""
PrettyLogger class file
    Universal colored logger config
"""

import sys
import logging


class PrettyLogger:
    """
    Pretty print class
    """

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.formatter = logging.Formatter('(%(asctime)s) [%(levelname)s] %(message)s')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
