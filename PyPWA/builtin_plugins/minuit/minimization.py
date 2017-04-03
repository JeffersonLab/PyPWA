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
--------------------------
Attempts to find a minima, for information about how it works read Iminuit's
documentation online.

- _ParserObject - Translates the received value inside run to something the 
  user can easily interact with. 
  
- Minuit - The main optimizer object.
"""

import logging

import iminuit
import numpy
import tabulate

from PyPWA import AUTHOR, VERSION
from PyPWA.core.shared.interfaces import internals
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ParserObject(internals.OptimizerOptionParser):

    def __init__(self, parameters):
        self._parameters = parameters

    def convert(self, *args):
        parameters_with_values = {}
        for parameter, arg in zip(self._parameters, args[0][0]):
            parameters_with_values[parameter] = arg

        return parameters_with_values


class Minuit(plugins.Optimizer):

    __logger = logging.getLogger(__name__ + ".Minuit")

    __final_value = 0  # type: numpy.float64
    __covariance = 0  # type: tuple
    __values = 0
    __set_up = 0

    __calc_function = None
    __parameters = None
    __settings = None
    __strategy = None
    __number_of_calls = None

    def __init__(
            self, parameters=False, settings=False,
            strategy=1, number_of_calls=10000,
    ):
        self.__logger.addHandler(logging.NullHandler())

        self.__parameters = parameters
        self.__settings = settings
        self.__strategy = strategy
        self.__number_of_calls = number_of_calls

    def main_options(self, calc_function, fitting_type=False):
        self.__calc_function = calc_function
        self.__error_def(fitting_type)

    def __check_params(self):
        if isinstance(self.__parameters, bool):
            raise ValueError(
                "There are no supplied parameters! Please set "
                "'parameters' under 'Minuit' in your settings!"
            )
        self.__logger.debug(
            "Found parameters: {0}".format(repr(self.__parameters))
        )

    def __error_def(self, fitting_type):
        if fitting_type == "chi-squared":
            self._set_up = 1
        else:
            self._set_up = .5

    def start(self):
        self.__check_params()

        self.__logger.debug("Found settings: " + repr(self.__settings))
        minimal = iminuit.Minuit(
            self.__calc_function,
            forced_parameters=self.__parameters,
            **self.__settings
        )

        minimal.set_strategy(self.__strategy)
        minimal.set_up(self._set_up)
        minimal.migrad(ncall=self.__number_of_calls)

        self.__final_value = minimal.fval
        self.__covariance = minimal.covariance
        self.__values = minimal.values

    def return_parser(self):
        return _ParserObject(self.__parameters)

    def save_extra(self, save_name):
        if not isinstance(self.__covariance, type(None)):
            print("Covariance.\n")
            the_x = []
            the_y = []
            for field in self.__covariance:
                the_x.append(field[0])
                the_y.append(field[1])

            x_true = set(the_x)
            y_true = set(the_y)

            covariance = []
            for x in x_true:
                holding = [x]
                for y in y_true:
                    holding.append(self.__covariance[(x, y)])
                covariance.append(holding)

            table_fancy = tabulate.tabulate(
                covariance, y_true, "fancy_grid", numalign="center"
            )

            table = tabulate.tabulate(
                covariance, y_true, "grid", numalign="center"
            )

            try:
                print(table_fancy)
            except UnicodeEncodeError:
                    print(table)

            with open(save_name + ".txt", "w") as stream:
                stream.write("Covariance.\n")
                stream.write(table)
                stream.write("\n")
                stream.write("fval: "+str(self.__final_value))

            numpy.save(
                save_name + ".npy", {
                    "covariance": self.__covariance,
                    "fval": self.__final_value,
                    "values": self.__values
                }
            )
