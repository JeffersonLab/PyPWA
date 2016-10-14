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

"""
Holds the various likelihood calculations.
"""
import os

import logging

import numpy

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.shell.fitting import calculations
from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import plugin_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Fitting(plugin_templates.ShellMain):

    def __init__(
            self, data_parser=None, minimization=None,
            kernel_processing=None, likelihood_type=None,
            generated_length=None, functions_location=None,
            processing_name=None, setup_name=None, data_location=None,
            accepted_monte_carlo_location=None, save_name=None, **options
    ):
        """

        Args:
            data_parser (plugin_templates.DataParserTemplate):
            minimization (plugin_templates.MinimizerTemplate):
            kernel_processing (plugin_templates.KernelProcessingTemplate):
            likelihood_type (str):
            generated_length (int):
            functions_location (str):
            processing_name (str):
            setup_name (str):
            data_location (str):
            accepted_monte_carlo_location (str):
            save_name (str):
            options (dict):
        """

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._data_parser = data_parser
        self._minimization = minimization
        self._kernel_processing = kernel_processing
        self._likelihood_type = likelihood_type
        self._generated_length = generated_length
        self._functions_location = functions_location
        self._processing_name = processing_name
        self._setup_name = setup_name
        self._data_location = data_location
        self._accepted_monte_carlo_location \
            = accepted_monte_carlo_location
        self._save_name = save_name
        if options:
            super(Fitting, self).__init__(options)

        self._monte_carlo_raw_data = None  # type: numpy.ndarray
        self._data_raw_data = None  # type: numpy.ndarray
        self._corrected_data = None  # type: dict
        self._processing_function = None  # type: object
        self._setup_function = None  # type: object

    def _check_params(self):
        if isinstance(self._functions_location, type(None)):
            raise ValueError(
                "Received nothing for the function's location! \n"
                "Set 'function's location' under 'General Fitting'"
            )
        if not os.path.exists(os.path.abspath(self._functions_location)):
            raise ValueError(
                "The 'function's location' doesn't point to a valid path!"
            )

    def _load_data(self):
        self._data_raw_data = self._data_parser.parse(self._data_location)

        if self._accepted_monte_carlo_location:
            self._monte_carlo_raw_data = self._data_parser.parse(
                self._accepted_monte_carlo_location
            )

    def _load_functions(self):
        loader = plugin_loader.SingleFunctionLoader(
            self._functions_location
        )

        self._processing_function = loader.fetch_function(
            self._processing_name, True
        )

        self._setup_function = loader.fetch_function(
            self._setup_name, False
        )

    def start(self):
        self._check_params()
        self._load_data()
        self._setup_data()
        self._load_functions()

        minimizer_parser = self._minimization.return_parser()

        interface_kernel = calculations.FittingInterfaceKernel(
            minimizer_parser
        )

        if self._likelihood_type is "chi-squared":
            self._start_chi(interface_kernel)
        else:
            self._start_likelihood(interface_kernel)

    def _start_chi(self, interface_kernel):
        chi_kernel = calculations.Chi(
            self._setup_function, self._processing_function
        )

        self._kernel_processing.main_options(
            self._corrected_data, chi_kernel, interface_kernel
        )

        interface = self._kernel_processing.fetch_interface()

        self._the_end(interface, "chi-squared")

    def _start_likelihood(self, interface_kernel):
        if "monte_carlo" in list(self._corrected_data.keys()):
            kernel = calculations.ExtendedLikelihoodAmplitude(
                self._setup_function, self._processing_function,
                self._generated_length
            )
        else:
            kernel = calculations.UnextendedLikelihoodAmplitude(
                self._setup_function, self._processing_function
            )

        self._kernel_processing.main_options(
            self._corrected_data, kernel, interface_kernel
        )

        interface = self._kernel_processing.fetch_interface

        self._the_end(interface, "likelihood")

    def _the_end(self, interface, fitting_type):
        """

        Args:
            interface (interface_:

        Returns:

        """
        self._minimization.main_options(interface.run, fitting_type)

        self._minimization.start()
        interface.stop()
        self._minimization.save_extra(self._save_name)

    def _setup_data(self):
        corrected = {}

        corrected_data = self._filter_data(
            self._data_raw_data, "data"
        )

        if isinstance(self._monte_carlo_raw_data, numpy.ndarray):
            corrected_monte_carlo = self._filter_data(
                self._monte_carlo_raw_data, "monte_carlo"
            )

            for key in list(corrected_monte_carlo.keys()):
                corrected[key] = corrected_monte_carlo[key]

        for key in list(corrected_data.keys()):
            corrected[key] = corrected_data[key]

        self._corrected_data = corrected_data

    @staticmethod
    def _filter_data(array, main_name):
        """

        Args:
            array (numpy.ndarray):

        Returns:

        """
        if "BinN" in array.dtype.names:
            where_zero = numpy.where(array["BinN"] == 0)[0]

            for key in array.dtype.names:
                array[key] = numpy.delete(array[key], where_zero)

        names_list = list(array.dtype.names)
        segregated_data = {}

        if "QFactor" in names_list:
            names_list.remove("QFactor")
            segregated_data["qfactor"] = array["QFactor"]

        if "BinN" in names_list:
            names_list.remove("BinN")
            segregated_data["binned"] = array["BinN"]

        segregated_data[main_name] = array[names_list]

        return segregated_data