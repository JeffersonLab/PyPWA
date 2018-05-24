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
Splits data to be nested inside the Kernels
-------------------------------------------
- _ListSplit - Splits list data
- _ArraySplit - Splits Array Data
- _MainSplitter - Calls the Split Data Objects to split their associated data,
  and raises an error if the data is of an unsupported type
- SetupData - Iterates over the supplied dictionary and calls the splitter
  on each of the available keys. Creates a list of dictionaries with a length
  equal to the number of requested processes.
"""

from typing import Any, Dict, List, Union

import numpy

from PyPWA.libs.math import particle
from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


_supported_types = Union[numpy.ndarray, List[Any], particle.ParticlePool]


class _ArraySplit(object):

    def __init__(self, number_of_process):
        # type: (int) -> None
        self.__number_of_processes = number_of_process

    def __call__(self, data):
        # type: (numpy.ndarray) -> List[numpy.ndarray]
        return numpy.array_split(data, self.__number_of_processes)


class _ListSplit(object):

    def __init__(self, number_of_processes):
        # type: (int) -> None
        self.__number_of_processes = number_of_processes
        self.__packets = [[]] * number_of_processes

    def __call__(self, data):
        # type: (List[Any]) -> List[List[Any]]
        self.__check_data(data)
        self.__split_list(data)
        return self.__packets

    def __check_data(self, data):
        # type: (List[Any]) -> None
        if len(data) < self.__number_of_processes:
            raise ValueError("Trying to split less data than processes!")

    def __split_list(self, data):
        # type: (List[Any]) -> None
        index = 0
        for item in data:
            if index == self.__number_of_processes:
                index = 0
            self.__packets[index].append(item)
            index += 1


class _ParticlePoolSplitter(object):

    def __init__(self, number_of_processes):
        # type: (int) -> None
        self.__number_of_processes = number_of_processes

    def __call__(self, data):
        # type: (particle.ParticlePool) -> List[particle.ParticlePool]
        return data.split(self.__number_of_processes)


class _MainSplitter(object):

    def __init__(self, number_of_processes):
        # type: (int) -> None
        self.__number_of_processes = number_of_processes
        self.__array_split = _ArraySplit(number_of_processes)
        self.__list_split = _ListSplit(number_of_processes)
        self.__pool_split = _ParticlePoolSplitter(number_of_processes)

    def __call__(self, data):
        # type: (_supported_types) -> List[Any]
        if isinstance(data, numpy.ndarray):
            return self.__array_split(data)
        elif isinstance(data, list):
            return self.__list_split(data)
        elif isinstance(data, particle.ParticlePool):
            return self.__pool_split(data)
        else:
            raise ValueError("Unknown data type: %s!" % type(data))


class SetupData(object):

    def __init__(self, number_of_processes):
        # type: (int) -> None
        self.__number_of_processes = number_of_processes
        self.__splitter = _MainSplitter(number_of_processes)
        self.__data_names = None  # type: List[str]
        self.__split_data = None  # type: List[Dict[str, Any]]

    def split(self, data):
        # type: (Dict[str, _supported_types]) -> List[Dict[str, Any]]
        self.__get_data_names(data)
        self.__setup_data_packets()
        self.__load_data(data)
        return self.__split_data

    def __get_data_names(self, data):
        # type: (Dict[str, Any]) -> None
        self.__data_names = data.keys()

    def __setup_data_packets(self):
        split = []
        for process_index in range(self.__number_of_processes):
            split.append(self.__get_empty_dict())
        self.__split_data = split

    def __get_empty_dict(self):
        # type: () -> Dict[str, False]
        internal_dict = dict()
        for data_name in self.__data_names:
            internal_dict[data_name] = 0
        return internal_dict

    def __load_data(self, data):
        # type: (Dict[str, Any]) -> None
        for name in self.__data_names:
            for index, data_packet in enumerate(self.__splitter(data[name])):
                self.__split_data[index][name] = data_packet
