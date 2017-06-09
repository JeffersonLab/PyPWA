import os

import pytest

from PyPWA.core.arguments import _loader
from PyPWA.core.shared.interfaces import plugins

PLUGIN_LOCATION = os.path.join(
    os.path.dirname(__file__), "../../data/source_files"
)


@pytest.fixture("module")
def loader():
    argument_loader = _loader.RequestedFetcher()
    return argument_loader


def test_loader_can_find_data_parser(loader):
    # type: (_loader.RequestedFetcher) -> None
    plugin = loader.get_plugin_by_name("Builtin Parser")
    assert issubclass(plugin, plugins.BasePlugin)
    assert plugin.plugin_name == "Builtin Parser"


def test_loader_can_find_blank_module(loader):
    # type: (_loader.RequestedFetcher) -> None
    main = loader.get_plugin_by_name("blank shell module")
    assert issubclass(main, plugins.BasePlugin)
    assert main.plugin_name == "blank shell module"


def test_loader_raises_error_with_unknown(loader):
    # type: (_loader.RequestedFetcher) -> None
    with pytest.raises(ValueError):
        loader.get_plugin_by_name("TacoSauce")
