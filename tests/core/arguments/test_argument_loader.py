import os

import pytest

from PyPWA.builtin_plugins import data
from PyPWA.core.arguments import _loader
from PyPWA.shell import blank

PLUGIN_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../data/source_files"
)


@pytest.fixture("module")
def loader():
    argument_loader = _loader.RequestedFetcher()
    return argument_loader


def test_loader_can_find_data_parser(loader):
    plugin = loader.get_plugin_by_name("Builtin Parser")
    assert isinstance(plugin, data.ArgDataParse)
    assert plugin.get_name() == "Builtin Parser"


def test_loader_can_find_blank_module(loader):
    main = loader.get_plugin_by_name("blank shell module")
    assert isinstance(main, blank.BlankArguments)
    assert main.get_name() == "blank shell module"


def test_loader_raises_error_with_unknown(loader):
    with pytest.raises(ValueError):
        loader.get_plugin_by_name("TacoSauce")
