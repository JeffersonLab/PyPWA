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
Simple tests written to test all the functionality and error catching
of the caching module.
"""

import os
import io
import pytest

from PyPWA.libs.components.data_processor import exceptions
from PyPWA.libs.components.data_processor.cache import _standard_cache
from PyPWA.libs.components.data_processor.cache import _basic_info


TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__),
    "../../../../data/test_docs/temporary_write_data"
)

DATA = ";qjkxbmwvzpyfgcrl"


class InfoA(_basic_info.FindBasicInfo):

    def __init__(self):
        # We don't actually want to run the init
        pass

    @property
    def file_hash(self):
        return "aoeuidhtns-1234567890"

    @property
    def cache_location(self):
        return TEMP_WRITE_LOCATION


class InfoB(_basic_info.FindBasicInfo):

    def __init__(self):
        # We don't actually want to run the init
        pass

    @property
    def file_hash(self):
        return "1234567890aoeuidhtns"

    @property
    def cache_location(self):
        return TEMP_WRITE_LOCATION


@pytest.fixture
def basic_info_a():
    return InfoA()


@pytest.fixture
def basic_info_b():
    return InfoB()


@pytest.fixture
def write_a(basic_info_a):
    return _standard_cache.WriteCache(basic_info_a)


@pytest.fixture
def read_b(basic_info_b):
    return _standard_cache.ReadCache(basic_info_b)


@pytest.fixture
def wrapping_pass_read(write_a, basic_info_a):
    write_a.write_cache(DATA)

    yield _standard_cache.ReadCache(basic_info_a)

    os.remove(TEMP_WRITE_LOCATION)


@pytest.fixture
def wrapping_fail_read(write_a, basic_info_b):
    write_a.write_cache(DATA)

    yield _standard_cache.ReadCache(basic_info_b)

    os.remove(TEMP_WRITE_LOCATION)


@pytest.fixture
def induced_pickle_error(write_a, basic_info_a):
    write_a.write_cache(DATA)

    with io.open(TEMP_WRITE_LOCATION, "wb") as stream:
        stream.write(os.urandom(10240))

    yield _standard_cache.ReadCache(basic_info_a)

    os.remove(TEMP_WRITE_LOCATION)


def test_read_is_valid_true(wrapping_pass_read):
    assert wrapping_pass_read.is_valid() is True


def test_get_cache_matches_read(wrapping_pass_read):
    assert wrapping_pass_read.get_cache() == DATA


def test_read_is_valid_false(wrapping_fail_read):
    assert not wrapping_fail_read.is_valid()


def test_get_cache_raises_error(wrapping_fail_read):
    with pytest.raises(exceptions.CacheError):
        wrapping_fail_read.get_cache()


def test_read_is_valid_false_with_bad_pickle(induced_pickle_error):
    assert not induced_pickle_error.is_valid()


def test_get_cache_raises_error_with_bad_pickle(induced_pickle_error):
    with pytest.raises(exceptions.CacheError):
        induced_pickle_error.get_cache()


def test_read_is_valid_false_with_no_cache(read_b):
    assert not read_b.is_valid()


def test_get_cache_raises_error_with_no_cache(read_b):
    with pytest.raises(exceptions.CacheError):
        read_b.get_cache()
