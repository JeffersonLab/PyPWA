#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import example_python_sheet
import pytest

from PyPWA import Path, builtin_plugins
from PyPWA.initializers.configurator import options
from PyPWA.libs import components, plugin_loader
from PyPWA.libs.components import data_processor, process

ROOT = Path(__file__).parent
EXAMPLE_SHEET = ROOT / "example_python_sheet.py"
DOES_NOT_EXIST = ROOT / "awfulness.py"
BLANK = Path()


@pytest.fixture(scope="module")
def plugin_loader_with_plugins():
    loader = plugin_loader.PluginLoader()
    loader.add_plugin_location([builtin_plugins, components, None])
    return loader.get_by_class(options.Component)


def check_template_is_in_list(template, plugin_list):
    found = False
    for plugin in plugin_list:
        if isinstance(plugin, template):
            found = True
            break
    assert found


def test_plugin_loader_with_sets():
    loader = plugin_loader.PluginLoader()
    loader.add_plugin_location({builtin_plugins})


def test_data_parser_is_found(plugin_loader_with_plugins):
    check_template_is_in_list(
        data_processor.DataConf, plugin_loader_with_plugins
    )

def test_processing_is_found(plugin_loader_with_plugins):
    check_template_is_in_list(process.Processing, plugin_loader_with_plugins)


@pytest.mark.xfail(
    reason="File isn't included in search path, no support for non modules",
)
def test_options_test_is_found(plugin_loader_with_plugins):
    assert example_python_sheet.OptionsTest in plugin_loader_with_plugins


@pytest.fixture(scope="module")
def python_sheet_loader():
    loader = plugin_loader.PluginLoader()
    loader.add_plugin_location(EXAMPLE_SHEET)
    return loader


def test_finds_meaning(python_sheet_loader):
    fun = python_sheet_loader.get_by_name("the_meaning_of_life")
    assert fun() == 42


def test_cant_find_nothing(python_sheet_loader):
    with pytest.raises(ImportError):
        fun = python_sheet_loader.get_by_name("nothing")


def test_can_load_non_existent_file():
    with pytest.raises(ImportError):
        loader = plugin_loader.PluginLoader()
        loader.add_plugin_location(DOES_NOT_EXIST)


def test_can_ignore_blank_path():
    loader = plugin_loader.PluginLoader()
    loader.add_plugin_location(BLANK)
