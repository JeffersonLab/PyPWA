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
The ChiSquared Likelihood is defined here:
------------------------------------------
- Σ(((I°(D) - B)^2) / B)
- Σ(((I°(D) - M)^2) / E^2)
"""

import numpy
from typing import Dict

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.components.fit import fit_plugin

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ChiLikelihoodMetadata(fit_plugin.Setup):

    @property
    def name(self):
        return "chi-squared"

    @property
    def type(self):
        return fit_plugin.LikelihoodType.CHI_SQUARED

    def get_likelihood(self, optimizer_type, data, functions):
        multiplier = self.__setup_multiplier(optimizer_type)
        if data.binned is not None:
            return _Chi(functions, multiplier)
        elif data.expected_values is not None:
            return _UnBinnedChi(functions, multiplier)
        raise ValueError("Chi needs Binned or Expected/Errors set!")

    @staticmethod
    def __setup_multiplier(optimizer_type):
        if optimizer_type is fit_plugin.LikelihoodType.MAXIMIZER:
            return -1
        else:
            return 1

    def get_data_dictionary(self, data):
        package = {"data": data.data}

        if data.binned is not None:
            package['binned'] = data.binned
        elif data.expected_values is not None:
            package['event errors'] = data.events_errors
            package['expected values'] = data.expected_values
        return package


class _Chi(interfaces.Likelihood):

    def __init__(self, functions, multiplier):
        # type: (interfaces.FunctionPackage, int) -> None
        super(_Chi, self).__init__(functions.setup)
        self.__processing_function = functions.process
        self.__multiplier = multiplier
        self.data = None  # type: numpy.ndarray
        self.binned = None  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        intensity = self.__processing_function(self.data, data)
        likelihood = self.__likelihood(intensity)
        return self.__multiplier * likelihood

    def __likelihood(self, data):
        # type: (numpy.ndarray) -> float
        return numpy.sum(((data - self.binned)**2) / self.binned)


class _UnBinnedChi(interfaces.Likelihood):

    def __init__(self, functions, multiplier):
        # type: (interfaces.FunctionPackage, int) -> None
        super(_UnBinnedChi, self).__init__(functions.setup)
        self.__processing_function = functions.process
        self.__multiplier = multiplier
        self.data = None  # type: numpy.ndarray
        self.expected = None  # type: numpy.ndarray
        self.error = None  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        intensity = self.__processing_function(self.data, data)
        likelihood = self.__likelihood(intensity)
        return self.__multiplier * likelihood

    def __likelihood(self, data):
        # type: (numpy.ndarray) -> float
        return numpy.sum(((data - self.expected)**2) / self.error)


metadata = _ChiLikelihoodMetadata()
