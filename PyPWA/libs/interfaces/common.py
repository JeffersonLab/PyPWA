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
Common, nonspecific interfaces for PyPWA
----------------------------------------
- Types - Enumeration for Defined Plugins
- BasePlugin - Base interface for all plugins
- Main - Main interfaces for all main objects.
"""

import enum

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Types(enum.Enum):

    KERNEL_PROCESSING = 1
    OPTIMIZER = 2
    DATA_READER = 3
    DATA_PARSER = 4
    SKIP = 5


class BasePlugin(object):
    # Simply here for inheritance.
    pass


class Main(BasePlugin):

    def start(self):
        # type: () -> None
        """
        This is the method that should start the execution on the main object.
        It is assumed that basic setup of the program has been done by this
        point, and this should simply start the function of the program.
        """
        raise NotImplementedError
