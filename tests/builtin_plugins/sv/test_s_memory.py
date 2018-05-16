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

import numpy
import pytest

from PyPWA import Path
from PyPWA.builtin_plugins.sv import s_memory

ROOT = Path(__file__).parent
TEMP_WRITE_LOCATION = ROOT / "../../test_data/docs/temporary_write_data"
CSV_TEST_DATA = ROOT / "../../test_data/docs/sv_test_data.csv"
CSV_TEST_DATA_2 = ROOT / "../../test_data/docs/program_data/data/data.csv"
TSV_TEST_DATA = ROOT / "../../test_data/docs/sv_test_data.tsv"


@pytest.fixture
def full_data():
    parser = s_memory.SvMemory()
    return parser.parse(CSV_TEST_DATA_2)


@pytest.fixture(scope="module")
def numpy_flat():
    data = numpy.zeros(30, [("x", "f8"), ("y", "f8"), ("z", "f8")])

    for column in data.dtype.names:
        data[column] = numpy.random.rand(30)

    return data


@pytest.fixture(scope="module", params=[CSV_TEST_DATA, TSV_TEST_DATA])
def return_parsed_data(request):
    parser = s_memory.SvMemory()
    return parser.parse(request.param)


@pytest.fixture(
    scope="function",
    params=[
        TEMP_WRITE_LOCATION,
        Path(TEMP_WRITE_LOCATION.stem + ".csv"),
        Path(TEMP_WRITE_LOCATION.stem + ".tsv")
    ]
)
def looping_parser_test_data(numpy_flat, request):
    parser = s_memory.SvMemory()
    parser.write(request.param, numpy_flat)
    new_data = parser.parse(request.param)

    yield [numpy_flat, new_data]

    request.param.unlink()


def test_full_data_has_expected_data(full_data):
    assert full_data['v'][3] == 0.19246017603470056


def test_read_data_matches_expected(return_parsed_data):
    """
    Args:
        return_parsed_data (numpy.ndarray)
    """
    assert return_parsed_data["ctAD"][2] == -0.265433
    assert return_parsed_data["QFactor"][0] == 0.888493


def test_read_and_write(looping_parser_test_data):
    """
    Args:
        looping_parser_test_data (list[numpy.ndarray])
    """
    numpy.testing.assert_array_equal(
        looping_parser_test_data[0], looping_parser_test_data[1]
    )
