import pytest
from PyPWA.core.configurator import options
from PyPWA.core.shared import plugin_loader
from PyPWA import builtin_plugins
from PyPWA.core import configurator


def load_plugins():
    loader = plugin_loader.PluginLoader()
    loader.add_plugin_location([builtin_plugins, configurator])
    return loader.get_by_class(options.Plugin)


@pytest.fixture(params=load_plugins())
def iterate_over_plugins(request):
    return request.param


def check_dict(the_dict):
    assert isinstance(the_dict, dict)


def check_str(string):
    assert isinstance(string, str)
    assert string is not ""


def test_plugin_name(iterate_over_plugins):
    check_str(iterate_over_plugins.plugin_name)


def test_default_options(iterate_over_plugins):
    check_dict(iterate_over_plugins.option_difficulties)


def test_option_types(iterate_over_plugins):
    check_dict(iterate_over_plugins.option_types)


def test_module_comment(iterate_over_plugins):
    check_str(iterate_over_plugins.module_comment)


def test_option_comments(iterate_over_plugins):
    check_dict(iterate_over_plugins.option_comments)


def test_setup(iterate_over_plugins):
    assert issubclass(iterate_over_plugins.setup, options.Setup)


def test_provides(iterate_over_plugins):
    assert iterate_over_plugins.provides in options.Types
