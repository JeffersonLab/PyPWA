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

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.interfaces import data_loaders

__credits__ = ["Keandre Palmer"]
__author__ = AUTHOR
__version__ = VERSION


class NumpyReader(data_loaders.Reader):

    def __init__(self, file_location):
        self.__array = numpy.load(file_location)
        self.__counter = 0

    def get_event_count(self):
        return len(self.__array)

    def next(self):
        if self.__counter < len(self):
            self.__counter += 1
            return numpy.copy(self.__array[self.__counter-1])
        else:
            raise StopIteration

    def close(self):
        del self.__array


class NumpyWriter(data_loaders.Writer):
    def __init__(self, file_location):
        self.__array = False
        self.__file_location = file_location
        self.__i = 0

    def write(self, data):
        # type: (numpy.ndarray) -> None
        if not isinstance(self.__array, numpy.ndarray):
            self.__array = data
        else:
            self.__array = numpy.resize(self.__array, self.__array.size + 1)
            self.__array[-1] = data

    def close(self):
        # type: () -> None
        numpy.save(self.__file_location,self.__array)
        del self.__array