import pytest

from PyPWA.entries import configurator


class StartCalled(Exception):
    pass


class MockStartProgram(object):

    def start(self, configuration):
        assert "description" in configuration
        assert "main" in configuration
        assert "main name" in configuration
        assert "extras" in configuration
        if "main options" in configuration:
            assert isinstance(configuration["main options"], dict)
        raise StartCalled


@pytest.fixture()
def mock_start_program(monkeypatch):
    monkeypatch.setattr(configurator, "initializer", MockStartProgram())


def test_py_fit_entry(mock_start_program):
    with pytest.raises(StartCalled):
        configurator.py_fit()


def test_likelihood_fit_entry(mock_start_program):
    with pytest.raises(StartCalled):
        configurator.likelihood_fit()


def test_chi_squared_fit_entry(mock_start_program):
    with pytest.raises(StartCalled):
        configurator.chi_squared_fit()


def test_py_simulate_entry(mock_start_program):
    with pytest.raises(StartCalled):
        configurator.py_simulate()


def test_generate_intensities_entry(mock_start_program):
    with pytest.raises(StartCalled):
        configurator.generate_intensities()


def test_generate_weights_entry(mock_start_program):
    with pytest.raises(StartCalled):
        configurator.generate_weights()
