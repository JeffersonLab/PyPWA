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
import enum
from typing import Any, Callable, Dict, List, Union, Optional as Opt

import numexpr as ne
import numpy as npy
import pandas as pd

try:
    import torch
    TORCH_AVAIL = True
except ImportError:
    torch = npy
    torch.Tensor = npy.ndarray
    TORCH_AVAIL = False

from PyPWA import info as _info
from PyPWA.libs import process

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class NestedFunction(ABC):
    """Interface for Amplitudes

    These objects are used for calculating the users' amplitude. They're
    expected to be initialized by the time they are sent to the kernel,
    and will be deep-copied for each process. The setup will be called
    first to initialize data and anything else that might need to be done,
    and then the calculate function will be called for each call to the
    likelihood.

    Set USE_MP to false to execute on the main thread only, this is best
    for when using packages like numexpr that handle multi-threading
    themselves.

    Set USE_TORCH to calculate the likelihood using PyTorch. Assumes that
    all data returned from the NestedFunction will be in a Tensor.

    Set USE_THREADS to calculate the likelihood using threads. This is best
    if the likelihood is dependent on waiting for responses from hardware
    or network devices; or if you are working with data that can not be
    forked.

    Set USE_GPU to calculate the likelihood using GPU. If this is set to true,
    then USE_MP will be set to false, and USE_THREADS and USE_TORCH will be
    set to True internally. This will raise a RuntimeError if the GPU is not
    available.

    Set DEBUG to True to disable all multiprocessing and threads, this will
    prevent errors from being buried in tracebacks.

    Warnings
    --------
    If you enable USE_MP and USE_THREADS, then a RuntimeError will be raised,
    since Multiprocessing and threads are not compatible.

    See Also
    --------
    FunctionAmplitude : For using the old amplitudes with PyPWA 3
    """

    DEBUG = False
    USE_MP = True
    USE_TORCH = False
    USE_THREADS = False
    USE_GPU = False
    THREAD = 0

    def __init__(self):
        # If USE_GPU is set, then we'll disable MP and enable Threads + Torch
        if self.USE_GPU:
            self.USE_MP = False
            self.USE_TORCH = self.USE_THREADS = True

        if self.USE_MP and self.USE_THREADS:
            raise RuntimeError("Cannot use MP and THREADS at the same time")

        if self.DEBUG:
            self.USE_MP = self.USE_THREADS = False

    def __call__(self, *args):
        return self.calculate(*args)

    @abstractmethod
    def calculate(self, parameters) -> Union[npy.ndarray, torch.Tensor]:
        """Calculates the amplitude

        Parameters
        ----------
        parameters :  Dict[str, float]
            The parameters sent to the process by the optimizer

        Returns
        -------
        npy.ndarray, Series, or Tensor
            The array of results for the amplitude, these will be summed
            by the likelihood. A tensor is expected when USE_TORCH is true
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


class LikelihoodType(enum.Enum):
    LIKELIHOOD = enum.auto()
    CHI_SQUARED = enum.auto()
    OTHER = enum.auto()


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

        # Setup Single Process Mode
        no_parallel = not amplitude.USE_MP and not amplitude.USE_THREADS
        if no_parallel or amplitude.DEBUG or num_of_process == 0:
            self._single_process = True
        else:
            self._single_process = False

        # Setup Torch and Multiprocessing
        if TORCH_AVAIL and amplitude.USE_TORCH and amplitude.USE_GPU:
            if torch.cuda.is_available():
                self._num_of_processes = torch.cuda.device_count()
            else:
                raise RuntimeError("GPU not available")
        else:
            self._num_of_processes = num_of_process

        # We could check that USE_TORCH and TORCH_AVAIL are both true, but
        # the amplitude would fail to import if it wasn't.

    def _setup_interface(
            self, likelihood_data: Dict[str, Any], kernel: process.Kernel
    ):
        if self._single_process:
            [setattr(kernel, n, v) for n, v in likelihood_data.items()]
            kernel.setup()
            self._interface = kernel

        elif self._amplitude.USE_THREADS:
            interface = _LikelihoodInterface()
            self._interface = process.make_processes(
                likelihood_data, kernel, interface, self._num_of_processes,
                use_threads=True
            )

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

    TYPE = LikelihoodType.CHI_SQUARED

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
            raise ValueError(
                "ChiSquared needs Binned or Expected/Errors set!"
            )

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
        super(_ChiSquaredKernel, self).__init__()
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
        self.__amplitude.THREAD = self.PROCESS_ID
        self.__amplitude.setup(self.data)

        if self.binned is not None:
            self.__likelihood = self.__binned
            if self.__amplitude.USE_TORCH:
                self.__likelihood = self.__binned_with_torch
        else:
            self.__likelihood = self.__expected_errors
            if self.__amplitude.USE_TORCH:
                self.__likelihood = self.__expected_errors_with_torch

    def process(self, data: Any = False) -> float:
        intensity = self.__amplitude.calculate(data)
        return self.__multiplier * self.__likelihood(intensity)

    def __binned(self, results):
        return ne.evaluate(
            "sum(((results - binned)**2)/binned)", local_dict={
                "results": results, "binned": self.binned
            }
        )

    def __binned_with_torch(self, results):
        return torch.sum(
            (results - self.binned)**2/self.binned
        ).cpu().detach().numpy()

    def __expected_errors(self, results):
        return ne.evaluate(
            "sum(((results - expected)**2)/errors)", local_dict={
                "results": results, "expected": self.expected_values,
                "errors": self.event_errors
            }
        )

    def __expected_errors_with_torch(self, results):
        return torch.sum(
            (results - self.expected_values)**2/self.event_errors
        ).cpu().detach().numpy()


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

    TYPE = LikelihoodType.LIKELIHOOD

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
        super(_LogLikelihoodKernel, self).__init__()
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
        self.__data_amplitude.THREAD = self.PROCESS_ID
        self.__data_amplitude.setup(self.data)

        if self.monte_carlo is not None and self.__generated is not None:
            self.__monte_carlo_amplitude.THREAD = self.PROCESS_ID
            self.__monte_carlo_amplitude.setup(self.monte_carlo)
            self.__likelihood = self.__extended_likelihood
            if self.__data_amplitude.USE_TORCH:
                self.__likelihood = self.__extended_likelihood_with_torch
        else:
            self.__likelihood = self.__log_likelihood
            if self.__data_amplitude.USE_TORCH:
                self.__likelihood = self.__log_likelihood_with_torch

    def process(self, data: Any = False) -> float:
        return self.__multiplier * self.__likelihood(data)

    def __extended_likelihood(self, params):
        data = self.__data_amplitude.calculate(params)
        monte_carlo = self.__monte_carlo_amplitude.calculate(params)

        likelihood = ne.evaluate(
            "sum(qf * log(data))", local_dict={
                "qf": self.quality_factor, "data": data
            }
        )
        monte_carlo_sum = npy.sum(monte_carlo)

        return likelihood - self.__generated * monte_carlo_sum

    def __extended_likelihood_with_torch(self, params):
        data = self.__data_amplitude.calculate(params)
        monte_carlo = self.__monte_carlo_amplitude.calculate(params)

        likelihood = torch.sum(self.quality_factor * torch.log(data))
        monte_carlo_sum = torch.sum(monte_carlo)

        return (
                likelihood - self.__generated * monte_carlo_sum
        ).cpu().detach().numpy()

    def __log_likelihood(self, params):
        data = self.__data_amplitude.calculate(params)
        return ne.evaluate(
            "sum(qf*binned*log(data))", local_dict={
                "qf": self.quality_factor, "binned": self.binned, "data": data
            }
        )

    def __log_likelihood_with_torch(self, params):
        data = self.__data_amplitude.calculate(params)
        return torch.sum(
            self.quality_factor * self.binned * torch.log(data)
        ).cpu().detach().numpy()


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

    TYPE = LikelihoodType.OTHER

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
        super(_EmptyKernel, self).__init__()
        self.__amplitude = amplitude

        # These are set by the process lib
        self.data: npy.ndarray = None

    def setup(self):
        self.__amplitude.THREAD = self.PROCESS_ID
        self.__amplitude.setup(self.data)

        self.process = self._process_numpy
        if self.__amplitude.USE_TORCH:
            self.process = self._process_with_torch

    def process(self, data: Any = False) -> float:
        raise RuntimeError("Call the setup first!")

    def _process_numpy(self, data: Any) -> float:
        return npy.sum(self.__amplitude.calculate(data))  # type: ignore

    def _process_with_torch(self, data: Any) -> float:
        return torch.sum(
            self.__amplitude.calculate(data)
        ).cpu().detach().numpy()


class sweightedLogLikelihood(_GeneralLikelihood):
    """Computes the log likelihood with a given amplitude for sWeighted data.
    To use the sWeighted log likelihood, you only need to provide unbinned data,
    if sWeights are not provided, they will default to
    1. You must provide monte_carlo data. The generated length will be set to
    the length of the monte_carlo, unless a generated length is provided.
    Parameters
    ----------
    amplitude : AbstractAmplitude
        Either an user defined amplitude, or an amplitude from PyPWA
    data : DataFrame or npy.ndarray
        Data that will be passed directly to the amplitude
    monte_carlo : DataFrame or npy.ndarray, optional
        Data that will be passed to the monte_carlo
    sweight : Series or npy.ndarray, optional
        Array with sWeight values
    mcweight : Series or npy.ndarray, optional
        Array with MC weight values
    generated_length : int, optional
        The generated length of values for use with the monte_carlo,
        this value will default to the length of monte_carlo
    multiplier : float, optional
        Specify if the final value of the likelihood should be multiplied
        by a value, e.g. sum(weights)/sum(weights^2). Has to be negative
        for minimizer. Defaults to -1.
    num_of_processes : int, optional
        How many processes to be used to calculate the amplitude. Defaults
        to the number of threads available on the machine. If USE_MP is
        set to false or this is set to zero, no extra processes will
        be spawned
    Notes
    -----
    Extended Log-Likelihood. If not provided, the sW will be set to 1,
    and generated_length will be set to len(monte_carlo)
    .. math::
        L = \\sum{sW \\cdot log (Amp(data))} - \\
            \\frac{1}{generated\_length} \\cdot \\sum{Amp(monte\_carlo)}
    """

    TYPE = LikelihoodType.LIKELIHOOD

    def __init__(
            self, amplitude: NestedFunction,
            data: Union[npy.ndarray, pd.DataFrame],
            monte_carlo: Opt[Union[npy.ndarray, pd.DataFrame]] = None,
            sweight: Opt[Union[npy.ndarray, pd.Series]] = None,
            mcweight: Opt[Union[npy.ndarray, pd.Series]] = None,
            generated_length: Opt[int] = 1,
            multiplier: Opt[float] = -1,
            num_of_processes=multiprocessing.cpu_count(),
    ):
        super(sweightedLogLikelihood, self).__init__(
            amplitude, num_of_processes
        )

        if monte_carlo is not None and generated_length == 1:
            generated_length = len(monte_carlo)

        kernel = _sweightedLogLikelihoodKernel(
            multiplier, amplitude, generated_length
        )
        likelihood_data = self.__prep_data(
            data, monte_carlo, sweight, mcweight
        )

        self._setup_interface(likelihood_data, kernel)

    @staticmethod
    def __prep_data(
            data: Union[npy.ndarray, pd.DataFrame],
            monte_carlo: Opt[Union[npy.ndarray, pd.DataFrame]] = None,
            sweight: Opt[Union[npy.ndarray, pd.Series]] = None,
            mcweight: Opt[Union[npy.ndarray, pd.Series]] = None,
    ) -> Dict[str, Union[npy.ndarray, pd.DataFrame, pd.Series]]:
        likelihood_data = {"data": data}
        if monte_carlo is not None:
            likelihood_data["monte_carlo"] = monte_carlo
        if sweight is not None:
            likelihood_data["sweight"] = sweight
        if mcweight is not None:
            likelihood_data["mcweight"] = mcweight
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


class _sweightedLogLikelihoodKernel(process.Kernel):

    def __init__(
            self, multiplier: float, amplitude: NestedFunction,
            generated_length=Opt[int]
    ):
        super(_sweightedLogLikelihoodKernel, self).__init__()
        self.__multiplier = multiplier
        self.__data_amplitude = amplitude
        self.__monte_carlo_amplitude = copy.deepcopy(amplitude)
        self.__generated = 1/generated_length

        # These are set by the process lib
        self.data: npy.ndarray = None
        self.monte_carlo: npy.ndarray = None
        self.sweight: Union[npy.ndarray, float] = 1
        self.mcweight: Union[npy.ndarray, float] = 1

        # This is set at run time, after data has been loaded
        self.__likelihood: Callable[[npy.ndarray], npy.float] = None

    def setup(self):
        self.__data_amplitude.THREAD = self.PROCESS_ID
        self.__data_amplitude.setup(self.data)

        try:
            self.__monte_carlo_amplitude.TREAD = self.PROCESS_ID
            self.__monte_carlo_amplitude.setup(self.monte_carlo)
            self.__likelihood = self.__extended_likelihood
            if self.__data_amplitude.USE_TORCH:
                self.__likelihood = self.__extended_likelihood_with_torch
        except:
            print("Couldn't setup sweightedLogLikelihood")

    def process(self, data: Any = False) -> float:
        return self.__multiplier * self.__likelihood(data)

    def __extended_likelihood(self, params):
        data = self.__data_amplitude.calculate(params)
        mcdata = self.__monte_carlo_amplitude.calculate(params)

        likelihood_data = ne.evaluate(
            "sum(sw * log(data))", local_dict={
                "sw": self.sweight,
                "data": data
            }
        )
        likelihood_mc = ne.evaluate(
            "sum(mcw * mcdata)", local_dict={
                "mcw": self.mcweight,
                "mcdata": mcdata
            }
        )
        return likelihood_data - self.__generated * likelihood_mc

    def __extended_likelihood_with_torch(self, params):
        data = self.__data_amplitude.calculate(params)
        mcdata = self.__monte_carlo_amplitude.calculate(params)
        likelihood_data = torch.sum(self.sweight * torch.log(data))
        likelihood_mc = torch.sum(self.mcweight * mcdata)
        return (
            likelihood_data - self.__generated * likelihood_mc
        ).cpu().detach().numpy()
