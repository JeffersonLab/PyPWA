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
The processes and their factories are defined here. The current supported
methods are Duplex for worker processes and Simplex for offload processes.
"""
from PyPWA.core.shared.interfaces import internals
from PyPWA.builtin_plugins.process.communication import _interface
import multiprocessing

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Duplex(multiprocessing.Process):

    daemon = True  # When true, processes will die with main

    __kernel = None
    __communicator = None

    __should_calculate = True
    __received_value = None

    def __init__(self, kernel, communicator):
        super(Duplex, self).__init__()
        self.__kernel = kernel
        self.__communicator = communicator

    def run(self):
        self.__kernel.setup()
        self.__loop()
        return 0

    def __loop(self):
        while self.__should_calculate:
            self.__get_value()
            if self.__received_value == "DIE":
                self.__should_calculate = False
            else:
                self.__process()

    def __get_value(self):
        value = self.__communicator.receive()
        self.__received_value = value

    def __process(self):
        processed_data = self.__kernel.process(self.__received_value)
        self.__communicator.send(processed_data)


class Simplex(multiprocessing.Process):

    daemon = True  # When true, processes will die with main
    __kernel = None  # type: internals.Kernel
    __communicator = None  # type: _interface._Communication

    def __init__(self, single_kernel, communicator):
        super(Simplex, self).__init__()
        self.__kernel = single_kernel
        self.__communicator = communicator

    def run(self):
        self.__kernel.setup()
        self.__communicator.send(self.__kernel.process())
        return 0

    def _process(self):
        processed_data = self.__kernel.process()
        self.__communicator.send(processed_data)
