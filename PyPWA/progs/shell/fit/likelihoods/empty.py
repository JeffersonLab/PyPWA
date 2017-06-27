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
The Empty likelihood is defined here:
-------------------------------------
- Σ(I°(D))
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


class EmptyLikelihood(interfaces.Setup):

    NAME = "empty"

    def __init__(self):
        super(EmptyLikelihood, self).__init__()
        self.__data = dict()
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

    def __setup_likelihood(self, function_package):
        # type: (loaders.FunctionLoader) -> None
        self._likelihood = Empty(
            function_package.setup, function_package.process
        )

    def get_likelihood(self):
        # type: () -> interfaces.Likelihood
        return self.__likelihood

    def get_data(self):
        # type: () -> Dict[str, numpy.ndarray]
        return self.__data


class Empty(interfaces.Likelihood):

    def __init__(
            self,
            setup_function,  # type: shell_types.users_setup
            processing_function  # type: shell_types.users_processing
    ):
        super(Empty, self).__init__(setup_function)
        self.__processing_function = processing_function
        self.data = None  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        return numpy.sum(self.__processing_function(self.data, data))
