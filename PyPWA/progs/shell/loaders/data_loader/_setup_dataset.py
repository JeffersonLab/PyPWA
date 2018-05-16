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
Moves the data in the dataset to its correct positions.
-------------------------------------------------------
- _InternalDataExtractor - Takes the data and extracts columns from it,
  all while remove those columns from the original data.
- _QFactorSetup - Sets up the QFactor data using either the source data
  file or a separate data file.
- LoadData - Main entry point, extracts and loads all the data into the
  dateset object and returns that object.
"""

import logging
from typing import Dict
from typing import Optional as Opt

import numpy

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.progs.shell.loaders.data_loader import _dataset_storage
from PyPWA.progs.shell.loaders.data_loader import _file_handling

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _InternalDataExtractor(object):

    __LOGGER = logging.getLogger(__name__ + "._ColumnExtractor")

    def __init__(self, data_loader, internal_names):
        # type: (_file_handling.DataHandler, Dict[str, str]) -> None
        self.__source_array = data_loader.data
        self.__internal_names = internal_names
        if self.__array_exists():
            self.__column_names = list(data_loader.data.dtype.names)
        else:
            self.__column_names = list()

    def __array_exists(self):
        # type: () -> bool
        return isinstance(self.__source_array, numpy.ndarray)

    def extract(self, name):
        # type: (str) -> numpy.ndarray
        if name in self.__internal_names and self.__array_exists():
            return self.__process_column_name(self.__internal_names[name])
        else:
            return self.__empty_array()

    def __process_column_name(self, column):
        # type: (str) -> numpy.ndarray
        if self.__column_in_array(column):
            return self.__extract_column_from_array(column)
        else:
            return self.__empty_array()

    def __column_in_array(self, column):
        # type: (str) -> bool
        return column in self.__column_names

    def __extract_column_from_array(self, column):
        # type: (str) -> numpy.ndarray
        extracted_data = self.__extract_array_from_source_array(column)
        self.__trim_extracted_column_from_source_array()
        return extracted_data

    def __extract_array_from_source_array(self, column):
        # type: (str) -> numpy.ndarray
        self.__column_names.remove(column)
        return self.__source_array[column]

    def __trim_extracted_column_from_source_array(self):
        self.__source_array = self.__source_array[self.__column_names]

    def __empty_array(self):
        # type: () -> numpy.ndarray
        empty_array = numpy.ones(len(self.__source_array))
        return empty_array

    @property
    def trimmed_array(self):
        # type: () -> numpy.ndarray
        return self.__source_array


class _QFactorSetup(object):

    def __init__(self, data_loader, extraction):
        # type: (_file_handling.DataHandler, _InternalDataExtractor) -> None
        self.__data_loader = data_loader
        self.__extractor = extraction

    def load_data(self):
        # type: () -> numpy.ndarray
        if isinstance(self.__data_loader.qfactor, numpy.ndarray):
            return self.__data_loader.qfactor
        else:
            return self.__extracted_data()

    def __extracted_data(self):
        # type: () -> numpy.ndarray
        return self.__extractor.extract("quality factor")


class LoadData(object):

    __LOGGER = logging.getLogger(__name__ + ".DataLoading")

    def __init__(
            self,
            data,  # type: Path
            internal_data,  # type: Dict[str, str]
            qfactor=None,  # type: Opt[Path]
            monte_carlo=None  # type: Opt[Path]
    ):
        # type: (...) -> None
        self.__data_handler = _file_handling.DataHandler(
            data, monte_carlo, qfactor
        )
        self.__extractor = _InternalDataExtractor(
            self.__data_handler, internal_data
        )
        self.__qfactor_setup = _QFactorSetup(
            self.__data_handler, self.__extractor
        )
        self.__storage = _dataset_storage.DataStorage()

    def load(self):
        # type: () -> _dataset_storage.DataStorage
        if isinstance(self.__data_handler.data, numpy.ndarray):
            self.__process_columns()
        self.__process_data()
        return self.__storage

    def __process_columns(self):
        self.__get_binned()
        self.__get_qfactor()
        self.__get_event_errors()
        self.__get_expected_values()

    def __get_binned(self):
        self.__storage.binned = self.__extractor.extract("binned data")

    def __get_qfactor(self):
        self.__storage.qfactor = self.__qfactor_setup.load_data()

    def __get_event_errors(self):
        self.__storage.event_errors = self.__extractor.extract("event errors")

    def __get_expected_values(self):
        self.__storage.expected_values = self.__extractor.extract(
            "expected values"
        )

    def __process_data(self):
        self.__storage.data = self.__extractor.trimmed_array
        self.__storage.monte_carlo = self.__data_handler.monte_carlo
        self.__storage.single_array = self.__data_handler.single_array

    def write(self, file, array):
        self.__data_handler.write(file, array)
