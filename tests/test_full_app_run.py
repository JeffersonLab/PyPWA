import os

from PyPWA.core.configurator.execute import start

FIT_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "data/shell/rho/RHOfit"
)


SIM_CONFIG_LOCATION = os.path.join(
    os.path.dirname(__file__), "data/shell/rho/RHOsim"
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


def test_full_pyfit_run():
    executor = start.Execute()
    executor.run(PYFIT_CONFIG, FIT_CONFIG_LOCATION)
    os.remove("outputRHOFIT.npy")
    os.remove("outputRHOFIT.txt")


def test_full_pysim_run():
    executor = start.Execute()
    executor.run(PYSIM_CONFIG, SIM_CONFIG_LOCATION)
    os.remove("outputRHO_rejection.txt")
