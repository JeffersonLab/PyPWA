import pytest

from PyPWA.core.configurator import options
from PyPWA.core.configurator import option_tools


NO_OPTIONS = option_tools.CommandOptions({})
MIN_OPTIONS = option_tools.CommandOptions({"Option 1": 123})


@pytest.fixture
def plugin_name_conversion():
    return option_tools.PluginNameConversion()


def test_conversion_can_get_enum(plugin_name_conversion):
    plugin_type = plugin_name_conversion.external_to_internal("Data Parsing")
    assert plugin_type == options.Types.DATA_PARSER


def test_conversion_can_get_name(plugin_name_conversion):
    plugin_name = plugin_name_conversion.internal_to_external(
        options.Types.KERNEL_PROCESSING
    )

    assert plugin_name == "Kernel Processor"


