import logging

import PyPWA.core.shared.initial_logging


def test_initial_logging_takes_a_logging_level():
    PyPWA.core.shared.initial_logging.configure_root_logger(logging.DEBUG)
