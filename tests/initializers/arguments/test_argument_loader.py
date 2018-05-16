import pytest

from PyPWA.initializers.arguments import _loader
from PyPWA.libs.components import data_processor


@pytest.fixture("module")
def loader():
    argument_loader = _loader.RequestedFetcher()
    return argument_loader


def test_loader_can_find_data_parser(loader):
    plugin = loader.get_plugin_by_name("Data Processor")
    assert isinstance(plugin, data_processor.DataArg)
    assert plugin.get_name() == "Data Processor"


def test_loader_raises_error_with_unknown(loader):
    with pytest.raises(ValueError):
        loader.get_plugin_by_name("TacoSauce")
