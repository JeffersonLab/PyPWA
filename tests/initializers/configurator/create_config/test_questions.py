import sys

import pytest


from PyPWA.initializers.configurator.create_config import _questions
from PyPWA.initializers.configurator import options


@pytest.fixture(params=["required", "optional", "advanced"])
def input_options(monkeypatch, request):
    mocked_input = lambda x: request.param
    if sys.version_info.major == 2:
        monkeypatch.setitem(__builtins__, "raw_input", mocked_input)
    else:
        monkeypatch.setitem(__builtins__, "input", mocked_input)
    yield request.param


@pytest.fixture()
def get_plugin_level():
    return _questions.GetPluginLevel()


def test_get_plugin_level(input_options, get_plugin_level):
    get_plugin_level.ask_for_plugin_level()
    if input_options == "required":
        assert get_plugin_level.get_plugin_level() == options.Levels.REQUIRED
    elif input_options == "optional":
        assert get_plugin_level.get_plugin_level() == options.Levels.OPTIONAL
    else:
        assert get_plugin_level.get_plugin_level() == options.Levels.ADVANCED


@pytest.fixture()
def input_location(monkeypatch):
    if sys.version_info.major == 2:
        monkeypatch.setitem(__builtins__, "raw_input", lambda x: "xhere")
    else:
        monkeypatch.setitem(__builtins__, "input", lambda x: "xhere")


@pytest.fixture()
def plugin_directory():
    return _questions.GetPluginDirectory()


def test_plugin_directory(input_location, plugin_directory):
    plugin_directory.ask_for_plugin_directory()
    assert plugin_directory.get_plugin_directory() == "xhere"


@pytest.fixture()
def save_location():
    return _questions.GetSaveLocation()


def test_save_location_from_input(save_location, input_location):
    save_location.ask_for_save_location()
    assert save_location.get_save_location() == "xhere"


def test_save_location_from_override(save_location):
    save_location.override_save_location("elsewhere")
    assert save_location.get_save_location() == "elsewhere"



