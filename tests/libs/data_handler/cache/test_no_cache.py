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
from PyPWA.libs.data_handler.cache import _no_cache
from PyPWA.libs.data_handler import exceptions


@pytest.fixture
def NoWrite():
    return _no_cache.NoWrite()


@pytest.fixture
def NoRead():
    return _no_cache.NoRead()


def test_writer_doesnt_fail(NoWrite):
    NoWrite.write_cache("123")


def test_reader_isnt_valid(NoRead):
    assert not NoRead.is_valid()


def test_reader_get_cache(NoRead):
    with pytest.raises(exceptions.CacheError):
        NoRead.get_cache()