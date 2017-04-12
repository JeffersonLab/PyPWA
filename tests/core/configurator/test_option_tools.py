import pytest

from PyPWA.core.configurator import options
from PyPWA.core.configurator import option_tools


configuration = {
    "Option 1": 123,
    "Option 2": "A collection of words",
    "Option 3": ["Preset 2"],
    "Option 4": "ABC"
}

NO_OPTIONS = option_tools.CommandOptions(configuration, {})
MIN_OPTIONS = option_tools.CommandOptions(configuration, {"Option 1": 231})
FULL_OPTIONS = option_tools.CommandOptions(
    configuration,
    {
        "Option 1": 321,
        "Option 2": "words",
        "Option 3": ["Preset 1"],
        "Option 4": None
    }
)


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


def test_command_default_options_set():
    assert NO_OPTIONS.option_1 == 123
    assert NO_OPTIONS.option_2 == "A collection of words"
    assert NO_OPTIONS.option_3 == ["Preset 2"]
    assert NO_OPTIONS.option_4 == "ABC"


def test_command_min_options_set():
    assert MIN_OPTIONS.option_1 == 231
    assert MIN_OPTIONS.option_2 == "A collection of words"
    assert MIN_OPTIONS.option_3 == ["Preset 2"]
    assert MIN_OPTIONS.option_4 == "ABC"


def test_command_full_options_set():
    assert FULL_OPTIONS.option_1 == 321
    assert FULL_OPTIONS.option_2 == "words"
    assert FULL_OPTIONS.option_3 == ["Preset 1"]
    assert isinstance(FULL_OPTIONS.option_4, type(None))
