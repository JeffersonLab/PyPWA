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
import numpy
from typing import Dict

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.components.fit import interfaces

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _LogLikelihoodMetadata(interfaces.Setup):

    @property
    def name(self):
        return "log-likelihood"

    @property
    def type(self):
        return interfaces.LikelihoodType.LOG_LIKELIHOOD

    def get_likelihood(self, optimizer_type, data, functions):
        multiplier = self.__get_multiplier(optimizer_type)

        if data.monte_carlo and data.generated_length:
            return _ExtendedLikelihoodAmplitude(
                functions, multiplier, data.generated_length
            )
        else:
            return _UnExtendedLikelihoodAmplitude(functions, multiplier)

    @staticmethod
    def __get_multiplier(optimizer_type):
        if optimizer_type is interfaces.OptimizerType.MINIMIZER:
            return -1
        else:
            return 1

    def get_data_dictionary(self, data):
        package = {"data": data.data}
        if data.binned:
            package["binned"] = data.binned
        if data.qfactor:
            package["qfactor"] = data.qfactor
        if data.monte_carlo:
            package["monte_carlo"] = data.monte_carlo
        return package


class _ExtendedLikelihoodAmplitude(interfaces.Likelihood):

    __LOGGER = logging.getLogger(__name__ + ".ExtendedLikelihoodAmplitude")

    def __init__(
            self,
            functions, # type: interfaces.FunctionPackage
            multiplier,  # type: int
            generated_length  # type: float
    ):
        # type: (...) -> None
        super(_ExtendedLikelihoodAmplitude, self).__init__(functions.setup)
        self.__processing_function = functions.process
        self.__multiplier = multiplier
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
        return self.__multiplier * (data_result + monte_carlo_result)

    def __process_log_likelihood(self, data):
        # type: (numpy.ndarray) -> float
        return numpy.sum(self.qfactor * numpy.log(data))

    def __process_monte_carlo(self, monte_carlo):
        # type: (numpy.ndarray) -> float
        return self.__processed * numpy.sum(monte_carlo)


class _UnExtendedLikelihoodAmplitude(interfaces.Likelihood):

    def __init__(self, functions, multiplier):
        # type: (interfaces.FunctionPackage, int) -> None
        super(_UnExtendedLikelihoodAmplitude, self).__init__(functions.setup)
        self.__processing_function = functions.process
        self.__multiplier = multiplier
        self.data = None  # type: numpy.ndarray
        self.qfactor = 1  # type: numpy.ndarray
        self.binned = 1  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        processed_data = self.__processing_function(self.data, data)
        likelihood = self.__likelihood(processed_data)
        return self.__multiplier * likelihood

    def __likelihood(self, data):
        # type: (numpy.ndarray) -> float
        processed = self.qfactor * self.binned * numpy.log(data)
        value = numpy.sum(processed)
        return value


metadata = _LogLikelihoodMetadata()
