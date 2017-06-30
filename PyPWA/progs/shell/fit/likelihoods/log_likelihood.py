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
The Log-Likelihood Extended and UnExtended are defined here:
------------------------------------------------------------
- UnExtended Σln(Q*B*I°(D))
- Extended Σln(Q*I°(D)) - 1/total_number * Σ(I°(MC))
"""

import logging
from typing import Any, Dict
from typing import Optional as Opt
import warnings
import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.progs.shell import loaders
from PyPWA.progs.shell.fit import interfaces

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class LogLikelihood(interfaces.Setup):

    NAME = "likelihood"

    def __init__(self):
        self.__data = dict()  # type: Dict[str, numpy.ndarray]
        self.__generated_length = None  # type: float
        self.__likelihood = None  # type: interfaces.Likelihood

    def setup_likelihood(
            self,
            data_package,  # type: loaders.DataLoading
            function_package,  # type: loaders.FunctionLoader
            extra_info=None  # type: Opt[Dict[str, Any]]
    ):
        # type: (...) -> None
        self.__setup_data(data_package)
        self.__extract_generated_length(extra_info)
        self.__setup_likelihood(function_package)

    def __setup_data(self, data_package):
        # type: (loaders.DataLoading) -> None
        self.__data["data"] = data_package.data
        self.__data["qfactor"] = data_package.qfactor
        self.__data["binned"] = data_package.binned
        if isinstance(data_package.monte_carlo, numpy.ndarray):
            self.__data["monte_carlo"] = data_package.monte_carlo

    def __extract_generated_length(self, extra_info):
        # type: (Dict[str, float]) -> None
        if extra_info:
            self.__generated_length = extra_info["generated length"]

    def __setup_likelihood(self, function_package):
        # type: (loaders.FunctionLoader) -> None
        if "monte_carlo" in self.__data:
            self.__setup_extended_monte_carlo(function_package)
        else:
            self.__setup_standard_likelihood(function_package)

    def __setup_extended_monte_carlo(self, function_package):
        # type: (loaders.FunctionLoader) -> None
        self.__likelihood = ExtendedLikelihoodAmplitude(
            function_package.setup, function_package.process,
            self.__generated_length
        )

    def __setup_standard_likelihood(self, function_package):
        # type: (loaders.FunctionLoader) -> None
        self.__likelihood = UnExtendedLikelihoodAmplitude(
            function_package.setup, function_package.process
        )

    def get_data(self):
        # type: () -> Dict[str, numpy.ndarray]
        return self.__data

    def get_likelihood(self):
        # type: () -> interfaces.Likelihood
        return self.__likelihood


class ExtendedLikelihoodAmplitude(interfaces.Likelihood):

    __LOGGER = logging.getLogger(__name__ + ".ExtendedLikelihoodAmplitude")

    def __init__(
            self,
            setup_function,  # type: shell_types.users_setup
            processing_function,  # type: shell_types.users_processing
            generated_length  # type: float
    ):
        # type: (...) -> None
        super(ExtendedLikelihoodAmplitude, self).__init__(setup_function)
        self.__processing_function = processing_function
        self.__processed = 1.0 / generated_length
        self.data = None  # type: numpy.ndarray
        self.monte_carlo = None  # type: numpy.ndarray
        self.qfactor = 1  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        processed_data = self.__processing_function(self.data, data)
        processed_monte_carlo = self.__processing_function(
            self.monte_carlo, data
        )
        return self.__likelihood(processed_data, processed_monte_carlo)

    def __likelihood(self, data, monte_carlo):
        # type: (numpy.ndarray, numpy.ndarray) -> float
        data_result = self.__process_log_likelihood(data)
        monte_carlo_result = self.__process_monte_carlo(monte_carlo)
        return data_result + monte_carlo_result

    def __process_log_likelihood(self, data):
        # type: (numpy.ndarray) -> float
        return numpy.sum(self.qfactor * numpy.log(data))

    def __process_monte_carlo(self, monte_carlo):
        # type: (numpy.ndarray) -> float
        return self.__processed * numpy.sum(monte_carlo)


class UnExtendedLikelihoodAmplitude(interfaces.Likelihood):

    def __init__(
            self,
            setup_function,  # type: shell_types.users_setup
            processing_function  # type: shell_types.users_processing
    ):
        # type: (...) -> None
        super(UnExtendedLikelihoodAmplitude, self).__init__(setup_function)
        self.__processing_function = processing_function
        self.data = None  # type: numpy.ndarray
        self.qfactor = 1  # type: numpy.ndarray
        self.binned = 1  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        processed_data = self.__processing_function(self.data, data)
        return self.__likelihood(processed_data)

    def __likelihood(self, data):
        # type: (numpy.ndarray) -> float
        processed = self.qfactor * self.binned * numpy.log(data)
        value = numpy.sum(processed)
        return value
