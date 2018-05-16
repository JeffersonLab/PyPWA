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

import numpy
from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.components.data_processor import data_templates
from PyPWA.libs.components.data_processor import exceptions

__credits__ = ["Christopher Banks"]
__author__ = AUTHOR
__version__ = VERSION


class NumpyDataTest(data_templates.ReadTest):

    def __init__(self):
        self.__list_test = [
            self.__binary_file_load,
            self.__text_file,
        ]

    @staticmethod
    def __binary_file_load(file_location):
        # type: (Path) -> None
        numpy.load(str(file_location))

    @staticmethod
    def __text_file(file_location):
        # type: (Path) -> None
        numpy.loadtxt(str(file_location))

    def test(self, file_location):
        # type: (Path) -> None
        self.__iterate_through_file_types(file_location)

    def __iterate_through_file_types(self, file_location):
        # type: (Path)-> None
        result = []
        for file_type in self.__list_test:
            result.append(self.__run_test(file_type, file_location))
        if True not in result:
            raise exceptions.IncompatibleData

    @staticmethod
    def __run_test(file_type, file_location):
        # type: (str, str)-> bool
        try:
            file_type(file_location)
            return True
        except ValueError:
            return False
        except IOError:
            return False
