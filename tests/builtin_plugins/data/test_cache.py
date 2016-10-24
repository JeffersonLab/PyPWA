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

import pytest

from PyPWA.core import tools
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data import _cache

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/temporary_write_data"
)

CACHE_DIR = tools.DataLocation().get_cache_uri()

DATA_WRITTEN = "Something that can be hashed."


@pytest.fixture(scope="module")
def setup_teardown_test_data(request):
    with open(TEMP_WRITE_LOCATION, "w") as stream:
        stream.write(DATA_WRITTEN)

    yield

    os.remove(TEMP_WRITE_LOCATION)


@pytest.fixture(scope="function")
def init_cache(request):
    cache = _cache.MemoryCache()

    yield _cache.MemoryCache()

    cache.delete_cache(TEMP_WRITE_LOCATION)


def add_extra_lines_to_file():
    with open(TEMP_WRITE_LOCATION, "w") as stream:
        stream.write(" Random extra data.")


@pytest.mark.xfail(raises=exceptions.CacheError, strict=True)
def test_read_cache_with_no_cache_present(
        setup_teardown_test_data, init_cache
):
    """
    Args:
        init_cache (_cache.MemoryCache)
    """
    init_cache.read_cache(TEMP_WRITE_LOCATION)


def test_written_cache_matches_read(setup_teardown_test_data, init_cache):
    """
    Args:
        init_cache (_cache.MemoryCache)
    """
    init_cache.write_cache(DATA_WRITTEN, TEMP_WRITE_LOCATION)
    cached_data = init_cache.read_cache(TEMP_WRITE_LOCATION)

    assert cached_data == DATA_WRITTEN


@pytest.mark.xfail(raises=exceptions.CacheError, strict=True)
def test_MemoryCache_ChangeCacheContents_RaiseCacheChanged(
        setup_teardown_test_data, init_cache
):
    """
    Args:
        init_cache (_cache.MemoryCache)
    """
    init_cache.write_cache(DATA_WRITTEN, TEMP_WRITE_LOCATION)
    add_extra_lines_to_file()
    init_cache.read_cache(TEMP_WRITE_LOCATION)
