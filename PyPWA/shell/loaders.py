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
loaders.py - Shared logic between PyFit and PySimulate
------------------------------------------------------

Here two objects are defined, DataLoading and FunctionLoader.

DataLoading is setup to take a data parsing object and use it to load data
for the two programs in a way that the data can be easily repacked into 
processes.

FunctionLoader is used to load the setup and processing functions in a 
predictable way.
"""

import os

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared import plugin_loader
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class DataLoading(object):

    _parser = None  # type: plugins.DataParser
    _data_file = None  # type: str
    _qfactor_file = None  # type: str
    _monte_carlo_file = None  # type: str
    __data = None  # type: numpy.ndarray
    __qfactor = None  # type: numpy.ndarray
    __monte_carlo = None  # type: numpy.ndarray
    __binned = None  # type: numpy.ndarray

    def __init__(self, parser, data, qfactor=None, monte_carlo=None):
        self._parser = parser
        self._data_file = data
        self._qfactor_file = qfactor
        self._monte_carlo_file = monte_carlo

    def load_data(self):
        self.__load_data()
        self.__process_data()
        self.__load_qfactor()
        self.__load_monte_carlo()

    def __load_data(self):
        if self.__is_file(self._data_file):
            self.__data = self._parser.parse(self._data_file)

    def __process_data(self):
        self.__qfactor = self.__extract_data("qfactor")
        self.__binned = self.__extract_data("BinN")

    def __extract_data(self, column):
        names = list(self.__data.dtype.names)
        if column in names:
            names.remove(column)
            data = self.__data[column]
            self.__data = self.__data[names]
        else:
            data = numpy.ones(len(self.__data))

        return data

    def __load_qfactor(self):
        if self.__is_file(self._qfactor_file):
            self.__qfactor = self._parser.parse(self._qfactor_file)
        elif self.__qfactor is None:
            self.__qfactor = numpy.ones(len(self.__data))

    def __load_monte_carlo(self):
        if self.__is_file(self._monte_carlo_file):
            self.__monte_carlo = self._parser.parse(self._monte_carlo_file)
        else:
            self.__monte_carlo = False

    @staticmethod
    def __is_file(file_location):
        if isinstance(file_location, str) and os.path.isfile(file_location):
            return True
        else:
            return False

    def write(self, file_location, data):
        self._parser.write(file_location, data)

    @property
    def data(self):
        return self.__data

    @property
    def qfactor(self):
        return self.__qfactor

    @property
    def monte_carlo(self):
        return self.__monte_carlo

    @property
    def binned(self):
        return self.__binned


class FunctionLoader(object):

    __loader = plugin_loader.PluginStorage()
    __process_name = None
    __setup_name = None
    __process = None
    __setup = None

    def __init__(self, location, process_name, setup_name=None):
        self.__loader.add_plugin_location(location)
        self.__process_name = process_name
        self.__setup_name = setup_name

    def load_functions(self):
        self.__load_process()
        self.__load_setup()

    def __load_process(self):
        self.__process = self.__loader.get_by_name(self.__process_name)

    def __load_setup(self):
        if isinstance(self.__setup_name, str):
            self.__setup = self.__loader.get_by_name(self.__setup_name, False)
        self.__set_none_to_empty()

    def __set_none_to_empty(self):
        if self.__setup is None:
            self.__setup = self.__empty

    @staticmethod
    def __empty():
        pass

    @property
    def process(self):
        return self.__process

    @property
    def setup(self):
        return self.__setup
