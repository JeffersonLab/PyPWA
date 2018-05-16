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

import pytest

from PyPWA import Path
from PyPWA.builtin_plugins import sv, kv, gamp, numpy
from PyPWA.libs.components.data_processor import data_templates

ROOT = Path(__file__).parent
TEMP_WRITE_LOCATION = ROOT / "../test_data/docs/temporary_write_data"
CSV_TEST_DATA = ROOT / "../test_data/docs/sv_test_data.csv"
GAMP_TEST_DATA = ROOT / "../test_data/docs/gamp_test_data.gamp"
EVIL_TEST_DATA = ROOT / "../test_data/docs/kv_test_data.txt"
NUMPY_TEST_DATA = ROOT / "../test_data/docs/numpy_test_data.npy"


@pytest.fixture(
    scope="module",
    params=[
        [sv.SvDataPlugin, CSV_TEST_DATA],
        [kv.EVILDataPlugin, EVIL_TEST_DATA],
        [gamp.GampDataPlugin, GAMP_TEST_DATA],
        [numpy.NumpyDataPlugin, NUMPY_TEST_DATA]
    ]
)
def setup_plugin_object(request):
    yield [request.param[0](), request.param[1]]

    if TEMP_WRITE_LOCATION.is_file():
        TEMP_WRITE_LOCATION.unlink()


def test_plugin_name_is_string(setup_plugin_object):
    """
    Args:
        setup_plugin_object (list[data_templates.TemplateDataPlugin, str])
    """
    assert isinstance(setup_plugin_object[0].plugin_name, str)


def test_get_memory_parser_returns_parser(setup_plugin_object):
    """
    Args:
        setup_plugin_object (list[data_templates.TemplateDataPlugin, str])
    """
    assert isinstance(
        setup_plugin_object[0].get_plugin_memory_parser(),
        data_templates.Memory
    )


def test_supported_extensions_is_list_of_str(setup_plugin_object):
    """
    Args:
        setup_plugin_object (list[data_templates.TemplateDataPlugin, str])
    """
    for extension in setup_plugin_object[0].plugin_supported_extensions:
        assert isinstance(extension, str)


def test_supports_columned_data_is_bool(setup_plugin_object):
    """
    Args:
        setup_plugin_object (list[data_templates.TemplateDataPlugin, str])
    """
    assert isinstance(
        setup_plugin_object[0].plugin_supports_columned_data, bool
    )


def test_supports_single_array_is_bool(setup_plugin_object):
    """
    Args:
        setup_plugin_object (list[data_templates.TemplateDataPlugin, str])
    """
    assert isinstance(
        setup_plugin_object[0].plugin_supports_single_array, bool
    )


def test_supports_gamp_is_bool(setup_plugin_object):
    """
    Args:
        setup_plugin_object (list[data_templates.TemplateDataPlugin, str])
    """
    assert isinstance(setup_plugin_object[0].plugin_supports_tree_data, bool)


def test_get_plugin_reader_returns_reader(setup_plugin_object):
    """
    Args:
        setup_plugin_object (list[data_templates.TemplateDataPlugin, str])
    """
    assert isinstance(
        setup_plugin_object[0].get_plugin_reader(setup_plugin_object[1]),
        data_templates.Reader
    )


def test_get_plugin_writer_returns_writer(setup_plugin_object):
    """
    Args:
        setup_plugin_object (list[data_templates.TemplateDataPlugin, str])
    """
    assert isinstance(
        setup_plugin_object[0].get_plugin_writer(TEMP_WRITE_LOCATION),
        data_templates.Writer
    )
