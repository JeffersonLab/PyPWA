import os

import pytest

from PyPWA import builtin_plugins
from PyPWA.builtin_plugins import data, process, minuit, nestle
from PyPWA.core import plugin_loader
from PyPWA.core.templates import option_templates

EXAMPLE_SHEET = os.path.join(
    os.path.dirname(__file__), "example_python_sheet.py"
)

DOES_NOT_EXIST = os.path.join(
    os.path.dirname(__file__), "awfulness.py"
)

@pytest.fixture(scope="module")
def plugin_loader_with_plugins():
    loader = plugin_loader.PluginLoading(
        option_templates.PluginsOptionsTemplate
    )
    return loader.fetch_plugin([builtin_plugins])


def test_data_iterator_is_found(plugin_loader_with_plugins):
    assert data.DataIterator in plugin_loader_with_plugins


def test_data_parser_is_found(plugin_loader_with_plugins):
    assert data.DataParser in plugin_loader_with_plugins


def test_processing_is_found(plugin_loader_with_plugins):
    assert process.Processing in plugin_loader_with_plugins


def test_minuit_is_found(plugin_loader_with_plugins):
    assert minuit.MinuitOptions in plugin_loader_with_plugins


def test_nestle_is_found(plugin_loader_with_plugins):
    assert nestle.NestleOptions in plugin_loader_with_plugins


@pytest.fixture(scope="module")
def python_sheet_loader():
    loader = plugin_loader.PythonSheetLoader(EXAMPLE_SHEET)
    return loader


def test_finds_meaning(python_sheet_loader):
    fun = python_sheet_loader.fetch_function("the_meaning_of_life")
    assert fun() == 42


def test_finds_internet(python_sheet_loader):
    fun = python_sheet_loader.fetch_function("what_is_the_internet_ran_by")
    assert fun() == "cats"


def test_finds_console(python_sheet_loader):
    fun = python_sheet_loader.fetch_function("the_best_gaming_console")
    assert fun("microsoft") == "linux"
    assert fun() == "sony"


def test_cant_find_nothing(python_sheet_loader):
    with pytest.raises(AttributeError):
        fun = python_sheet_loader.fetch_function("nothing", True)


def test_returns_empty(python_sheet_loader):
    fun = python_sheet_loader.fetch_function("nothing", False)
    assert isinstance(fun(), type(None))


def test_can_load_non_existant_file():
    with pytest.raises(ImportError):
        loader = plugin_loader.PythonSheetLoader(DOES_NOT_EXIST)