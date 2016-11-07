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

"""
These are simple tests to make sure that when uninitialized methods are
called it will correctly raise a NotImplementedError.
"""

import pytest

from PyPWA.builtin_plugins.data import data_templates


@pytest.fixture(scope="module")
def setup_data_plugin():
    yield data_templates.TemplateDataPlugin()


@pytest.fixture(scope="module")
def setup_memory():
    yield data_templates.TemplateMemory()


@pytest.fixture(scope="module")
def setup_read_test():
    yield data_templates.ReadTest()


def test_data_plugin_name_raises_error(setup_data_plugin):
    """
    Args:
        setup_data_plugin (data_templates.TemplateDataPlugin)
    """
    with pytest.raises(NotImplementedError):
        setup_data_plugin.plugin_name


def test_data_plugin_get_plugin_parser_raises_error(setup_data_plugin):
    """
    Args:
        setup_data_plugin (data_templates.TemplateDataPlugin)
    """
    with pytest.raises(NotImplementedError):
        setup_data_plugin.get_plugin_memory_parser()


def test_data_plugin_get_plugin_reader_raises_error(setup_data_plugin):
    """
    Args:
        setup_data_plugin (data_templates.TemplateDataPlugin)
    """
    with pytest.raises(NotImplementedError):
        setup_data_plugin.get_plugin_reader("A File")


def test_data_plugin_get_plugin_writer_raises_error(setup_data_plugin):
    """
    Args:
        setup_data_plugin (data_templates.TemplateDataPlugin)
    """
    with pytest.raises(NotImplementedError):
        setup_data_plugin.get_plugin_writer("A File")


def test_data_plugin_get_plugin_read_test_raises_error(setup_data_plugin):
    """
    Args:
        setup_data_plugin (data_templates.TemplateDataPlugin)
    """
    with pytest.raises(NotImplementedError):
        setup_data_plugin.get_plugin_read_test()


def test_data_plugin_supported_extensions_raises_error(setup_data_plugin):
    """
    Args:
        setup_data_plugin (data_templates.TemplateDataPlugin)
    """
    with pytest.raises(NotImplementedError):
        setup_data_plugin.plugin_supported_extensions


def test_data_plugin_supports_flat_raises_error(setup_data_plugin):
    """
    Args:
        setup_data_plugin (data_templates.TemplateDataPlugin)
    """
    with pytest.raises(NotImplementedError):
        setup_data_plugin.plugin_supports_flat_data


def test_data_plugin_supports_gamp_raises_error(setup_data_plugin):
    """
    Args:
        setup_data_plugin (data_templates.TemplateDataPlugin)
    """
    with pytest.raises(NotImplementedError):
        setup_data_plugin.plugin_supports_gamp_data


def test_memory_parse_raises_error(setup_memory):
    """
    Args:
        setup_memory (data_templates.TemplateMemory)
    """
    with pytest.raises(NotImplementedError):
        setup_memory.parse("A File")


def test_memory_write_raises_error(setup_memory):
    """
    Args:
        setup_memory (data_templates.TemplateMemory)
    """
    with pytest.raises(NotImplementedError):
        setup_memory.write("A File", 12)


def test_read_test_quick_test_raises_error(setup_read_test):
    """
    Args:
        setup_read_test (data_templates.ReadTest)
    """
    with pytest.raises(NotImplementedError):
        setup_read_test.quick_test("A File")


def test_read_test_full_test_raises_error(setup_read_test):
    """
    Args:
        setup_read_test (data_templates.ReadTest)
    """
    with pytest.raises(NotImplementedError):
        setup_read_test.full_test("A File")
