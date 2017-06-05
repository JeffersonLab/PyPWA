#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

"""

import io
import logging
import pickle

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.cache import _basic_info
from PyPWA.builtin_plugins.data.cache import _template

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ReadCache(_template.ReadInterface):

    _info_object = _basic_info.FindBasicInfo
    _packaged_data = {"hash": "", "data": object}
    _logger = logging.getLogger(__name__)

    def __init__(self, basic_info):
        """
        Loads the cache from disk if it exists, will raise CacheError if
        something is wrong with the cache.
        """
        self._info_object = basic_info
        self._attempt_cache_load()

    @property
    def is_valid(self):
        return self._check_cache_is_valid()

    def get_cache(self):
        if self.is_valid:
            return self._packaged_data["data"]
        else:
            raise exceptions.CacheError

    def _attempt_cache_load(self):
        found_data = self._graciously_load_cache()
        self._set_data(found_data)

    def _graciously_load_cache(self):
        self._logger.debug(
            "Attempting to load %s" % self._info_object.cache_location
        )

        try:
            returned_data = self._load_data()
            self._logger.debug("Successfully loaded pickle cache!")
        except (OSError, IOError):
            returned_data = self._empty_raw_data
            self._logger.info("No cache exists.")
        except Exception as error:
            returned_data = self._empty_raw_data
            self._logger.warning(
                "Pickle is from a different Python version or is damaged."
            )
            self._logger.debug(error, exc_info=True)
        return returned_data

    @property
    def _empty_raw_data(self):
        return {"hash": False, "data": object}

    def _load_data(self):
        with io.open(self._info_object.cache_location, "rb") as stream:
            return pickle.load(stream)

    def _set_data(self, loaded_data):
            self._packaged_data = loaded_data

    def _check_cache_is_valid(self):
        if self._packaged_data["hash"] == self._info_object.file_hash:
            return self._caches_match()
        elif not self._packaged_data["hash"]:
            return self._cache_hash_is_false()
        else:
            return self._cache_hash_changed()

    def _caches_match(self):
        self._logger.debug("Cache Hashes match!")
        return True

    def _cache_hash_is_false(self):
        self._logger.debug("Cache load failed, hash is false.")
        return False

    def _cache_hash_changed(self):
        self._logger.warning("File hash has changed.")

        self._logger.debug(
            "%s != %s" % (
                self._packaged_data["hash"],
                self._info_object.file_hash
            )
        )

        return False


class WriteCache(_template.WriteInterface):

    _packaged_data = {"hash": "", "data": object}
    _logger = logging.getLogger(__name__)
    _info_object = _basic_info.FindBasicInfo

    def __init__(self, basic_info):
        """
        Writes the cache to disk.
        """
        self._logger.addHandler(logging.NullHandler())
        self._info_object = basic_info

    def write_cache(self, data):
        self._set_packaged_data(data)
        self._write_cache_data()

    def _set_packaged_data(self, data):
        self._packaged_data["hash"] = self._info_object.file_hash
        self._packaged_data["data"] = data

    def _write_cache_data(self):
        location = self._info_object.cache_location

        self._logger.debug("Making cache for '%s'" % location)

        with io.open(location, "wb") as stream:
            pickle.dump(
                self._packaged_data, stream, protocol=pickle.HIGHEST_PROTOCOL
            )
