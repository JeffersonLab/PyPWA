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

import logging

import numpy
import pymultinest
from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import interface_templates
from PyPWA.core_libs.templates import plugin_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class MultiNest(plugin_templates.MinimizerTemplate):
    """
    This will be elegant and amazing, eventually.
    """

    builtin_function = u"""\
The function with all the documentation required to build the parameter
space. Right now we don't understand this.
"""

    def __init__(
            self, prior_location=None, prior_name=None,
            number_of_parameters=None, options=None
    ):
        """

        Args:
            prior_location (str):
            prior_name (str):
            number_of_parameters (int):
            options (dict):
        """

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._prior_location = prior_location
        self._prior_name = prior_name
        self._number_of_parameters = number_of_parameters

        if options:
            super(MultiNest, self).__init__(options)

        self._prior_function = None  # type: object
        self._calculation_function = None  # type: object

    def main_options(self, calc_function, fitting_type=False):
        self._calculation_function = calc_function

    def start(self):
        self._load_function()

        pymultinest.run(
            self._calculation_function, self._prior_function,
            self._number_of_parameters
        )

    def _load_function(self):
        loader = plugin_loader.SingleFunctionLoader(self._prior_location)
        self._prior_function = loader.fetch_function(self._prior_name)

    def return_parser(self):
        class MultiNestParser(
            interface_templates.MinimizerParserTemplate
        ):

            def __init__(self):
                super(MultiNestParser, self).__init__()

            def convert(self, passed_value):
                new_cube = numpy.zeros(passed_value[2])

                for parameter in passed_value[2]:
                    new_cube[parameter] = passed_value[0][parameter]

                return new_cube
        return MultiNestParser()

    def save_extra(self, save_name):
        self._logger.info(
            "PyMultiNest Object doesn't support saving data as of this "
            "release."
        )