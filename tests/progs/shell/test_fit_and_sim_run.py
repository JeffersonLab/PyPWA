import os
import sys

import pytest

from PyPWA.entries import configurator

FIT_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "data/shell/rho/RHOfit"
)


SIM_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "data/shell/rho/RHOsim"
)


@pytest.fixture()
def patch_sys_argv(monkeypatch):
    holding = sys.argv
    yield
    monkeypatch.setattr('sys.argv', holding)


@pytest.fixture()
def fit_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr("sys.argv", ["PyFit", FIT_CONFIG_LOCATION])
    yield
    os.remove("outputRHOFIT.npy")
    os.remove("outputRHOFIT.txt")


def test_full_fit_run(fit_args):
    configurator.py_fit()


@pytest.fixture()
def simulate_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr("sys.argv", ["PySimulate", SIM_CONFIG_LOCATION])
    yield
    os.remove("outputRHO_rejection.txt")


def test_full_sim_run(simulate_args):
    configurator.py_simulate()
