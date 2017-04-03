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
Stores the exceptions used by the parsing plugins for the data module.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class IncompatibleData(Exception):
    """
    Raised when read test fails for a plugin.
    """
    pass


class UnknownData(Exception):
    """
    Raised when no suitable plugin is found.
    """
    pass


class CacheError(OSError):
    """
    A simple error that is raised whenever something has gone wrong with the
    Cache that is known.
    """
    pass
