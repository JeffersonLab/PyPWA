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

from PyPWA.core.configurator import options
from PyPWA.builtin_plugins.minuit import minimization
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class MinuitSetup(options.Setup):

    __command = None
    __interface = None

    def __init__(self, command):
        self.__command = command

    def __setup_interface(self):
        self.__interface = minimization.Minuit(
            parameters=self.__command.parameters,
            settings=self.__command.settings,
            strategy=self.__command.strategy,
            number_of_calls=self.__command.number_of_calls
        )

    def return_interface(self):
        return self.__interface