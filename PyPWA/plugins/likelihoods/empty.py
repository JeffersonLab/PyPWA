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
from typing import Dict

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.components.fit import interfaces

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _EmptyLikelihoodMetadata(interfaces.Setup):

    @property
    def name(self):
        return "empty"

    @property
    def type(self):
        return interfaces.LikelihoodType.OTHER

    def get_likelihood(self, optimizer_type, data, functions):
        return _Empty(functions)

    def get_data_dictionary(self, data):
        return {'data': data.data}


class _Empty(interfaces.Likelihood):

    def __init__(self, functions):
        super(_Empty, self).__init__(functions.setup)
        self.__processing_function = functions.process
        self.data = None  # type: numpy.ndarray

    def process(self, data=False):
        # type: (Dict[str, float]) -> float
        return numpy.sum(self.__processing_function(self.data, data))


metadata = _EmptyLikelihoodMetadata()
