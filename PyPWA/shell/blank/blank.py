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
A simple blank module that exists purely for testing.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import memory
from PyPWA.core.configurator import option_tools
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Blank(plugins.Main):

    def __init__(self, data_parser, option1, option2):
        # type: (memory.Memory, int, str) -> None
        self.__data_parser = data_parser
        self.__option1 = option1
        self.__option2 = option2

    def start(self):
        assert isinstance(self.__data_parser, memory.Memory)
        assert self.__option1 == 123
        assert isinstance(self.__option2, str)
