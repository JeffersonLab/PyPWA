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

from PyPWA import Path, PurePath
from PyPWA.libs.components.data_processor.cache import _basic_info

DATA = Path(__file__).parent / "../../../../test_data/docs/sv_test_data.csv"

SIMPLE_STRING = "1234567890aoeuidhtns-"

FAKE_LOCATION = Path("narnia")


@pytest.fixture
def mock_hash(monkeypatch):
    def returns_string(file_name):
        return SIMPLE_STRING

    monkeypatch.setattr(
        "PyPWA.libs.misc_file_libs.get_sha512_hash",
        returns_string
    )


@pytest.fixture
def mock_cache_uri(monkeypatch):
    def returns_string():
        return FAKE_LOCATION

    monkeypatch.setattr(
        "PyPWA.libs.misc_file_libs.get_cache_uri",
        returns_string
    )


@pytest.fixture
def mocked_basic_info(mock_hash, mock_cache_uri):
    info = _basic_info.FindBasicInfo()
    info.setup_basic_info(DATA)
    return info


@pytest.fixture
def standard_basic_info():
    info = _basic_info.FindBasicInfo()
    info.setup_basic_info(DATA)
    return info


def test_basic_info_hash_is_string(standard_basic_info):
    assert isinstance(standard_basic_info.file_hash, str)


def test_basic_info_location_is_Path(standard_basic_info):
    assert isinstance(standard_basic_info.cache_location, Path)


def test_mock_basic_info_equals_simple_string(mocked_basic_info):
    assert mocked_basic_info.file_hash == SIMPLE_STRING


def test_mock_basic_info_equals_fake_location(mocked_basic_info):
    assert (
        PurePath(mocked_basic_info.cache_location) ==
        PurePath(FAKE_LOCATION  / "sv_test_data.pickle")
    )
