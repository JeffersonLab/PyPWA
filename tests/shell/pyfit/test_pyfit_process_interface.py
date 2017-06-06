import pytest

import logging
import time

from PyPWA.shell.pyfit import _process_interface


@pytest.fixture()
def override_logging_effective_level(monkeypatch):
    # Output is disabled if level is greater than warning.
    monkeypatch.setattr(
        logging.getLogger(), "isEnabledFor", lambda x: False
    )


@pytest.fixture()
def output_thread(override_logging_effective_level):
    return _process_interface._ThreadInterface()


def test_small_output(output_thread):
    output_thread.start(None)
    time.sleep(2)
    output_thread.stop()


def test_full_output(output_thread):
    output_thread.start(1.2233)
    time.sleep(2)
    output_thread.stop()
