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
from PyPWA.plugins.data.sv import s_metadata

ROOT = Path(__file__).parent
CSV_TEST_DATA = ROOT / "../../../test_data/docs/sv_test_data.csv"
TSV_TEST_DATA = ROOT / "../../../test_data/docs/sv_test_data.tsv"
NOISE_TEST_DATA = ROOT / "../../../test_data/docs/noise_test_data"
BAD_CSV_TEST_DATA = ROOT / "../../../test_data/docs/sv_test_data_bad.csv"



@pytest.fixture(scope="module")
def setup_test():
    """
    Returns:
        data_templates.ReadTest
    """
    return s_metadata._SvDataTest()


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
    assert not setup_test.can_read(tests_fails)


def test_test_passes_with_good_files(setup_test, tests_passes):
    """
    Args:
        setup_test (data_templates.ReadTest)
        tests_passes (str)
    """
    assert setup_test.can_read(tests_passes)
