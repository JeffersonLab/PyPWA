import sys

import pytest

from PyPWA.builtin_plugins import process
from PyPWA.core.configurator import options
from PyPWA.core.configurator.create_config import _metadata
from PyPWA.progs.shell import simulate, fit


@pytest.fixture()
def metadata_storage():
    return _metadata.MetadataStorage()


@pytest.fixture()
def plugin_list():
    return _metadata.GetPluginList()


@pytest.fixture()
def mock_input_for_nestle(monkeypatch):
    if sys.version_info.major == 2:
        monkeypatch.setitem(__builtins__, "raw_input", lambda x: "Nestle")
    else:
        monkeypatch.setitem(__builtins__, "input", lambda x: "Nestle")


def test_metadata_storage_finds_builtin_parser(metadata_storage):
    plugin = metadata_storage.search_plugin(
        "Builtin Parser", options.Types.DATA_PARSER
    )
    assert isinstance(plugin, options.Plugin)


def test_metadata_storage_finds_optimizers(metadata_storage):
    object = metadata_storage.request_plugins_by_type(
        options.Types.OPTIMIZER
    )
    assert len(object) == 2


def check_plugin_in_list(template, plugin_list):
    found = False
    for plugin in plugin_list:
        if isinstance(plugin, template):
            found = True
            break
    assert found


def test_plugin_list_finds_pysimulate_plugins(plugin_list):
    plugin_list.parse_plugins(simulate.ShellSimulation)
    assert plugin_list.program == simulate.ShellSimulation
    check_plugin_in_list(process.Processing, plugin_list.plugins)


def test_plugin_list_finds_pyfit_plugins(plugin_list, mock_input_for_nestle):
    plugin_list.parse_plugins(fit.ShellFitting)
    assert plugin_list.program == fit.ShellFitting
    check_plugin_in_list(process.Processing, plugin_list.plugins)
