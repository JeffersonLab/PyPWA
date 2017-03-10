import pytest
import enum

from PyPWA.core.configurator import options


@pytest.fixture
def setup():
    return options.Setup()


def test_types_is_enum():
    assert issubclass(options.Types, enum.Enum)


def test_levels_is_enum():
    assert issubclass(options.Levels, enum.Enum)


def test_setup_return_interface_not_implemented(setup):
    with pytest.raises(NotImplementedError):
        setup.return_interface()
