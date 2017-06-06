import pytest
import sys

from PyPWA.builtin_plugins import process
from PyPWA.shell import pysimulate, pyfit
from PyPWA.core.configurator import options
from PyPWA.core.configurator.create_config import _metadata


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
    object = metadata_storage.search_plugin(
        "Builtin Parser", options.Types.DATA_PARSER
    )
    assert issubclass(object, options.Plugin)


def test_metadata_storage_finds_optimizers(metadata_storage):
    object = metadata_storage.request_plugins_by_type(
        options.Types.OPTIMIZER
    )
    assert len(object) == 2


def test_plugin_list_finds_pysimulate_plugins(plugin_list):
    plugin_list.parse_plugins(pysimulate.ShellSimulation)
    assert plugin_list.shell == pysimulate.ShellSimulation
    assert process.Processing in plugin_list.plugins


def test_plugin_list_finds_pyfit_plugins(plugin_list, mock_input_for_nestle):
    plugin_list.parse_plugins(pyfit.ShellFitting)
    assert plugin_list.shell == pyfit.ShellFitting
    assert process.Processing in plugin_list.plugins
