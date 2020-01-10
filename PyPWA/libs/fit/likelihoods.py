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
Main object for Parsing Data
"""

from abc import abstractmethod, ABC
from typing import Any, Callable, Dict, List, Optional, Union
import copy

import numpy as npy

from PyPWA import info as _info
from PyPWA.libs import process
import multiprocessing

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class AbstractAmplitude(ABC):

    @abstractmethod
    def calculate(self, parameters) -> npy.ndarray:
        ...

    @abstractmethod
    def setup(self, data, initial_params):
        ...


class FunctionAmplitude(AbstractAmplitude):

    def __init__(
            self, setup: Callable[[], None],
            processing: Callable[[npy.ndarray, npy.ndarray], npy.ndarray]
    ):
        self.__setup_function = setup
        self.__processing_function = processing
        self.__data: Any = None

    def setup(self, data, initial_params):
        self.__data = data
        self.__setup_function()

    def calculate(self, parameters) -> npy.ndarray:
        return self.__processing_function(self.__data, parameters)


class TranslatorInterface(ABC):

    @abstractmethod
    def __call__(self, *args) -> Union[Dict[str, float], npy.ndarray]:
        ...


class _LikelihoodInterface(process.Interface):

    def __init__(
            self, optimizer_translator: Optional[TranslatorInterface] = None
    ):
        if optimizer_translator is None:
            self.__translator = lambda *x: x
        else:
            self.__translator = optimizer_translator

    def run(self, communicator: List[Any], args: Any) -> Any:
        parameters = self.__translator(args)

        for likelihood_process in communicator:
            likelihood_process.send(parameters)

        result = npy.float(0)
        for likelihood_process in communicator:

            data = likelihood_process.recv()
            if isinstance(data, process.ProcessCodes):
                raise likelihood_process.recv()

            result += data
        return result


class ChiSquared:

    def __init__(
            self, amplitude: AbstractAmplitude,
            initial_parameters: Union[Dict[str, Any], npy.ndarray],
            data: Dict[str, npy.ndarray],
            is_minimizer: Optional[bool] = True,
            num_of_processes=multiprocessing.cpu_count(),
            optimizer_translator: Optional[TranslatorInterface] = None
    ):
        multiplier = 1 if is_minimizer else -1

        if "binned" in data or (
                "event_errors" in data and "expected_values" in data
        ):
            raise ValueError("ChiSquared needs Binned or Expected/Errors set!")
        else:
            kernel = _ChiSquaredKernel(
                multiplier, amplitude, initial_parameters
            )

        interface = _LikelihoodInterface(optimizer_translator)
        self.__interface = process.make_processes(
            data, kernel, interface, num_of_processes, True
        )

    def __call__(self, *args):
        return self.__interface.run(args)

    def close(self):
        self.__interface.close()


class _ChiSquaredKernel(process.Kernel):

    def __init__(
            self, multiplier: int, amplitude: AbstractAmplitude,
            initial_parameters: Union[Dict[str, Any], npy.ndarray]
    ):
        self.__multiplier = multiplier
        self.__amplitude = amplitude
        self.__initial_parameters = initial_parameters

        # These are set by the process lib
        self.data: npy.ndarray = None
        self.binned: npy.ndarray = None
        self.event_errors: npy.ndarray = None
        self.expected_values: npy.ndarray = None

        # This is set at run time, after data has been loaded
        self.__likelihood: Callable[[npy.ndarray], npy.float] = None

    def setup(self):
        self.__amplitude.setup(self.data, self.__initial_parameters)

        if self.binned is not None:
            self.__likelihood = self.__binned
        else:
            self.__likelihood = self.__expected_errors

    def process(self, data: Any = False) -> Any:
        intensity = self.__amplitude.calculate(data)
        likelihood = self.__likelihood(intensity)
        return self.__multiplier * likelihood

    def __binned(self, results):
        difference = (results - self.binned) ** 2
        return npy.sum(difference / self.binned)

    def __expected_errors(self, results):
        difference = (results - self.expected_values) ** 2
        return npy.sum(difference / self.event_errors)


class LogLikelihood:

    def __init__(
            self, amplitude: AbstractAmplitude,
            initial_parameters: Union[Dict[str, Any], npy.ndarray],
            data: Dict[str, npy.ndarray],
            generated_length: Optional[int] = None,
            is_minimizer: Optional[bool] = True,
            num_of_processes=multiprocessing.cpu_count(),
            optimizer_translator: Optional[TranslatorInterface] = None
    ):
        multiplier = -1 if is_minimizer else 1
        kernel = _LogLikelihoodKernel(
            multiplier, amplitude, initial_parameters, generated_length
        )
        interface = _LikelihoodInterface(optimizer_translator)
        self.__interface = process.make_processes(
            data, kernel, interface, num_of_processes, True
        )

    def __call__(self, *args):
        return self.__interface.run(args)

    def close(self):
        self.__interface.close()


class _LogLikelihoodKernel(process.Kernel):

    def __init__(
            self, multiplier: int, amplitude: AbstractAmplitude,
            initial_parameters: Union[Dict[str, Any], npy.ndarray],
            generated_length=Optional[int]

    ):
        self.__multiplier = multiplier
        self.__data_amplitude = amplitude
        self.__monte_carlo_amplitude = copy.deepcopy(amplitude)
        self.__initial_parameters = initial_parameters
        self.__generated = 1/generated_length

        # These are set by the process lib
        self.data: npy.ndarray = None
        self.monte_carlo: npy.ndarray = None
        self.binned: npy.ndarray = None
        self.quality_factor: npy.ndarray = None

        # This is set at run time, after data has been loaded
        self.__likelihood: Callable[[npy.ndarray], npy.float] = None

    def setup(self):
        self.__data_amplitude.setup(self.data, self.__initial_parameters)

        if self.monte_carlo is not None and self.__generated is not None:
            self.__monte_carlo_amplitude.setup(
                self.monte_carlo, self.__initial_parameters
            )
            self.__likelihood = self.__extended_likelihood
        else:
            self.__likelihood = self.__log_likelihood

        if self.binned is None:
            self.binned = 1
        if self.quality_factor is None:
            self.quality_factor = 1

    def process(self, data: Any = False) -> Any:
        return self.__multiplier * self.__likelihood(data)

    def __extended_likelihood(self, params):
        data_result = npy.sum(
            self.quality_factor * npy.log(
                self.__data_amplitude.calculate(params)
            )
        )

        monte_carlo_result = self.__generated * npy.sum(
            self.__monte_carlo_amplitude.calculate(params)
        )

        return data_result - monte_carlo_result

    def __log_likelihood(self, params):
        intensity = self.quality_factor * self.binned * npy.log(
            self.__data_amplitude.calculate(params)
        )
        return npy.sum(intensity)


class EmptyLikelihood:

    def __init__(
            self, amplitude: AbstractAmplitude,
            initial_parameters: Union[Dict[str, Any], npy.ndarray],
            data: Dict[str, npy.ndarray],
            num_of_processes=multiprocessing.cpu_count(),
            optimizer_translator: Optional[TranslatorInterface] = None
    ):
        kernel = _EmptyKernel(amplitude, initial_parameters)
        interface = _LikelihoodInterface(optimizer_translator)
        self.__interface = process.make_processes(
            data, kernel, interface, num_of_processes, True
        )

    def __call__(self, *args):
        return self.__interface.run(args)

    def close(self):
        self.__interface.close()


class _EmptyKernel(process.Kernel):

    def __init__(
            self, amplitude: AbstractAmplitude,
            initial_parameters: Union[Dict[str, Any], npy.ndarray]
    ):
        self.__amplitude = amplitude
        self.__initial_parameters = initial_parameters

        # These are set by the process lib
        self.data: npy.ndarray = None

    def setup(self):
        self.__amplitude.setup(self.data, self.__initial_parameters)

    def process(self, data: Any = False) -> Any:
        return self.__amplitude.calculate(data)
