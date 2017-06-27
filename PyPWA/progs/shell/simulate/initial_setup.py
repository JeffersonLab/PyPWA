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
Translates the command object from the configurator into arguments that 
can be used by the Simulation package and its various objects.
"""

from PyPWA.progs.shell.simulate import _libs

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import option_tools
from PyPWA.core.configurator import options
from PyPWA.progs.shell import loaders
from PyPWA.progs.shell.simulate import pysimulate

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class SimulationSetup(options.Setup):

    def __init__(self, options_object):
        # type: (option_tools.CommandOptions) -> None
        self.__options = options_object

        self.__simulator = None  # type: pysimulate.Simulator
        self.__functions = None  # type: loaders.FunctionLoader
        self.__data_loader = None  # type: _libs.DataHandler

        self.__load_functions()
        self.__load_data()
        self.__set_interface()

    def __load_functions(self):
        the_type = self.__options.the_type

        if the_type == "full" or the_type == "intensities":
            self.__functions = loaders.FunctionLoader(
                self.__options.functions_location,
                self.__options.processing_name, self.__options.setup_name
            )

    def __load_data(self):
        self.__data_loader = _libs.DataHandler(
            self.__options.data_parser, self.__options.data_location,
            self.__options.save_name
        )

    def __set_interface(self):
        self.__simulator = pysimulate.Simulator(
            self.__data_loader, self.__options.the_type,
            self.__options.kernel_processing, self.__functions,
            self.__options.parameters, self.__options.max_intensity
        )

    def return_interface(self):
        # type: () -> pysimulate.Simulator
        return self.__simulator
