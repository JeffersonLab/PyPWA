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
Templates and Exceptions for PyPWA

This file holds all the templates and exceptions used for the entirety of
PyPWA from the class that need to be extended to build your own plugin and
the exceptions you should use or try to catch when/if an error occurs.
"""

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class NoPath(Exception):
    """
    Exception used when unable to find a path.
    """
    pass


class NoCachePath(NoPath):
    """
    The Exception for when the object was unable to determine a writable
    path for the cache.
    """
    pass


class NoDataPath(NoPath):
    """
    The exception used when unable to find the data path.
    """
    pass


class NoConfigPath(NoPath):
    """
    The exception used when unable to find the config path.
    """
    pass


class NoLogPath(NoPath):
    """
    The exception used when unable to find the log path.
    """
    pass
