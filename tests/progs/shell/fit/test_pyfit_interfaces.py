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


def test_process_raises_not_implemented_error(likelihood):
    with pytest.raises(NotImplementedError):
        likelihood.process("Some lovely data for a lovely process.")


def test_setup_interface_raises_not_implemented_error(setup):
    with pytest.raises(NotImplementedError):
        setup.setup_likelihood("data", "functions")


def test_get_likelihood_raises_not_implemented_error(setup):
    with pytest.raises(NotImplementedError):
        setup.setup_likelihood("data", "functions")


def test_get_data_raises_not_implemented_error(setup):
    with pytest.raises(NotImplementedError):
        setup.setup_likelihood("data", "functions")
