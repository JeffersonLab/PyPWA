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

import copy
import multiprocessing
from abc import abstractmethod, ABC
from typing import Any, Callable, Dict, List, Union, Optional as Opt

import numpy as npy
import pandas as pd
import numexpr as ne

from PyPWA import info as _info
from PyPWA.libs import process

# Handle GPU calculation being available... or not.
GPU_AVAIL = True
try:
    import cupy as cp
except ImportError:
    GPU_AVAIL = False
    cp = npy


__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class NestedFunction(ABC):
    """Interface for Amplitudes

    These objects are used for calculating the users amplitude. They're
    expected to be initialized by the time they are sent to the kernel,
    and will be deep-copied for each process. The setup will be called
    first to initialize data and anything else that might need to be done,
    and then the calculate function will be called for each call to the
    likelihood.

    Set USE_MP to false to execute on the main thread only, this is best
    for when using packages like numexpr.

    Set USE_GPU to calculate the likelihood entirely on the GPU. Assumes that
    all data returned from the NestedFunction will already be in CuPy. If
    this is set to True, then GPU acceleration will be used over
    multiprocessing, and will effectively implicitly set USE_MP to false.

    See Also
    --------
    FunctionAmplitude : For using the old amplitudes with PyPWA 3
    """

    USE_MP = True
    USE_GPU = False

    def __call__(self, *args):
        return self.calculate(*args)

    @abstractmethod
    def calculate(self, parameters) -> npy.ndarray:
        """Calculates the amplitude

        Parameters
        ----------
        parameters :  Dict[str, float]
            The parameters sent to the process by the optimizer

        Returns
        -------
        npy.ndarray or Series
            The array of results for the amplitude, these will be summed
            by the likelihood.
        """
        ...

    @abstractmethod
    def setup(self, data):
        """Sets up the amplitude for use.

        This is where the data that will be used for this specific process
        will be passed to.

        Parameters
        ----------
        data : DataFrame or npy.ndarray
            The data that will be used for calculation
        """
        ...


class FunctionAmplitude(NestedFunction):
    """Wrapper for Legacy PyPWA 2.X amplitudes

    The old amplitudes were two simple functions that would be passed to
    the kernels, a single setup function and a calculate function. Now
    the amplitudes are objects. This wraps the functions and presents
    them as the new Amplitude object

    Parameters
    ----------
    setup : Callable[[], ] function with no arguments or returns
        The old setup function that would be used
    processing : Callable[[pd.DataFrame, Dict[str, float]], float]
        The old processing function

    See Also
    --------
    NestedFunction : For defining new functions
    """

    def __init__(
            self, setup: Callable[[], None],
            processing: Callable[[npy.ndarray, Dict[str, float]], npy.ndarray]
    ):
        self.__setup_function = setup
        self.__processing_function = processing
        self.__data: Any = None

    def setup(self, data):
        self.__data = data
        self.__setup_function()

    def calculate(self, parameters) -> npy.ndarray:
        return self.__processing_function(self.__data, parameters)


class _LikelihoodInterface(process.Interface):

    def run(self, communicator: List[Any], *args: Any) -> Any:
        # Our wrappers around the optimizers collapse the parameters into
        # a single parameter. Other optimizers probably won't do this, so
        # instead we just pass the whole tuple along and hope the user's
        # amplitude will know what to do with it.
        if len(args) == 1:
            args = args[0]

        for likelihood_process in communicator:
            likelihood_process.send(args)

        result = npy.float64(0)
        for likelihood_process in communicator:

            data = likelihood_process.recv()
            if isinstance(data, process.ProcessCodes):
                raise likelihood_process.recv()

            result += data
        return result


class _GeneralLikelihood:

    def __init__(self, amplitude: NestedFunction, num_of_process: int):
        self._amplitude = amplitude
        self._num_of_processes = num_of_process
        self._single_process = amplitude.USE_GPU or not amplitude.USE_MP

    def _setup_interface(
            self, likelihood_data: Dict[str, Any], kernel: process.Kernel
    ):
        if self._single_process or not self._num_of_processes:
            [setattr(kernel, n, v) for n, v in likelihood_data.items()]
            kernel.setup()
            self._interface = kernel

        else:
            interface = _LikelihoodInterface()
            self._interface = process.make_processes(
                likelihood_data, kernel, interface, self._num_of_processes
                )


class ChiSquared(_GeneralLikelihood):
    """Computes the Chi-Squared Likelihood with a given amplitude.

    This likelihood supports two different types of the ChiSquared,
    one with binned or one with expected values.

    To use the binned ChiSquared, you need to provide data and binned
    values, to use the expected values, you need to provide data,
    event_errors, and expected_values.

    Parameters
    ----------
    amplitude : AbstractAmplitude
        Either an user defined amplitude, or an amplitude from PyPWA
    data : DataFrame or npy.ndarray
        The data that will be passed directly to the amplitude
    binned : Series or npy.ndarray, optional
        The array of bin values, should be the same length as data
    event_errors : Series or npy.ndarray, optional
        The array of errors, should be the same length as data
    expected_values : Series or npy.ndarray, optional
        The array of expected values, should be the same length as data
    is_minimizer : bool, optional
        Specify if the final value of the likelihood should be multiplied
        by -1. Defaults to True.
    num_of_processes : int, optional
        How many processes to be used to calculate the amplitude. Defaults
        to the number of threads available on the machine. If USE_MP is
        set to false or this is set to zero, no extra processes will
        be spawned

    Raises
    ------
    ValueError
        If binned values or expected/errors are not provided

    Notes
    -----
    Binned ChiSquare:

    .. math::
        \\chi^{2} = \\frac{(Amp(data) - binned)^{2}}{binned}

    Expected values:

    .. math::
        \\chi^{2} = \\frac{(Amp(data) - expected)^{2}}{errors}

    """

    def __init__(
            self, amplitude: NestedFunction,
            data: npy.ndarray,
            binned: Opt[Union[npy.ndarray, pd.Series]] = None,
            event_errors: Opt[Union[npy.ndarray, pd.Series]] = None,
            expected_values: Opt[Union[npy.ndarray, pd.Series]] = None,
            is_minimizer: Opt[bool] = True,
            num_of_processes=multiprocessing.cpu_count(),
    ):

        super(ChiSquared, self).__init__(amplitude, num_of_processes)
        multiplier = 1 if is_minimizer else -1

        likelihood_data = self.__prep_data(
            data, binned, event_errors, expected_values
        )

        kernel = _ChiSquaredKernel(multiplier, amplitude)
        self._setup_interface(likelihood_data, kernel)

    @staticmethod
    def __prep_data(
            data: npy.ndarray,
            binned: Opt[Union[npy.ndarray, pd.Series]] = None,
            event_errors: Opt[Union[npy.ndarray, pd.Series]] = None,
            expected_values: Opt[Union[npy.ndarray, pd.Series]] = None,
    ) -> Dict[str, Union[npy.ndarray, pd.DataFrame, pd.Series]]:
        likelihood_data = {"data": data}
        if binned is not None:
            likelihood_data["binned"] = binned
        elif event_errors is not None and expected_values is not None:
            likelihood_data["event_errors"] = event_errors
            likelihood_data["expected_values"] = expected_values
        else:
            raise ValueError("ChiSquared needs Binned or Expected/Errors set!")
        return likelihood_data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __call__(self, *args):
        return self._interface.run(*args)

    def close(self):
        """Closes the likelihood
        This needs to be called after you're done with the likelihood,
        _Unless_, you created the likelihood using the `with` statement
        """
        self._interface.close()


class _ChiSquaredKernel(process.Kernel):

    def __init__(self, multiplier: int, amplitude: NestedFunction):
        self.__multiplier = multiplier
        self.__amplitude = amplitude

        # These are set by the process lib
        self.data: npy.ndarray = None
        self.binned: npy.ndarray = None
        self.event_errors: npy.ndarray = None
        self.expected_values: npy.ndarray = None

        # This is set at run time, after data has been loaded
        self.__likelihood: Callable[[npy.ndarray], npy.float] = None

    def setup(self):
        self.__amplitude.setup(self.data)

        if self.binned is not None:
            self.__likelihood = self.__binned
        else:
            self.__likelihood = self.__expected_errors

    def process(self, data: Any = False) -> float:
        intensity = self.__amplitude.calculate(data)
        return self.__multiplier * self.__likelihood(intensity)

    def __binned(self, results):
        if self.__amplitude.USE_GPU:
            return cp.asnumpy(
                cp.sum((results - self.binned)**2/self.binned)
            )
        else:
            return ne.evaluate(
                "sum(((results - binned)**2)/binned)", local_dict={
                    "results": results, "binned": self.binned
                }
            )

    def __expected_errors(self, results):
        if self.__amplitude.USE_GPU:
            return cp.asnumpy(
                cp.sum((results - self.expected_values)**2/self.event_errors)
            )
        else:
            return ne.evaluate(
                "sum(((results - expected)**2)/errors)", local_dict={
                    "results": results, "expected": self.expected_values,
                    "errors": self.event_errors
                }
            )


class LogLikelihood(_GeneralLikelihood):
    """Computes the log likelihood with a given amplitude.

    To use the standard log likelihood, you only need to provide data,
    If binned and quality factor are not provided, they will default to
    1. If you wish to use the Extended Log Likelihood, you must provide
    monte_carlo data. The generated length will be set to the length of
    the monte_carlo, unless a generated length is provided.

    Parameters
    ----------
    amplitude : AbstractAmplitude
        Either an user defined amplitude, or an amplitude from PyPWA
    data : DataFrame or npy.ndarray
        Data that will be passed directly to the amplitude
    monte_carlo : DataFrame or npy.ndarray, optional
        Data that will be passed to the monte_carlo
    binned : Series or npy.ndarray, optional
        Array with bin values. This won't be used if monte_carlo is
        provided.
    quality_factor : Series or npy.ndarray, optional
        Array with quality factor values
    generated_length : int, optional
        The generated length of values for use with the monte_carlo,
        this value will default to the length of monte_carlo
    is_minimizer : bool, optional
        Specify if the final value of the likelihood should be multiplied
        by -1. Defaults to True.
    num_of_processes : int, optional
        How many processes to be used to calculate the amplitude. Defaults
        to the number of threads available on the machine. If USE_MP is
        set to false or this is set to zero, no extra processes will
        be spawned

    Notes
    -----
    Standard Log-Likelihood. If not provided, :math:`Q_f` and binned will
    be set to 1:

    .. math::
        L = \\sum{Q_f \\cdot binned \\cdot log (Amp(data))}

    Extended Log-Likelihood. If not provided, the Q_f will be set to 1,
    and generated_length will be set to len(monte_carlo)

    .. math::
        L = \\sum{Q_f \\cdot log (Amp(data))} - \\
            \\frac{1}{generated\\_length} \\cdot \\sum{Amp(monte\\_carlo)}

    """

    def __init__(
            self, amplitude: NestedFunction,
            data: Union[npy.ndarray, pd.DataFrame],
            monte_carlo: Opt[Union[npy.ndarray, pd.DataFrame]] = None,
            binned: Opt[Union[npy.ndarray, pd.Series]] = None,
            quality_factor: Opt[Union[npy.ndarray, pd.Series]] = None,
            generated_length: Opt[int] = 1,
            is_minimizer: Opt[bool] = True,
            num_of_processes=multiprocessing.cpu_count(),
    ):
        super(LogLikelihood, self).__init__(amplitude, num_of_processes)
        multiplier = -1 if is_minimizer else 1

        if monte_carlo is not None and generated_length == 1:
            generated_length = len(monte_carlo)

        kernel = _LogLikelihoodKernel(multiplier, amplitude, generated_length)
        likelihood_data = self.__prep_data(
            data, monte_carlo, binned, quality_factor
        )

        self._setup_interface(likelihood_data, kernel)

    @staticmethod
    def __prep_data(
            data: Union[npy.ndarray, pd.DataFrame],
            monte_carlo: Opt[Union[npy.ndarray, pd.DataFrame]] = None,
            binned: Opt[Union[npy.ndarray, pd.Series]] = None,
            quality_factor: Opt[Union[npy.ndarray, pd.Series]] = None,
    ) -> Dict[str, Union[npy.ndarray, pd.DataFrame, pd.Series]]:
        likelihood_data = {"data": data}
        if monte_carlo is not None:
            likelihood_data["monte_carlo"] = monte_carlo
        if binned is not None:
            likelihood_data["binned"] = binned
        if quality_factor is not None:
            likelihood_data["quality_factor"] = quality_factor
        return likelihood_data

    def __call__(self, *args):
        return self._interface.run(*args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Closes the likelihood
        This needs to be called after you're done with the likelihood,
        UNLESS, you created the likelihood using the `with` statement
        """
        self._interface.close()


class _LogLikelihoodKernel(process.Kernel):

    def __init__(
            self, multiplier: int, amplitude: NestedFunction,
            generated_length=Opt[int]
    ):
        self.__multiplier = multiplier
        self.__data_amplitude = amplitude
        self.__monte_carlo_amplitude = copy.deepcopy(amplitude)
        self.__generated = 1/generated_length

        # These are set by the process lib
        self.data: npy.ndarray = None
        self.monte_carlo: npy.ndarray = None
        self.binned: Union[npy.ndarray, float] = 1
        self.quality_factor: Union[npy.ndarray, float] = 1

        # This is set at run time, after data has been loaded
        self.__likelihood: Callable[[npy.ndarray], npy.float] = None

    def setup(self):
        self.__data_amplitude.setup(self.data)

        if self.monte_carlo is not None and self.__generated is not None:
            self.__monte_carlo_amplitude.setup(self.monte_carlo)
            self.__likelihood = self.__extended_likelihood
        else:
            self.__likelihood = self.__log_likelihood

    def process(self, data: Any = False) -> float:
        return self.__multiplier * self.__likelihood(data)

    def __extended_likelihood(self, params):
        data = self.__data_amplitude.calculate(params)
        monte_carlo = self.__monte_carlo_amplitude.calculate(params)

        if self.__data_amplitude.USE_GPU:
            likelihood = cp.asnumpy(
                cp.sum(self.quality_factor * cp.log(data))
            )
            monte_carlo_sum = cp.asnumpy(cp.sum(monte_carlo))
        else:
            likelihood = ne.evaluate(
                "sum(qf * log(data))", local_dict={
                    "qf": self.quality_factor, "data": data
                }
            )
            monte_carlo_sum = npy.sum(monte_carlo)

        return likelihood - self.__generated * monte_carlo_sum

    def __log_likelihood(self, params):
        data = self.__data_amplitude.calculate(params)

        if self.__data_amplitude.USE_GPU:
            return cp.asnumpy(
                cp.sum(self.quality_factor * self.binned * cp.log(data))
            )

        else:
            return ne.evaluate(
                "sum(qf*binned*log(data))", local_dict={
                    "qf": self.quality_factor, "binned": self.binned, "data": data
                }
            )


class EmptyLikelihood(_GeneralLikelihood):
    """Provides the multiprocessing benefits of a standard likelihood
    without a defined likelihood.

    This allows you to include a likelihood into your amplitude or to run
    your amplitude without a likelihood entirely.

    Attributes
    ----------
    amplitude : AbstractAmplitude
        Either an user defined amplitude, or an amplitude from PyPWA
    data : DataFrame or npy.ndarray
        The data that will be passed directly to the amplitude
    num_of_processes : int, optional
        How many processes to be used to calculate the amplitude. Defaults
        to the number of threads available on the machine. If USE_MP is
        set to false or this is set to zero, no extra processes will
        be spawned
    """

    def __init__(
            self, amplitude: NestedFunction,
            data: Union[npy.ndarray, pd.DataFrame],
            num_of_processes=multiprocessing.cpu_count()
    ):
        super(EmptyLikelihood, self).__init__(amplitude, num_of_processes)
        kernel = _EmptyKernel(amplitude)
        self._setup_interface({"data": data}, kernel)

    def __call__(self, *args):
        return self._interface.run(*args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Closes the likelihood
        This needs to be called after you're done with the likelihood,
        UNLESS, you created the likelihood using the `with` statement
        """
        self._interface.close()


class _EmptyKernel(process.Kernel):

    def __init__(self, amplitude: NestedFunction):
        self.__amplitude = amplitude

        # These are set by the process lib
        self.data: npy.ndarray = None

    def setup(self):
        self.__amplitude.setup(self.data)

    def process(self, data: Any = False) -> float:
        if self.__amplitude.USE_GPU:
            return cp.asnumpy(cp.sum(self.__amplitude.calculate(data)))
        else:
            return npy.sum(self.__amplitude.calculate(data))
