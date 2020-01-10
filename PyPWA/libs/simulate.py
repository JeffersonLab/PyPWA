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
from typing import Any, Dict, List, Union

import numpy as npy
import pandas

from PyPWA import info as _info
from PyPWA.libs import process
from PyPWA.libs.file import project
from PyPWA.libs.fit import likelihoods

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


def monte_carlo_simulation(
        amplitude: likelihoods.AbstractAmplitude,
        data: Union[npy.ndarray, project.BaseFolder],
        params: Dict[str, float] = None,
        processes: int = multiprocessing.cpu_count()) -> npy.ndarray:
    """Produces the rejection list
    This takes a user defined intensity object along with it's
    associated data, and generates a pass/fail array to be used to
    mask the monte carlo.

    :param amplitude: Users amplitude, an object extending from
        AbstractAmplitude
    :param data: Data to simulate against, either as a structured numpy
        array or a pandas DataFrame
    :param params: Dictionary of the parameters and their associated
        values. These are the values for the intensity to simulate with.
    :param processes: How many processes to execute with if applicable
    :return: A pass/fail boolean array of the same length as data
    """

    if isinstance(data, (npy.ndarray, pandas.DataFrame)):
        intensity = _in_memory_intensities(amplitude, data, params, processes)
    elif isinstance(data, project.BaseFolder):
        intensity = _in_table_intensities(amplitude, data, params)
    else:
        raise ValueError("Unknown data type!")

    return _make_reject_list(intensity)


def _in_memory_intensities(
        amplitude: likelihoods.AbstractAmplitude,
        data: Union[npy.ndarray, pandas.DataFrame],
        params: Dict[str, float],
        processes: int) -> npy.ndarray:

    kernel = _Kernel(amplitude, params)
    interface = _Interface()
    manager = process.make_processes(
        {"data": data}, kernel, interface, processes, False
    )
    result = manager.run()
    manager.close()
    return result


class _Kernel(process.Kernel):

    def __init__(
            self,
            amplitude: likelihoods.AbstractAmplitude,
            parameters: Dict[str, float]):
        self.__amplitude = amplitude
        self.__parameters = parameters
        self.data: npy.ndarray = None

    def setup(self):
        self.__amplitude.setup(self.data, self.__parameters)

    def process(self, data: Any = False) -> Any:
        calculated = self.__amplitude.calculate(self.__parameters)
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

            if isinstance(data, process.ProcessCodes):
                raise communication.recv()

            list_of_data[data[0]] = data[1]
        return list_of_data


def _in_table_intensities(
        amplitude: likelihoods.AbstractAmplitude,
        data: project.BaseFolder,
        parameters: Dict[str, float]) -> npy.ndarray:

    amplitude.setup(data, parameters)
    return amplitude.calculate(parameters)


def _make_reject_list(intensities: npy.ndarray) -> npy.ndarray:
    random_numbers = npy.random.rand(len(intensities))
    return (intensities / intensities.max()) > random_numbers
