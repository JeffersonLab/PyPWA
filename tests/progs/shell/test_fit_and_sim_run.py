import os
import sys

import pytest

from PyPWA.entries import configurator

FIT_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../data/shell/rho/RHOfit"
)

INT_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../data/shell/rho/RHOint"
)

WEG_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../data/shell/rho/RHOweg.json"
)

SIM_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../data/shell/rho/RHOsim"
)


@pytest.fixture()
def patch_logging(monkeypatch):
    monkeypatch.setattr(
        "PyPWA.core.shared.initial_logging.setup_logging",
        lambda count, file=None: None
    )

@pytest.fixture()
def patch_sys_argv(monkeypatch, patch_logging):
    holding = sys.argv
    yield
    monkeypatch.setattr('sys.argv', holding)

"""
PyFit Tests
"""

@pytest.fixture()
def fit_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr("sys.argv", ["PyFit", FIT_CONFIG_LOCATION])
    yield
    os.remove("outputRHOFIT.npy")
    os.remove("outputRHOFIT.txt")


def test_full_fit_run(fit_args):
    configurator.py_fit()

"""
PySimulate Tests
"""

@pytest.fixture()
def simulate_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr("sys.argv", ["PySimulate", SIM_CONFIG_LOCATION])
    yield
    os.remove("outputRHO_rejection.pf")


def test_full_sim_run(simulate_args):
    configurator.py_simulate()

"""
GenerateIntensities Tests
"""

@pytest.fixture()
def intensities_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr(
        "sys.argv", ["GenerateIntensities", INT_CONFIG_LOCATION]
    )
    yield
    os.remove('outputINT_intensities.txt')
    os.remove('outputINT_max.txt')


def test_full_int_run(intensities_args):
    configurator.generate_intensities()


"""
GenerateIntensities Tests
"""

@pytest.fixture()
def weights_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr(
        "sys.argv", ["GenerateWeights", WEG_CONFIG_LOCATION]
    )
    yield
    os.remove("output_rejection.pf")


def test_full_weight_run(weights_args):
    configurator.generate_weights()
