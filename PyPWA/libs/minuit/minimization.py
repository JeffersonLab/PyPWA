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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs import templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Minuit(templates.MinimizerTemplate):

    def __init__(
            self, calc_function=False, parameters=False, settings=False,
            fitting_type=False, strategy=1, number_of_calls=10000,
            options=False
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
        self.final_value = 0
        self.covariance = 0
        self.values = 0
        self._set_up = 0

        self._calc_function = calc_function
        self._parameters = parameters
        self._settings = settings
        self._strategy = strategy
        self._number_of_calls = number_of_calls

        self._error_def(fitting_type)
        super(Minuit, self).__init__(options)

    def main_options(self, calc_function, fitting_type=False):
        self._calc_function = calc_function
        self._error_def(fitting_type)

    def _error_def(self, fitting_type):
        if fitting_type == "chisquared":
            self._set_up = 1
        else:
            self._set_up = .5

    def start(self):
        """
        Method to call to start minimization process
        """
        minimal = iminuit.Minuit(
            self._calc_function,
            forced_parameters=self._parameters,
            **self._settings
        )

        minimal.set_strategy(self._strategy)
        minimal.set_up(self._set_up)
        minimal.migrad(ncall=self._number_of_calls)
        self.final_value = minimal.fval
        self.covariance = minimal.covariance
        self.values = minimal.values

    def convert(self, passed_value):
        parameters_with_values = {}
        for parameter, arg in zip(self._parameters, passed_value):
            parameters_with_values[parameter] = arg

        return parameters_with_values
