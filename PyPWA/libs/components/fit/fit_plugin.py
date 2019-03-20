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

from enum import Enum
from typing import Dict, Optional as Opt

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.components.process import templates
from PyPWA.progs.shell import shell_types

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class LikelihoodType(Enum):
    OTHER = 1
    CHI_SQUARED = 2
    LOG_LIKELIHOOD = 3


class OptimizerType(Enum):
    MINIMIZER = 1
    MAXIMIZER = 2


class Likelihood(templates.Kernel):

    def __init__(self, setup_function: Opt[shell_types.users_setup] = None):
        self.__setup_function = setup_function

    def setup(self) -> None:
        if self.__setup_function:
            self.__setup_function()

    def process(self, data: Dict[str, numpy.float64] = False) -> float:
        raise NotImplementedError


class Setup:

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def type(self) -> LikelihoodType:
        raise NotImplementedError

    def get_likelihood(
            self,
            optimizer_type: OptimizerType,
            data: FitData,
            functions: CallPackage
    ) -> Likelihood:
        raise NotImplementedError

    def get_data_dictionary(self, data: FitData) -> Dict[str, numpy.ndarray]:
        raise NotImplementedError
