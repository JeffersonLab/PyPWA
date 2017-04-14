import pytest

import os
from PyPWA.core.configurator.execute import _settings


CONFIGURATION_FILE = os.path.join(
    os.path.dirname(__file__), "configuration.yml"
)

OVERRIDE = {
        "main": "shell fitting method",
        "main name": "General Fitting",
        "extras": None
    }


@pytest.fixture
def setup():
    setup_object = _settings.Setup()
    setup_object.load_settings(OVERRIDE, CONFIGURATION_FILE)
    return setup_object

@pytest.fixture
def ids(setup):
    return setup.plugin_ids


@pytest.fixture
def settings(setup):
    return setup.loaded_settings


def test_names_are_in_ids(ids):
    names = [
        "Builtin Parser",
        "Builtin Multiprocessing",
        "Minuit",
        "shell fitting method"
    ]

    for name in names:
        assert name in ids


def test_general_fitting_none_settings(settings):
    assert isinstance(
        settings["shell fitting method"]['generated length'], type(None)
    )

    assert isinstance(
        settings["shell fitting method"]['qfactor location'], type(None)
    )

    assert isinstance(
        settings["shell fitting method"]['accepted monte carlo location'],
        type(None)
    )


def test_general_fitting_presets(settings):
    assert settings["shell fitting method"]['likelihood type'] == \
           "chi-squared"


def test_parser_boolean(settings):
    assert isinstance(settings["Builtin Parser"]["enable cache"], bool)
    assert settings["Builtin Parser"]["enable cache"]


def test_minuit_list(settings):
    list_items = ['O1', 'O2', 'O3', 'O4', 'O5']
    for item in list_items:
        assert item in settings["Minuit"]["parameters"]


def test_minuit_settings(settings):
    assert settings["Minuit"]["settings"]['limit_O5'] == [-15., 10.]











