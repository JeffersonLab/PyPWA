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

import sys
import enum
import logging
import multiprocessing
from typing import List

from PyPWA import VERSION, AUTHOR
from PyPWA.libs.components.process import templates

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ProcessCodes(enum.Enum):

    SHUTDOWN = 1
    ERROR = 2


class _AbstractProcess(multiprocessing.Process):

    def __init__(self):
        super(_AbstractProcess, self).__init__()
        self.daemon = True  # When true, processes will die with main

    def run(self):
        raise NotImplementedError


class Duplex(_AbstractProcess):

    __LOGGER = logging.getLogger(__name__ + ".Duplex")

    def __init__(self, kernel, connect):
        # type: (templates.Kernel, multiprocessing.Pipe) -> None
        super(Duplex, self).__init__()
        self.__kernel = kernel
        self.__connection = connect

    def run(self):
        try:
            self.__kernel.setup()
        except Exception as error:
            self.__handle_error(error)
            raise
        else:
            self.__loop()

    def __loop(self):
        while True:
            received = self.__connection.recv()
            if received == ProcessCodes.SHUTDOWN:
                self.__LOGGER.debug("Gracefully shutting down process.")
                sys.exit()
            self.__process(received)

    def __process(self, received_data):
        try:
            value = self.__kernel.process(received_data)
        except Exception as error:
            self.__handle_error(error)
            raise
        else:
            self.__connection.send(value)

    def __handle_error(self, error):
        # type: (Exception) -> None
        self.__connection.send(ProcessCodes.ERROR)
        self.__LOGGER.exception(error)


class Simplex(_AbstractProcess):

    __LOGGER = logging.getLogger(__name__ + ".Simplex")

    def __init__(self, single_kernel, connect):
        # type: (templates.Kernel, multiprocessing.Pipe) -> None
        super(Simplex, self).__init__()
        self.__kernel = single_kernel
        self.__connection = connect

    def run(self):
        try:
            self.__kernel.setup()
            self.__connection.send(self.__kernel.process())
        except Exception as error:
            self.__connection.send(ProcessCodes.ERROR)
            self.__LOGGER.exception(error)
            raise
        finally:
            self.__LOGGER.debug("Shutting Down.")


class ProcessInterface(object):

    __LOGGER = logging.getLogger(__name__ + "._ProcessInterface")

    def __init__(
            self,
            interface_kernel,  # type: templates.Interface
            process_com,  # type: List[multiprocessing.Pipe]
            processes  # type: List[multiprocessing.Process]
    ):
        # type: (...) -> None
        self.__connections = process_com
        self.__interface = interface_kernel
        self.__processes = processes

    def run(self, *args):
        return self.__interface.run(self.__connections, args)

    def stop(self, force=False):
        if self.__interface.IS_DUPLEX and not force:
            self.__ask_processes_to_stop()
        else:
            self.__terminate_processes()

    def __ask_processes_to_stop(self):
        for connection in self.__connections:
            self.__LOGGER.debug("Attempting to kill processes.")
            connection.send(ProcessCodes.SHUTDOWN)

    def __terminate_processes(self):
        self.__LOGGER.debug("Terminating Processes is Risky!")
        for process in self.__processes:
            process.terminate()

    @property
    def is_alive(self):
        for process in self.__processes:
            if process.is_alive():
                return True
        return False
