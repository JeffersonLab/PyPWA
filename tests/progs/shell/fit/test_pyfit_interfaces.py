import pytest

from PyPWA.progs.shell.fit import interfaces


class WasCalled(Exception):
    pass


def processing():
    pass


def startup():
    raise WasCalled


@pytest.fixture
def likelihood():
    return interfaces.Likelihood(startup)


@pytest.fixture
def setup():
    return interfaces.Setup()


def test_setup_function_is_passed_to_likelihood(likelihood):
    with pytest.raises(WasCalled):
        likelihood.setup()
