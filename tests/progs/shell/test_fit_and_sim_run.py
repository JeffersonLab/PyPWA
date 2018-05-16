import sys

import pytest

from PyPWA import Path
from PyPWA.entries import configurator

ROOT = Path(__file__).parent
FIT_CONFIG_LOCATION = ROOT / "../../test_data/docs/program_data/rho/RHOfit"
INT_CONFIG_LOCATION = ROOT / "../../test_data/docs/program_data/rho/RHOint"
WEG_CONFIG_LOCATION = ROOT / "../../test_data/docs/program_data/rho/RHOweg.json"
SIM_CONFIG_LOCATION = ROOT / "../../test_data/docs/program_data/rho/RHOsim"


@pytest.fixture()
def patch_logging(monkeypatch):
    monkeypatch.setattr(
        "PyPWA.libs.initial_logging.setup_logging",
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
    monkeypatch.setattr("sys.argv", ["PyFit", str(FIT_CONFIG_LOCATION)])
    yield
    npy = Path("outputRHOFIT.npy")
    txt = Path("outputRHOFIT.txt")
    npy.unlink() if npy.exists() else None
    txt.unlink() if txt.exists() else None


def test_full_fit_run(fit_args):
    configurator.py_fit()

"""
PySimulate Tests
"""

@pytest.fixture()
def simulate_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr("sys.argv", ["PySimulate", str(SIM_CONFIG_LOCATION)])
    yield
    rejection = Path("outputRHO_rejection.pf")
    rejection.unlink() if rejection.exists() else None


def test_full_sim_run(simulate_args):
    configurator.py_simulate()

"""
GenerateIntensities Tests
"""

@pytest.fixture()
def intensities_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr(
        "sys.argv", ["GenerateIntensities", str(INT_CONFIG_LOCATION)]
    )
    yield
    intensities = Path('outputINT_intensities.txt')
    max = Path("outputINT_max.txt")

    intensities.unlink() if intensities.exists() else None
    max.unlink() if max.exists() else None


def test_full_int_run(intensities_args):
    configurator.generate_intensities()


"""
GenerateIntensities Tests
"""

@pytest.fixture()
def weights_args(monkeypatch, patch_sys_argv):
    monkeypatch.setattr(
        "sys.argv", ["GenerateWeights", str(WEG_CONFIG_LOCATION)]
    )
    yield
    rejection = Path("output_rejection.pf")
    rejection.unlink() if rejection.exists() else None


def test_full_weight_run(weights_args):
    configurator.generate_weights()
