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
Shared logic between PyFit and PySimulate
-----------------------------------------

- DataLoading - takes a data parsing object and use it to load data
  for the two programs in a way that the data can be easily repacked into 
  processes.

- FunctionLoader - used to load the setup and processing functions in a 
  predictable way.
"""

import logging
import os
from typing import Callable, Dict, Union
from typing import Optional as Opt

import numpy
from numpy import ndarray, float64

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared import plugin_loader
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


users_process_function = Callable[[ndarray, Dict[str, float64]], ndarray]
users_setup_function = Callable[[], None]


class DataLoading(object):

    __LOGGER = logging.getLogger(__name__ + ".DataLoading")

    def __init__(
            self,
            parser,  # type: plugins.DataParser
            data,  # type: str
            internal_data=None,  # type: Opt[Dict[str, str]]
            qfactor=None,  # type: Opt[str]
            monte_carlo=None  # type: Opt[str]
    ):
        # type: (...) -> None
        self._parser = parser
        self._data_file = data
        self._qfactor_file = qfactor
        self._monte_carlo_file = monte_carlo
        self.__internal_names = internal_data
        self.__data = None  # type: ndarray
        self.__qfactor = None  # type: ndarray
        self.__monte_carlo = None  # type: ndarray
        self.__binned = None  # type: ndarray
        self.__event_errors = None  # type: ndarray
        self.__expected_values = None  # type: ndarray
        self.__load_data()

    def __load_data(self):
        self.__parse_data_file()
        self.__process_data()
        self.__parse_qfactor_file()
        self.__parse_monte_carlo_file()

    def __parse_data_file(self):
        if self.__is_file(self._data_file):
            self.__LOGGER.info("Loading data.")
            self.__data = self._parser.parse(self._data_file)
        else:
            raise ValueError("Data Location isn't a file!")

    def __process_data(self):
        if "quality factor" in self.__internal_names:
            self.__qfactor = self.__extract_data(
                self.__internal_names["quality factor"]
            )
        else:
            self.__qfactor = self.__extract_data("qfactor")

        if "binned data" in self.__internal_names:
            self.__binned = self.__extract_data(
                self.__internal_names["binned data"]
            )
        else:
            self.__qfactor = self.__extract_data("BinN")

        if "event errors" in self.__internal_names:
            self.__event_errors = self.__extract_data(
                self.__internal_names["event errors"]
            )

        if "expected values" in self.__internal_names:
            self.__expected_values = self.__extract_data(
                self.__internal_names["expected values"]
            )

    def __extract_data(self, column):
        # type: (str) -> ndarray
        names = list(self.__data.dtype.names)
        if column in names:
            self.__LOGGER.info("Extracting '%s' from data." % column)
            names.remove(column)
            data = self.__data[column]
            self.__data = self.__data[names]
        else:
            data = numpy.ones(len(self.__data))

        return data

    def __parse_qfactor_file(self):
        if self.__is_file(self._qfactor_file):
            self.__LOGGER.info("Loading QFactor data.")
            self.__qfactor = self._parser.parse(self._qfactor_file)
        elif self.__qfactor is None:
            self.__qfactor = numpy.ones(len(self.__data))

    def __parse_monte_carlo_file(self):
        if self.__is_file(self._monte_carlo_file):
            self.__LOGGER.info("Loading Monte Carlo Data.")
            self.__monte_carlo = self._parser.parse(self._monte_carlo_file)
        else:
            self.__monte_carlo = None

    @staticmethod
    def __is_file(file_location):
        # type: (str) -> bool
        if isinstance(file_location, str) and os.path.isfile(file_location):
            return True
        else:
            return False

    def write(self, file_location, data):
        # type: (str, ndarray) -> None
        self._parser.write(file_location, data)

    @property
    def data(self):
        # type: () -> ndarray
        return self.__data

    @property
    def qfactor(self):
        # type: () -> ndarray
        return self.__qfactor

    @property
    def monte_carlo(self):
        # type: () -> Union[ndarray, None]
        return self.__monte_carlo

    @property
    def binned(self):
        # type: () -> ndarray
        return self.__binned

    @property
    def event_errors(self):
        # type: () -> ndarray
        return self.__event_errors

    @property
    def expected_values(self):
        # type: () -> ndarray
        return self.__expected_values


class FunctionLoader(object):

    __LOGGER = logging.getLogger(__name__ + ".FunctionLoader")

    def __init__(self, location, process_name, setup_name=None):
        # type: (str, str, Opt[str]) -> None
        self.__loader = plugin_loader.PluginLoader()
        self.__loader.add_plugin_location(location)
        self.__process_name = process_name
        self.__setup_name = setup_name
        self.__process = None  # type: users_process_function
        self.__setup = None  # type: users_setup_function
        self.__load_functions()

    def __load_functions(self):
        self.__load_process()
        self.__load_setup()

    def __load_process(self):
        self.__process = self.__loader.get_by_name(self.__process_name)

    def __load_setup(self):
        if isinstance(self.__setup_name, str):
            self.__setup = self.__loader.get_by_name(self.__setup_name, False)
            self.__LOGGER.debug("Found setup type %s" % repr(self.__setup))
        self.__set_none_to_empty()

    def __set_none_to_empty(self):
        if self.__setup is None:
            self.__LOGGER.info("No setup function found, settings to empty.")
            self.__setup = self.__empty

    @staticmethod
    def __empty():
        # type: () -> None
        pass

    @property
    def process(self):
        # type: () -> users_process_function
        return self.__process

    @property
    def setup(self):
        # type: () -> users_setup_function
        return self.__setup
