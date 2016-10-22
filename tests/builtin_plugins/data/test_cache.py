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

from PyPWA.builtin_plugins.data import _cache

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/temporary_write_data"
)

CACHE_DIR = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/"
)


def test_MemoryCache_ReadNoCache_RaisesCacheNotFound():
    """
    Checks that the cache fails correctly if its called to read a cache
    that doesn't exist.
    """
    with open(TEMP_WRITE_LOCATION, "w") as stream:
        stream.write("Something\n")

    cache = _cache.MemoryCache()

    with pytest.raises(_cache.CacheError):
        cache.read_cache(TEMP_WRITE_LOCATION, CACHE_DIR)

    os.remove(TEMP_WRITE_LOCATION)


def test_MemoryCache_WriteAndRead_ContentsMatch():
    """
    Checks that the data that is written out to the cache can be read back
    in correctly.
    """
    with open(TEMP_WRITE_LOCATION, "w") as stream:
        stream.write("Something\n")

    cache = _cache.MemoryCache()
    cache.make_cache("Something", TEMP_WRITE_LOCATION, CACHE_DIR)

    cached_data = cache.read_cache(TEMP_WRITE_LOCATION, CACHE_DIR)

    assert cached_data == "Something"

    os.remove(TEMP_WRITE_LOCATION)
    os.remove(CACHE_DIR + "/.temporary_write_data.pickle")


def test_MemoryCache_ChangeCacheContents_RaiseCacheChanged():
    """
    Checks that the correct error is raised when the cached file has
    changed between cache attempts.
    """
    with open(TEMP_WRITE_LOCATION, "w") as stream:
        stream.write("Something\n")

    cache = _cache.MemoryCache()
    cache.make_cache("Something", TEMP_WRITE_LOCATION, CACHE_DIR)

    with open(TEMP_WRITE_LOCATION, "w") as stream:
        stream.write("else\n")

    with pytest.raises(_cache.CacheError):
        cache.read_cache(TEMP_WRITE_LOCATION, CACHE_DIR)

    os.remove(TEMP_WRITE_LOCATION)
    os.remove(CACHE_DIR + "/.temporary_write_data.pickle")
