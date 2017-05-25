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
Defines how the configurator will interact with PyFit.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options
from PyPWA.shell import loaders
from PyPWA.shell.pyfit import pyfit

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class FittingSetup(options.Setup):

    def __init__(self, options_object):
        self.__options = options_object
        self.__interface = None  # type: pyfit.Fitting
        self.__data_loader = None  # type: loaders.DataLoading
        self.__functions = None  # type: loaders.FunctionLoader
        self.__run_setup()

    def __run_setup(self):
        self.__load_data()
        self.__load_functions()
        self.__setup_interface()

    def __load_data(self):
        self.__data_loader = loaders.DataLoading(
            self.__options.data_parser, self.__options.data_location,
            self.__options.internal_data, self.__options.qfactor_location,
            self.__options.accepted_monte_carlo_location
        )

    def __load_functions(self):
        self.__functions = loaders.FunctionLoader(
            self.__options.functions_location, self.__options.processing_name,
            self.__options.setup_name
        )

    def __setup_interface(self):
        self.__interface = pyfit.Fitting(
            self.__options.optimizer, self.__options.kernel_processing,
            self.__data_loader, self.__functions,
            self.__options.likelihood_type, self.__options.generated_length,
            self.__options.save_name
        )

    def return_interface(self):
        # type: () -> pyfit.Fitting
        return self.__interface
