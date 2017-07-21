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
from typing import Optional as Opt

from numpy import ndarray

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _FileLoader(object):

    __LOGGER = logging.getLogger(__name__ +"._FileLoader")

    def __init__(self, data_parser):
        self.__data_parser = data_parser

    def load_file(self, file):
        # type: (Opt[str]) -> Opt[ndarray]
        if file:
            return self.__try_to_load_file(file)

    def __try_to_load_file(self, file):
        # type: (str) -> Opt[ndarray]
        try:
            return self.__data_parser.parse(file)
        except Exception as error:
            self.__LOGGER.exception(error)


class DataHandler(object):

    __LOGGER = logging.getLogger(__name__ + "._DataFileLoader")

    def __init__(self, data_parser, data, monte_carlo, qfactor):
        # type: (plugins.DataParser, Opt[str], Opt[str], Opt[str]) -> None
        self.__data_parser = data_parser
        self.__file_loader = _FileLoader(data_parser)
        self.__data = self.__file_loader.load_file(data)
        self.__monte_carlo = self.__file_loader.load_file(monte_carlo)
        self.__qfactor = self.__file_loader.load_file(qfactor)

    def write(self, file, array):
        self.__data_parser.write(file, array)

    @property
    def data(self):
        # type: () -> Opt[ndarray]
        if self.__data_is_columned():
            return self.__data

    def __data_is_columned(self):
        # type: () -> bool
        return bool(self.__data.dtype.names)

    @property
    def monte_carlo(self):
        # type: () -> Opt[ndarray]
        return self.__monte_carlo

    @property
    def qfactor(self):
        # type: () -> Opt[ndarray]
        return self.__qfactor

    @property
    def single_array(self):
        # type: () -> Opt[ndarray]
        if not self.__data_is_columned():
            return self.__data
