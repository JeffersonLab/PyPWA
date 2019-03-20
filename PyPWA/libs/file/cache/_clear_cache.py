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

import logging

from PyPWA import AUTHOR, VERSION
from . import _basic_info, _template

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ClearCache(_template.ReadInterface):

    __LOGGER = logging.getLogger(__name__ + ".ClearCache")

    def __init__(self, basic_info: _basic_info.FindBasicInfo):
        self.__info = basic_info
        self.__attempt_to_remove_cache()

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.__info)

    def is_valid(self):
        return False

    def get_cache(self):
        raise RuntimeError("No Valid Cache")

    def __attempt_to_remove_cache(self):
        try:
            self.__remove_cache()
        except OSError:
            self.__LOGGER.debug("No cache to delete.")

    def __remove_cache(self):
        self.__info.cache_location.unlink()
