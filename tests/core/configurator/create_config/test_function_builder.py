import os

import pytest

from PyPWA.shell import pysimulate

from PyPWA.core.configurator.create_config import _function_builder
from PyPWA.core.configurator.create_config import _metadata


@pytest.fixture()
def function_handler():
    return _function_builder.FunctionHandler()


@pytest.fixture()
def plugin_list():
    plugins = _metadata.GetPluginList()
    plugins.parse_plugins(pysimulate.ShellSimulation)
    return plugins


def test_function_builder(function_handler, plugin_list):
    function_handler.output_functions(plugin_list, "test_functions")
    os.remove("test_functions.py")
