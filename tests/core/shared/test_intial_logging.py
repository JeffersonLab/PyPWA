import logging

from PyPWA.core.shared import initial_logging


def test_initial_logging_takes_a_logging_level():
    initial_logging.InternalLogger.configure_root_logger(logging.DEBUG)
