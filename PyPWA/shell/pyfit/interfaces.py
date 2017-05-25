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
These are the interfaces needed to define a new likelihood.
-----------------------------------------------------------

- Likelihood - used for the actual algorithm to calculate the likelihood.

- Setup - used to define how to interact with the likelihood and the name of 
  the likelihood.
"""

from typing import Any, Dict
from typing import Optional as Opt

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import internals
from PyPWA.shell import loaders
from PyPWA.shell import shell_types

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Likelihood(internals.Kernel):

    def __init__(self, setup_function=None):
        # type: (shell_types.users_setup) -> None
        self.__setup_function = setup_function

    def setup(self):
        # type: () -> None
        if self.__setup_function:
            self.__setup_function()

    def process(self, data=False):
        # type: (Dict[str, numpy.float64]) -> numpy.float64
        raise NotImplementedError


class Setup(object):

    NAME = NotImplemented

    def setup_likelihood(
            self,
            data_package,  # type: loaders.DataLoading
            function_package,  # type: loaders.FunctionLoader
            extra_info=None  # type: Opt[Dict[str, Any]]
    ):
        # type: (...) -> None
        raise NotImplementedError

    def get_likelihood(self):
        # type: () -> Likelihood
        raise NotImplementedError

    def get_data(self):
        # type: () -> Dict[str, numpy.ndarray]
        raise NotImplementedError
