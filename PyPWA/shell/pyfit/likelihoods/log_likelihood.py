# coding=utf-8
#
# PyPWA, a scientific analysis toolkit.
# Copyright (C) 2016  JLab
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
The Log-Likelihood Extended and UnExtended are defined here:
- UnExtended Σln(Q*B*I°(D))
- Extended Σln(Q*I°(D)) - 1/total_number * Σ(I°(MC))
"""

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.shell import loaders
from PyPWA.shell.pyfit import interfaces

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class LogLikelihood(interfaces.Setup):

    name = "Log Likelihood"
    _data = None  # type: loaders.DataLoading
    _functions = None  # type: loaders.FunctionLoader
    __generated_length = None  # type: int
    _dictionary_data = None  # type: dict
    _likelihood = None  # type: interfaces.Likelihood

    def __init__(self, data_package, function_package, extra_info):
        self._data = data_package
        self._functions = function_package
        self.__generated_length = extra_info["Generated Length"]

    def setup_interface(self):
        self.__setup_data()
        self.__setup_likelihood()

    def __setup_data(self):
        self._dictionary_data = dict()
        self._dictionary_data["data"] = self._data.data
        self._dictionary_data["qfactor"] = self._data.qfactor
        self._dictionary_data["binned"] = self._data.binned
        if self._data.monte_carlo:
            self._dictionary_data["monte_carlo"] = self._data.monte_carlo

    def __setup_likelihood(self):
        if self._data.monte_carlo:
            self.__setup_extended_monte_carlo()
        else:
            self.__setup_standard_likelihood()

    def __setup_extended_monte_carlo(self):
        self._likelihood = ExtendedLikelihoodAmplitude(
            self._functions.setup, self._functions.process,
            self.__generated_length
        )

    def __setup_standard_likelihood(self):
        self._likelihood = UnExtendedLikelihoodAmplitude(
            self._functions.setup, self._functions.process
        )


class ExtendedLikelihoodAmplitude(interfaces.Likelihood):
    __processed = 0  # type: numpy.float64
    data = None  # type: numpy.ndarray
    monte_carlo = None  # type: numpy.ndarray
    qfactor = 1  # type: numpy.ndarray

    def __init__(
            self, setup_function, processing_function, generated_length
    ):
        super(ExtendedLikelihoodAmplitude, self).__init__(
            setup_function, processing_function
        )

        self.__processed = 1.0 / generated_length

    def process(self, data=False):
        processed_data = self._processing_function(self.data, data)
        processed_monte_carlo = self._processing_function(
            self.monte_carlo, data
        )

        return self.__likelihood(processed_data, processed_monte_carlo)

    def __likelihood(self, data, monte_carlo):
        self.__check_data_for_zeros(data)

        return self.__process_log_likelihood(data) + \
            self.__process_monte_carlo(monte_carlo)

    @staticmethod
    def __check_data_for_zeros(data):
        if numpy.any(data == 0):
            print("WARNING, Found Zeros! " + repr(
                numpy.count_nonzero(data == 0)
            ))

    def __process_log_likelihood(self, data):
        return numpy.sum(self.qfactor * numpy.log(data))

    def __process_monte_carlo(self, monte_carlo):
        return self.__processed * numpy.sum(monte_carlo)


class UnExtendedLikelihoodAmplitude(interfaces.Likelihood):
    data = None  # type: numpy.ndarray
    qfactor = 1  # type: numpy.ndarray
    binned = 1  # type: numpy.ndarray

    def __init__(self, setup_function, processing_function):
        super(UnExtendedLikelihoodAmplitude, self).__init__(
            setup_function, processing_function
        )

    def process(self, data=False):
        processed_data = self._processing_function(self.data, data)
        return self.__likelihood(processed_data)

    def __likelihood(self, data):
        value = numpy.sum(self.qfactor * self.binned * numpy.log(data))
        return value
