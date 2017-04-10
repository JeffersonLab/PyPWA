import pytest

from PyPWA.core.configurator.execute import start


function_settings = {
    "main": "blank shell module",
    "main name": "Blank Shell",
    "main options": {"Option 4": "madness"},
    "extras": None
}


config = {
    "Blank Shell": {
        "option 1": 123,
        "optn 2": "A collection of words",
        "Optional 3": "prest 2"
    },
    "Builtin Parser": {
        "Enable Cache": False
    }

}


def fake_read_config(self, config_location):
    return config


@pytest.fixture
def setup_settings(monkeypatch):
    monkeypatch.setattr(
        start.config_loader.ConfigurationLoader, "read_config",
        fake_read_config
    )

    return start.SetupSettings()


def test_full_configurator_execute_with_blank_module(setup_settings):
    setup_settings.run(function_settings, "Arbitrary file location")
