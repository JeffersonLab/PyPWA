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

import os

import pytest
from PyPWA.libs.data_handler import exceptions
from PyPWA.builtin_plugins.sv import s_read_tests

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.csv"
)

TSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/sv_test_data.tsv"
)

BAD_CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__),
    "../../data/test_docs/sv_test_data_bad.csv"
)

NOISE_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../../data/test_docs/noise_test_data"
)


@pytest.fixture(scope="module")
def setup_test():
    """
    Returns:
        data_templates.ReadTest
    """
    return s_read_tests.SvDataTest()


@pytest.fixture(scope="module", params=[NOISE_TEST_DATA, BAD_CSV_TEST_DATA])
def tests_fails(request):
    return request.param


@pytest.fixture(scope="module", params=[CSV_TEST_DATA, TSV_TEST_DATA])
def tests_passes(request):
    return request.param


def test_test_fails_with_bad_files(setup_test, tests_fails):
    """
    Args:
        setup_test (data_templates.ReadTest)
        tests_fails (str)
    """
    with pytest.raises(exceptions.IncompatibleData):
        setup_test.test(tests_fails)


def test_test_passes_with_good_files(setup_test, tests_passes):
    """
    Args:
        setup_test (data_templates.ReadTest)
        tests_passes (str)
    """
    setup_test.test(tests_passes)
