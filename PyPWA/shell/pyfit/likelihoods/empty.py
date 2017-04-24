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

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.shell import loaders
from PyPWA.shell.pyfit import interfaces

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class EmptyLikelihood(interfaces.Setup):
    name = "empty"
    _data = None  # type: loaders.DataLoading
    _functions = None  # type: loaders.FunctionLoader
    _dictionary_data = None  # type: dict
    _likelihood = None  # type: interfaces.Likelihood

    def __init__(self, data_package, function_package, extra_info):
        self._data = data_package
        self._functions = function_package

    def setup_interface(self):
        self.__setup_data()
        self.__setup_likelihood()

    def __setup_data(self):
        self._dictionary_data = dict()
        self._dictionary_data["data"] = self._data.data

    def __setup_likelihood(self):
        self._likelihood = Empty(
            self._functions.setup, self._functions.process
        )


class Empty(interfaces.Likelihood):

    data = None  # type: numpy.ndarray

    def __init__(self, setup_function, processing_function):
        super(Empty, self).__init__(setup_function, processing_function)

    def process(self, data=False):
        return numpy.sum(self._processing_function(self.data, data))
