#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import iminuit
import numpy
import tabulate
import logging

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs.templates import interface_templates
from PyPWA.core_libs.templates import plugin_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Minuit(plugin_templates.MinimizerTemplate):

    def __init__(
            self, calc_function=False, parameters=False, settings=False,
            fitting_type=False, strategy=1, number_of_calls=10000,
            **options
    ):
        """
        Object based off of iminuit, provides an easy way to run
        minimization

        Args:
            calc_function (function): function that holds the
                calculations.
            parameters (list): List of the parameters
            settings (dict): Dictionary of the settings for iminuit
            strategy (int): iminuit's strategy
            fitting_type (str): The type of fitting function, either
                likelihood or chisquared.
            number_of_calls (int): Max number of calls
            options (dict): The settings dictionary built from the users
                input and the plugin initializer.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._final_value = 0  # type: numpy.float64
        self._covariance = 0  # type: tuple
        self._values = 0
        self._set_up = 0

        self._calc_function = calc_function
        self._parameters = parameters
        self._settings = settings
        self._strategy = strategy
        self._number_of_calls = number_of_calls
        if options:
            super(Minuit, self).__init__(options)

    def main_options(self, calc_function, fitting_type=False):
        self._calc_function = calc_function
        self._error_def(fitting_type)

    def _check_params(self):
        if isinstance(self._parameters, bool):
            raise ValueError(
                "There are no supplied parameters! Please set "
                "'parameters' under 'Minuit' in your settings!"
            )
        self._logger.debug(
            "Found parameters: {0}".format(repr(self._parameters))
        )

    def _error_def(self, fitting_type):
        if fitting_type == "chi-squared":
            self._set_up = 1
        else:
            self._set_up = .5

    def start(self):
        """
        Method to call to start minimization process
        """
        self._check_params()

        self._logger.debug("Found settings: " + repr(self._settings))
        minimal = iminuit.Minuit(
            self._calc_function,
            forced_parameters=self._parameters,
            **self._settings
        )

        minimal.set_strategy(self._strategy)
        minimal.set_up(self._set_up)
        minimal.migrad(ncall=self._number_of_calls)
        self._final_value = minimal.fval
        self._covariance = minimal.covariance
        self._values = minimal.values

    def return_parser(self):
        """

        Returns:
            interface_templates.MinimizerParserTemplate
        """

        class ParserObject(interface_templates.MinimizerParserTemplate):

            def __init__(self, parameters):
                self._parameters = parameters

            def convert(self, *args):
                parameters_with_values = {}
                for parameter, arg in zip(self._parameters, args[0][0]):
                    parameters_with_values[parameter] = arg

                return parameters_with_values

        return ParserObject(self._parameters)

    def save_extra(self, save_name):
        if not isinstance(self._covariance, type(None)):
            print("Covariance.\n")
            the_x = []
            the_y = []
            for field in self._covariance:
                the_x.append(field[0])
                the_y.append(field[1])

            x_true = set(the_x)
            y_true = set(the_y)

            covariance = []
            for x in x_true:
                holding = [x]
                for y in y_true:
                    holding.append(self._covariance[(x, y)])
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
                stream.write("fval: "+str(self._final_value))

            numpy.save(save_name + ".npy", {
                "covariance": self._covariance,
                "fval": self._final_value,
                "values": self._values
            })
