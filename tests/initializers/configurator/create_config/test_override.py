import pytest

from PyPWA.initializers.configurator.create_config import _override


def get_config():
    # Prevent bugs from configuration changing between tests.
    return {
        "shell function name": {
            "should not be seen": 1,
            "should also not be seen": 2,
            "Perfectly Fine": 3
        }
    }

OVERRIDE_WITH_OPTIONS = {
    "main": "shell function name",
    "main name": "Shell Test",
    "main options": {
        "should not be seen": 10,
        "should also not be seen": 20
    }
}

OVERRIDE_WITHOUT_OPTIONS = {
    "main": "shell function name",
    "main name": "Shell Test"
}


@pytest.fixture()
def override():
    return _override.Override()


def test_override_with_options(override):
    override.execute(get_config(), OVERRIDE_WITH_OPTIONS)
    assert "should not be seen" not in \
        override.processed_configuration["Shell Test"]


def test_override_without_options(override):
    override.execute(get_config(), OVERRIDE_WITHOUT_OPTIONS)
    assert "should not be seen" in \
           override.processed_configuration["Shell Test"]
