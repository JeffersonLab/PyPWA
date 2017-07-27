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
A python a cython minimizer
---------------------------
Attempts to find a minima, for information about how it works read Iminuit's
documentation online.

- _ParserObject - Translates the received value inside run to something the
  user can easily interact with.
- Minuit - The main optimizer object.
"""

import logging
from typing import Any, Callable, Dict, List, Tuple

import iminuit
import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.minuit import _save_data
from PyPWA.libs.interfaces import optimizers

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ParserObject(optimizers.OptimizerOptionParser):

    def __init__(self, parameters):
        # type: (List[str]) -> None
        self._parameters = parameters

    def convert(self, *args):
        # type: (Tuple[Tuple[List[float]]]) -> Dict[str, float]
        parameters_with_values = {}
        for parameter, arg in zip(self._parameters, args[0][0]):
            parameters_with_values[parameter] = arg

        return parameters_with_values


class Minuit(optimizers.Optimizer):

    OPTIMIZER_TYPE = optimizers.OptimizerTypes.MINIMIZER

    __LOGGER = logging.getLogger(__name__ + ".Minuit")

    def __init__(
            self,
            parameters=False,  # type: List[str]
            settings=False,  # type: Dict[str, Any]
            strategy=1,  # type: int
            number_of_calls=10000,  # type: int
    ):
        # type: (...) -> None
        self.__save_data = _save_data.SaveData()
        self.__parameters = parameters
        self.__settings = settings
        self.__strategy = strategy
        self.__number_of_calls = number_of_calls

        self.__final_value = 0  # type: numpy.float64
        self.__covariance = 0  # type: tuple
        self.__values = 0  # type: float
        self.__set_up = 0  # type: float
        self.__calc_function = None  # type: Callable[[List[str]], float]

    def main_options(
            self,
            calc_function,  # type: Callable[[List[str], float]]
            fitting_type=False  # type: optimizers.LikelihoodTypes
    ):
        # type: (...) -> None
        self.__calc_function = calc_function
        self.__error_def(fitting_type)

    def __check_params(self):
        if isinstance(self.__parameters, bool):
            raise ValueError(
                "There are no supplied parameters! Please set "
                "'parameters' under 'Minuit' in your settings!"
            )
        self.__LOGGER.debug(
            "Found parameters: {0}".format(repr(self.__parameters))
        )

    def __error_def(self, fitting_type):
        # type: (optimizers.LikelihoodTypes) -> None
        if fitting_type is optimizers.LikelihoodTypes.CHI_SQUARED:
            self.__set_up = 1
        else:
            self.__set_up = .5

    def start(self):
        self.__check_params()

        self.__LOGGER.debug("Found settings: " + repr(self.__settings))
        minimal = iminuit.Minuit(
            self.__calc_function,
            forced_parameters=self.__parameters,
            **self.__settings
        )

        minimal.set_strategy(self.__strategy)
        minimal.set_up(self.__set_up)
        minimal.migrad(ncall=self.__number_of_calls)

        self.__final_value = minimal.fval
        self.__covariance = minimal.covariance
        self.__values = minimal.values

    def return_parser(self):
        # type: () -> _ParserObject
        return _ParserObject(self.__parameters)

    def save_extra(self, save_name):
        # type: (str) -> None
        if not isinstance(self.__covariance, type(None)):
            self.__save_data.save_data(
                save_name, self.__covariance, self.__final_value,
                self.__values
            )
