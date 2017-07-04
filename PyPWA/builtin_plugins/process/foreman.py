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
Kernel Based Processing
-----------------------
 - _ProcessingInterface - Interface between the processes and the requesting
   plugins.
 - CalculationForeman - Walks through the process of creating the processes
   using the provided kernel and data.
"""

import logging
import multiprocessing
from typing import Any, Dict, List

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.process import _data_split
from PyPWA.builtin_plugins.process import _kernel_setup
from PyPWA.builtin_plugins.process import _process_factory
from PyPWA.core.shared.interfaces import internals
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ProcessInterface(internals.ProcessInterface):

    __LOGGER = logging.getLogger(__name__ + "._ProcessInterface")

    def __init__(
            self,
            interface_kernel,  # type: internals.KernelInterface
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
            connection.send(internals.ProcessCodes.SHUTDOWN)

    def __terminate_processes(self):
        self.__LOGGER.debug("Terminating Processes is Risky!")
        for process in self.__processes:
            process.terminate()

    @property
    def is_alive(self):
        return self.__processes[0].is_alive()


class CalculationForeman(plugins.KernelProcessing):

    __LOGGER = logging.getLogger(__name__ + ".CalculationForeman")

    def __init__(
            self, number_of_processes=multiprocessing.cpu_count() * 2,
    ):
        # type: (int) -> None
        self.__splitter = _data_split.SetupData(number_of_processes)
        self.__kernel_setup = _kernel_setup.SetupKernels()
        self.__processes = None  # type: List[multiprocessing.Process]
        self.__connections = None  # type: List[multiprocessing.Pipe]
        self.__interface = None  # type: _ProcessInterface

    def main_options(
            self,
            data,  # type: Dict[str, Any]
            kernel,  # type: internals.Kernel
            internal_interface  # type: internals.KernelInterface
    ):
        # type: (...) -> None
        kernels = self.__setup_kernels(data, kernel)
        self.__make_processes(kernels, internal_interface.IS_DUPLEX)
        self.__start_processes()
        self.__build_interface(internal_interface)

    def __setup_kernels(self, data, kernel):
        # type: (Dict[str, Any], internals.Kernel) -> List[internals.Kernel]
        process_data = self.__splitter.split(data)
        kernels = self.__kernel_setup.setup_kernels(kernel, process_data)
        return kernels

    def __make_processes(self, kernels, duplex):
        # type: (List[internals.Kernel], bool) -> None
        if duplex:
            self.__LOGGER.debug("Building Duplex Processes.")
            processes, connections = _process_factory.duplex_build(kernels)
        else:
            self.__LOGGER.debug("Building Simplex Processes.")
            processes, connections = _process_factory.simplex_build(kernels)
        self.__processes, self.__connections = (processes, connections)

    def __start_processes(self):
        self.__LOGGER.debug("Starting Processes!")
        for process in self.__processes:
            process.start()

    def __build_interface(self, internal_interface):
        self.__interface = _ProcessInterface(
            internal_interface, self.__connections, self.__processes
        )

    def fetch_interface(self):
        # type: () -> _ProcessInterface
        return self.__interface
