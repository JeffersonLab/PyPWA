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
Defines how the simulation works for PyPWA
"""

import multiprocessing
import secrets
from typing import Any, Callable, Dict, List, Union

import numpy as npy

from PyPWA import info as _info
from PyPWA.libs import process
from PyPWA.libs.file import project

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


def monte_carlo_simulation(
        function: Callable[[Any, Any], npy.ndarray],
        setup: Callable[[], None],
        params: Dict[str, float],
        data: Union[npy.ndarray, project.BaseFolder],
        processes: int = multiprocessing.cpu_count()
) -> npy.ndarray:
    """Calculates the rejection list
    This takes a user defined intensity function along with it's
    associated data, and generates a pass/fail array to be used to
    mask the monte carlo.

    :param function: Function defining the intensity
    :param setup: A function called once to setup the intensity,
        if needed.
    :param params: Dictionary of the parameters and their associated
        values. These are the values for the intensity to simulate with.
    :param data: The data to simulate against
    :param processes: How many processes to execute with if applicable
    :return: A pass/fail boolean array of the same length as data
    """

    if isinstance(data, npy.ndarray):
        intensity = _in_memory_intensities(
            setup, function, data, params, processes
        )
    elif isinstance(data, project.BaseFolder):
        intensity = _in_table_intensities(setup, function, data, params)
    else:
        raise ValueError("Unknown data type!")

    return _make_reject_list(intensity)


def _in_memory_intensities(
        setup_function: Callable[[], None],
        processing_function: Callable[[Any, Any], npy.ndarray],
        data: npy.ndarray,
        params: Dict[str, float],
        processes: int) -> npy.ndarray:

    kernel = _Kernel(setup_function, processing_function, params)
    interface = _Interface()
    manager = process.make_processes(
        {"data": data}, kernel, interface, processes, False
    )
    return manager.run()


class _Kernel(process.Kernel):

    def __init__(
            self,
            setup_function: Callable[[], None],
            processing_function: Callable[[Any, Any], npy.ndarray],
            parameters: Dict[str, float]):
        self.__setup_function = setup_function
        self.__processing_function = processing_function
        self.__parameters = parameters
        self.data: npy.ndarray = None

    def setup(self):
        self.__setup_function()

    def process(self, data: Any = False) -> Any:
        calculated = self.__processing_function(self.data, self.__parameters)
        return self.PROCESS_ID, calculated


class _Interface(process.Interface):
    IS_DUPLEX = False

    def run(self, communicator: List[Any], args: Any) -> npy.ndarray:
        data = self.__receive_data(communicator)
        return npy.concatenate(data)

    @staticmethod
    def __receive_data(communicator: List[Any]) -> List[npy.ndarray]:
        list_of_data = list(range(len(communicator)))
        for communication in communicator:
            data = communication.recv()
            list_of_data[data[0]] = data[1]
        return list_of_data


def _in_table_intensities(
        setup_function: Callable[[], None],
        processing_function: Callable[[Any, Any], Any],
        data: project.BaseFolder,
        parameters: Dict[str, float]) -> npy.ndarray:

    setup_function()

    chunk_collection = []
    for index, chunk in enumerate(data.root.iterate_data()):
        chunk_collection.append(processing_function(chunk, parameters))

    return npy.concatenate(chunk_collection)


def _make_reject_list(intensities: npy.ndarray) -> npy.ndarray:
    rejection_list = npy.zeros(len(intensities), bool)
    for index, event in enumerate(intensities / intensities.max()):
        if event > secrets.SystemRandom().random():
            rejection_list[index] = True
    return rejection_list
