import os

import example_python_sheet
import pytest

from PyPWA import builtin_plugins
from PyPWA.builtin_plugins import data, process, minuit, nestle
from PyPWA.core.shared import plugin_loader
from PyPWA.core.configurator import options

EXAMPLE_SHEET = os.path.join(
    os.path.dirname(__file__), "example_python_sheet.py"
)

DOES_NOT_EXIST = os.path.join(
    os.path.dirname(__file__), "awfulness.py"
)


@pytest.fixture(scope="module")
def plugin_loader_with_plugins():
    loader = plugin_loader.PluginStorage()
    loader.add_plugin_location([builtin_plugins])
    return loader.get_by_class(options.Plugin)


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


@pytest.mark.xfail(
    reason="File isn't included in search path, no support for non modules",
)
def test_options_test_is_found(plugin_loader_with_plugins):
    assert example_python_sheet.OptionsTest in plugin_loader_with_plugins


@pytest.fixture(scope="module")
def python_sheet_loader():
    loader = plugin_loader.PluginStorage()
    loader.add_plugin_location(EXAMPLE_SHEET)
    return loader


def test_finds_meaning(python_sheet_loader):
    fun = python_sheet_loader.get_by_name("the_meaning_of_life")
    assert fun() == 42


def test_cant_find_nothing(python_sheet_loader):
    with pytest.raises(ImportError):
        fun = python_sheet_loader.get_by_name("nothing", True)


def test_returns_empty(python_sheet_loader):
    fun = python_sheet_loader.get_by_name("nothing", False)
    assert isinstance(fun(), type(None))


def test_can_load_non_existant_file():
    with pytest.raises(ImportError):
        loader = plugin_loader.PluginStorage()
        loader.add_plugin_location(DOES_NOT_EXIST)
