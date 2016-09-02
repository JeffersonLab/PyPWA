import logging

import PyPWA.configurator.initial_logging


def test_InitialLogging_SetDebug():
    """
    Extremely simple test for the initial logging
    """
    PyPWA.configurator.initial_logging.define_logger(logging.DEBUG)
