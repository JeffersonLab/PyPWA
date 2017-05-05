import os
import logging

import pytest

from PyPWA.core.shared import initial_logging
from PyPWA.core.configurator.execute import start

FIT_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "data/pyfit/rho/RHOfit"
)


SIM_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "data/pyfit/rho/RHOsim"
)


PYFIT_CONFIG = {
    "main": "shell fitting method",
    "main name": "General Fitting",
}


PYSIM_CONFIG = {
    "main": "shell simulation",
    "main name": "Simulator",
    "main options": {
        "the type": "full",
        "max intensity": None
    }
}


@classmethod
def override_get_level(cls):
    return logging.DEBUG


@pytest.fixture()
def force_logging_off(monkeypatch):
    # PyTest breaks the internal logging mechanism, so we have to bypass it.
    monkeypatch.setattr(
        initial_logging.InternalLogger, "get_level", override_get_level
    )


def test_full_pyfit_run(force_logging_off):
    executor = start.Execute()
    executor.run(PYFIT_CONFIG, FIT_CONFIG_LOCATION)
    os.remove("outputRHOFIT.npy")
    os.remove("outputRHOFIT.txt")


def test_full_pysim_run(force_logging_off):
    executor = start.Execute()
    executor.run(PYSIM_CONFIG, SIM_CONFIG_LOCATION)
    os.remove("outputRHO_rejection.txt")
