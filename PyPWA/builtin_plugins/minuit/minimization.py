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
from PyPWA.libs.components.optimizers import opt_plugins
from PyPWA.libs import configuration_db

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ParserObject(opt_plugins.OptionParser):

    def __init__(self):
        self.__parameters = configuration_db.Connector().read(
            "Optimizer", "parameters"
        )

    def convert(self, *args):
        # type: (Tuple[Tuple[List[float]]]) -> Dict[str, float]
        parameters_with_values = {}
        for parameter, arg in zip(self.__parameters, args[0][0]):
            parameters_with_values[parameter] = arg

        return parameters_with_values


class Minuit(opt_plugins.Optimizer):

    __LOGGER = logging.getLogger(__name__ + ".Minuit")

    def __init__(self):
        # type: () -> None
        self.__final_value = 0  # type: numpy.float64
        self.__covariance = 0  # type: tuple
        self.__values = 0  # type: float
        self.__set_up = 0  # type: float

        self.__db = configuration_db.Connector()
        self.__save_data = _save_data.SaveData()

    def run(self, calculation_function, fitting_type=None):
        # type: (Callable[Any], opt_plugins.Likelihood) -> None
        self.__error_def(fitting_type)
        self.__log_information()
        self.__execute_minimizer(calculation_function)

    def __error_def(self, fitting_type):
        # type: (opt_plugins.Likelihood) -> None
        if fitting_type is opt_plugins.Likelihood.CHI_SQUARED:
            self.__set_up = 1
        else:
            self.__set_up = .5

    def __log_information(self):
        settings, strategy, max_iterations, parameters = self.__load_data()
        self.__LOGGER.debug("Found settings: %s" % repr(settings))
        self.__LOGGER.info("Running with strategy: %d" % strategy)
        self.__LOGGER.debug("Settings max iterations to: %d" % max_iterations)
        self.__LOGGER.info("Found parameters: %s" % repr(parameters))

    def __load_data(self):
        # type: () -> Tuple[Dict[str, Any], int, int, List[str]]
        settings = self.__db.read("minuit", "settings")
        strategy = self.__db.read("minuit", "strategy")
        max_iterations = self.__db.read("minuit", "number of calls")
        parameters = self.__db.read("minuit", "parameters")
        return settings, strategy, max_iterations, parameters

    def __execute_minimizer(self, calculation_function):
        settings, strategy, max_iterations, parameters = self.__load_data()

        minimal = iminuit.Minuit(
            calculation_function, forced_parameters=parameters,
            **settings
        )

        minimal.set_strategy(strategy)
        minimal.set_up(self.__set_up)
        minimal.migrad(ncall=max_iterations)

        self.__final_value = minimal.fval
        self.__covariance = minimal.covariance
        self.__values = minimal.values


    def save_data(self, save_name):
        # type: (str) -> None
        if not isinstance(self.__covariance, type(None)):
            self.__save_data.save_data(
                save_name, self.__covariance,
                self.__final_value, self.__values
            )
