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

"""

import logging
import os

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.cache import _basic_info
from PyPWA.builtin_plugins.data.cache import _template

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ClearCache(_template.ReadInterface):

    _logger = logging.getLogger(__name__)
    _info = _basic_info.FindBasicInfo

    def __init__(self, basic_info):
        self._logger.addHandler(logging.NullHandler())
        self._info = basic_info
        self._attempt_to_remove_cache()

    @property
    def is_valid(self):
        return False

    def get_cache(self):
        raise exceptions.CacheError

    def _attempt_to_remove_cache(self):
        try:
            self._remove_cache()
        except OSError:
            self._logger.info("No cache to delete.")

    def _remove_cache(self):
        os.remove(self._info.cache_location)
