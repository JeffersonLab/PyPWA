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
"""

from typing import Any, Dict
from typing import Optional as Opt

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.progs.shell import loaders
from PyPWA.progs.shell.fit import interfaces

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ChiLikelihood(interfaces.Setup):

    NAME = "chi-squared"

    def __init__(self):
        super(ChiLikelihood, self).__init__()
        self.__data = dict()  # type: Dict[str, numpy.ndarray]
        self.__likelihood = None  # type: interfaces.Likelihood

    def setup_likelihood(
            self,
            data_package,  # type: loaders.DataLoading
            function_package,  # type: loaders.FunctionLoader
            extra_info=None  # type: Opt[Dict[str, Any]]
    ):
        # type: (...) -> None
        self.__setup_data(data_package)
        self.__setup_likelihood(function_package)

    def __setup_data(self, data_package):
        # type: (loaders.DataLoading) -> None
        self.__data["data"] = data_package.data
        self.__data["qfactor"] = data_package.qfactor
        self.__data["binned"] = data_package.binned
        self.__data["event errors"] = data_package.event_errors
        self.__data["expected values"] = data_package.expected_values

    def __setup_likelihood(self, function_package):
        # type: (loaders.FunctionLoader) -> None
        if not numpy.all(self.__data['binned'] == 1):
            self.__setup_chi(function_package)
        elif self.__event_and_error_data_exists():
            self.__setup_unbinned_chi(function_package)
        else:
            raise ValueError(
                "Given UnBinned data without expected value and error"
            )

    def __event_and_error_data_exists(self):
        expected = not numpy.all(self.__data['event errors'] == 1)
        errors = not numpy.all(self.__data['expected values'] == 1)
        return expected and errors

    def __setup_chi(self, function_package):
        # type: (loaders.FunctionLoader) -> None
        self.__likelihood = Chi(
            function_package.setup, function_package.process
        )

    def __setup_unbinned_chi(self, function_package):
        # type: (loaders.FunctionLoader) -> None
        self.__likelihood = UnBinnedChi(
            function_package.setup, function_package.process
        )

    def get_data(self):
        # type: () -> Dict[str, numpy.ndarray]
        return self.__data

    def get_likelihood(self):
        # type: () -> interfaces.Likelihood
        return self.__likelihood


class Chi(interfaces.Likelihood):

    def __init__(
            self,
            setup_function,  # type: shell_types.users_setup
            processing_function  # type: shell_types.users_processing
    ):
        # type: (...) -> None
        super(Chi, self).__init__(setup_function)
        self.__processing_function = processing_function
        self.data = None  # type: numpy.ndarray
        self.binned = None  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        processed_data = self.__processing_function(self.data, data)
        return self.__likelihood(processed_data)

    def __likelihood(self, data):
        # type: (numpy.ndarray) -> float
        return numpy.sum(((data - self.binned)**2) / self.binned)


class UnBinnedChi(interfaces.Likelihood):

    def __init__(
            self,
            setup_function,  # type: shell_types.users_setup
            processing_function  # type: shell_types.users_processing
    ):
        # type: (...) -> None
        super(UnBinnedChi, self).__init__(setup_function)
        self.__processing_function = processing_function
        self.data = None  # type: numpy.ndarray
        self.expected = None  # type: numpy.ndarray
        self.error = None  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        processed_data = self.__processing_function(self.data, data)
        return self.__likelihood(processed_data)

    def __likelihood(self, data):
        # type: (numpy.ndarray) -> float
        return numpy.sum(((data - self.expected)**2) / self.error)
