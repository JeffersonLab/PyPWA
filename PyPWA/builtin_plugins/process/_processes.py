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
This are where the actual processes are defined
-----------------------------------------------
- _AbstractProcess - The abstract process that the other processes subclass,
  this defines both the interface for the subclasses, and sets daemon mode to
  true so that processes will shutdown with the main process.
- Duplex - The duplex process, this process will take information received
  from the main process and calculate over it.
- Simplex - The Simplex process, this process will calculate over whatever
  is in its kernel the moment it starts, then return the calculated value
  over its pipe.
"""

import logging
import multiprocessing
from typing import Any

from PyPWA import VERSION, AUTHOR
from PyPWA.libs.interfaces import kernel

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _AbstractProcess(multiprocessing.Process):

    def __init__(self):
        # type: (kernel.Kernel, multiprocessing.Pipe) -> None
        super(_AbstractProcess, self).__init__()
        self.daemon = True  # When true, processes will die with main

    def run(self):
        raise NotImplementedError


class Duplex(_AbstractProcess):

    __LOGGER = logging.getLogger(__name__ + ".Duplex")

    def __init__(self, kernel, connect):
        # type: (kernel.Kernel, multiprocessing.Pipe) -> None
        super(Duplex, self).__init__()
        self.__kernel = kernel
        self.__connection = connect
        self.__received_value = None

    def run(self):
        self.__kernel.setup()
        self.__loop()

    def __loop(self):
        while True:
            self.__get_value()
            if self.__received_value == kernel.ProcessCodes.SHUTDOWN:
                self.__LOGGER.debug("Gracefully shutting down process.")
                break
            self.__process()

    def __get_value(self):
        self.__received_value = self.__connection.recv()

    def __process(self):
        try:
            value = self.__run_kernel()
        except Exception as error:
            self.__handle_error(error)
        else:
            self.__connection.send(value)

    def __run_kernel(self):
        # type: () -> Any
        return self.__kernel.process(self.__received_value)

    def __handle_error(self, error):
        # type: (Exception) -> None
        self.__connection.send(kernel.ProcessCodes.ERROR)
        self.__LOGGER.exception(error)
        self.__LOGGER.critical(
            "Child process in critical state! The program will crash!"
        )
        raise error


class Simplex(_AbstractProcess):

    __LOGGER = logging.getLogger(__name__ + ".Simplex")

    def __init__(self, single_kernel, connect):
        # type: (kernel.Kernel, multiprocessing.Pipe) -> None
        super(Simplex, self).__init__()
        self.__kernel = single_kernel
        self.__connection = connect

    def run(self):
        self.__kernel.setup()
        self.__process()
        self.__LOGGER.debug("Shutting Down.")

    def __process(self):
        try:
            self.__connection.send(self.__kernel.process())
        except Exception as error:
            self.__connection.send(kernel.ProcessCodes.ERROR)
            self.__LOGGER.exception(error)
            raise error
