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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.configurator import options
from PyPWA.shell import loaders
from PyPWA.shell.pysimulate import _libs
from PyPWA.shell.pysimulate import pysimulate

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class SimulationSetup(options.Setup):

    __interface = None
    __options = None
    __functions = None
    __data_loader = None

    def __init__(self, options_object):
        self.__options = options_object
        self.__load_functions()
        self.__load_data()

    def __load_functions(self):
        the_type = self.__options.the_type

        if the_type == "full" or the_type == "intensities":
            self.__functions = loaders.FunctionLoader(
                self.__options.functions_location,
                self.__options.processing_name, self.__options.setup_name
            )

    def __load_data(self):
        self.__data_loader = _libs.DataHandler(
            self.__options.DATA_PARSER, self.__options.data_location,
            self.__options.save_name
        )

    def __set_interface(self):
        self.__interface = pysimulate.Simulator(
            self.__data_loader, self.__options.the_type,
            self.__options.KERNEL_PROCESSING, self.__functions,
            self.__options.parameters, self.__options.max_intensity
        )

    def return_interface(self):
        return self.__interface