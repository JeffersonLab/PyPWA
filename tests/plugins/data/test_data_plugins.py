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
from PyPWA.plugins.data import gamp, kv, numpy, sv
from PyPWA.libs.components.data_processor import data_templates, DataType
import numpy as npy

ROOT = Path(__file__).parent
TEMP_WRITE_LOCATION = ROOT / "../../test_data/docs/temporary_write_data"
CSV_TEST_DATA = ROOT / "../../test_data/docs/sv_test_data.csv"
GAMP_TEST_DATA = ROOT / "../../test_data/docs/gamp_test_data.gamp"
EVIL_TEST_DATA = ROOT / "../../test_data/docs/kv_test_data.txt"
NUMPY_TEST_DATA = ROOT / "../../test_data/docs/numpy_test_data.npy"


@pytest.fixture(
    scope="module",
    params=[
        [sv.SvDataPlugin, CSV_TEST_DATA],
        [kv.EVILDataPlugin, EVIL_TEST_DATA],
        [gamp.GampDataPlugin, GAMP_TEST_DATA],
        [numpy.NumpyDataPlugin, NUMPY_TEST_DATA]
    ]
)
def get_plugin(request):
    yield lambda b: request.param[0]() if b else request.param[1]

    NPY = str(TEMP_WRITE_LOCATION.parent) + "/temporary_write_data.npy"
    if TEMP_WRITE_LOCATION.is_file():
        TEMP_WRITE_LOCATION.unlink()
    elif Path(NPY).is_file():
        Path(NPY).unlink()


def test_plugin_name_is_string(get_plugin):
    assert isinstance(get_plugin(1).plugin_name, str)


def test_get_memory_parser_returns_parser(get_plugin):
    assert isinstance(
        get_plugin(1).get_memory_parser(),
        data_templates.Memory
    )


def test_supported_extensions_is_list_of_str(get_plugin):
    for extension in get_plugin(1).supported_extensions:
        assert isinstance(extension, str)


def test_supports_columned_data_is_bool(get_plugin):
    for data_type in get_plugin(1).supported_data_types:
        assert isinstance(data_type, DataType)


def test_get_plugin_reader_returns_reader(get_plugin):
    plugin = get_plugin(1)
    file_location = get_plugin(0)

    with plugin.get_reader(file_location, npy.float64) as reader:
        assert isinstance(reader, data_templates.Reader)


def test_get_plugin_writer_returns_writer(get_plugin):
    plugin = get_plugin(1)

    with plugin.get_writer(TEMP_WRITE_LOCATION) as writer:
        assert isinstance(writer, data_templates.Writer)
