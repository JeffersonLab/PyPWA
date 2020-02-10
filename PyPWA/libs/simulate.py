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
from typing import Any, Dict, List, Union, Set, Tuple

import numpy as npy
import pandas as pd

from PyPWA import info as _info
from PyPWA.libs import process
from PyPWA.libs.file import project
from PyPWA.libs.fit import likelihoods

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


def monte_carlo_simulation(
        amplitude: likelihoods.NestedFunction,
        data: Union[npy.ndarray, pd.DataFrame, project.BaseFolder],
        params: Dict[str, float] = None,
        processes: int = multiprocessing.cpu_count()) -> npy.ndarray:
    """Produces the rejection list
    This takes a user defined intensity object along with it's
    associated data, and generates a pass/fail array to be used to
    mask any dataset of the same length as data.

    Parameters
    ----------
    amplitude : Amplitude derived from AbstractAmplitude
        A user defined amplitude or pre-made PyPWA amplitude that you
        wish to carve your data with.
    data : Structured Array, DataFrame, or BaseFolder from Project
        This is the data you want to be passed to the `setup` function
        of your amplitude. If you provide a Structured Array or DataFrame
        the entire calculation will occur in memory with the selected
        number of processes. If you provide a Project BaseFolder the
        calculation will rely entirely on the Amplitude.
    params : Dict[str, float], optional
         An optional dictionary of parameters that will be passed to the
         AbstractAmplitude's `calculate` function.
    processes : int, optional
        Selects the number of processes to run with, defaults to the
        number of processes detected through multiprocessing

    Returns
    -------
    boolean npy.ndarray
        A masking array that can be used with any DataFrame or Structured
        Array to cut the events to the generated shape

    Raises
    ------
    ValueError
        If the data is not understood. If you received this, check your
        data to ensure its a supported type

    Examples
    --------
    How to cut your data with results from monte_carlo_simulation

    >>> rejection = monte_carlo_simulation(Amplitude(), data)
    >>> carved = data[rejection]
    """
    intensity, max_value = process_user_function(
        amplitude, data, params, processes
    )
    return make_rejection_list(intensity, max_value)


def process_user_function(amplitude: likelihoods.NestedFunction,
        data: Union[npy.ndarray, pd.DataFrame, project.BaseFolder],
        params: Dict[str, float] = None,
        processes: int = multiprocessing.cpu_count()
) -> Tuple[npy.ndarray, float]:
    """Produces an array of values for the calculated function.

    Parameters
    ----------
    amplitude : Amplitude derived from AbstractAmplitude
        A user defined amplitude or pre-made PyPWA amplitude that you
        wish to carve your data with.
    data : Structured Array, DataFrame, or BaseFolder from Project
        This is the data you want to be passed to the `setup` function
        of your amplitude. If you provide a Structured Array or DataFrame
        the entire calculation will occur in memory with the selected
        number of processes. If you provide a Project BaseFolder the
        calculation will rely entirely on the Amplitude.
    params : Dict[str, float], optional
         An optional dictionary of parameters that will be passed to the
         AbstractAmplitude's `calculate` function.
    processes : int, optional
        Selects the number of processes to run with, defaults to the
        number of processes detected through multiprocessing

    Returns
    -------
    (float npy.ndarray, float)
        The final values computed from the user's function and the max
        value computed for that dataset.

    Raises
    ------
    ValueError
        If the data is not understood. If you received this, check your
        data to ensure its a supported type
    """
    if isinstance(data, (npy.ndarray, pd.DataFrame)):
        intensity = _in_memory_intensities(amplitude, data, params, processes)
    elif isinstance(data, project.BaseFolder):
        intensity = _in_table_intensities(amplitude, data, params)
    else:
        raise ValueError("Unknown data type!")

    return intensity, intensity.max()


def _in_memory_intensities(
        amplitude: likelihoods.NestedFunction,
        data: Union[npy.ndarray, pd.DataFrame],
        params: Dict[str, float],
        processes: int) -> npy.ndarray:

    kernel = _Kernel(amplitude, params)
    if not amplitude.USE_MP or not processes:
        kernel.data = data
        kernel.setup()
        return kernel.run()[1]

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
            amplitude: likelihoods.NestedFunction,
            parameters: Dict[str, float]):
        self.__amplitude = amplitude
        self.__parameters = parameters
        self.data: npy.ndarray = None

    def setup(self):
        self.__amplitude.setup(self.data)

    def process(self, data: Any = False) -> Any:
        calculated = self.__amplitude.calculate(self.__parameters)
        return self.PROCESS_ID, calculated


class _Interface(process.Interface):
    IS_DUPLEX = False

    def run(self, communicator: List[Any], *args: Any) -> npy.ndarray:
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
        amplitude: likelihoods.NestedFunction,
        data: project.BaseFolder,
        parameters: Dict[str, float]) -> npy.ndarray:

    amplitude.setup(data)
    return amplitude.calculate(parameters)


def make_rejection_list(
        intensities: npy.ndarray,
        max_value: Union[List[float], npy.ndarray, float]
) -> npy.ndarray:
    """Produces the rejection list from pre-calculated function values.
    Uses the values returned by process_user_function.

    Parameters
    ----------
    intensities : Numpy array or Pandas Series
        This is a single dimensional array containing the final values
        for the user's function.
    max_value : List, Tuple, Set, nd.ndarray, or float
        The max value for the entire dataset, or list of all the max
        values from each dataset. Only the largest value from the list
        will be used.

    Returns
    -------
    boolean npy.ndarray
        A masking array that can be used with any DataFrame or Structured
        Array to cut the events to the generated shape
    """
    if isinstance(max_value, (list, tuple, set, npy.ndarray)):
        max_value = max(max_value)

    random_numbers = npy.random.rand(len(intensities))
    return (intensities / max_value) > random_numbers
