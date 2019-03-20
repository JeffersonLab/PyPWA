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
Interfaces for the cache objects defined in this package
--------------------------------------------------------

- WriteInterface - Interface for all write objects
- ReadInterface - Interface for all read objects.
"""

from typing import Any

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class WriteInterface(object):

    def write_cache(self, data: Any):
        raise NotImplementedError


class ReadInterface(object):

    def is_valid(self):
        raise NotImplementedError

    def get_cache(self):
        raise NotImplementedError
