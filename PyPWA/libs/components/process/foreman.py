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
from typing import Any, Dict, List, Optional

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers import configuration_db
from PyPWA.libs.components.process import (
    _data_split, _kernel_setup,
    _process_factory, templates
)

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ProcessInterface(object):

    __LOGGER = logging.getLogger(__name__ + "._ProcessInterface")

    def __init__(
            self,
            interface_kernel,  # type: templates.KernelInterface
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
            connection.send(templates.ProcessCodes.SHUTDOWN)

    def __terminate_processes(self):
        self.__LOGGER.debug("Terminating Processes is Risky!")
        for process in self.__processes:
            process.terminate()

    @property
    def is_alive(self):
        return self.__processes[0].is_alive()


class CalculationForeman(object):

    __LOGGER = logging.getLogger(__name__ + ".CalculationForeman")

    def __init__(self, number_of_processes=None):
        # type: (Optional[int]) -> None
        process_count = self.__get_process_count(number_of_processes)
        self.__splitter = _data_split.SetupData(process_count)
        self.__kernel_setup = _kernel_setup.SetupKernels()
        self.__processes = None  # type: List[multiprocessing.Process]
        self.__connections = None  # type: List[multiprocessing.Pipe]
        self.__interface = None  # type: _ProcessInterface

    @staticmethod
    def __get_process_count(potential_processes):
        # type: () -> int
        if potential_processes:
            return potential_processes
        else:
            return configuration_db.Connector().read(
                "Builtin Multiprocessing", "number of processes"
            )

    def main_options(
            self,
            data,  # type: Dict[str, Any]
            process_kernel,  # type: templates.Kernel
            internal_interface  # type: templates.KernelInterface
    ):
        # type: (...) -> None
        kernels = self.__setup_kernels(data, process_kernel)
        self.__make_processes(kernels, internal_interface.IS_DUPLEX)
        self.__start_processes()
        self.__build_interface(internal_interface)

    def __setup_kernels(self, data, process_kernel):
        # type: (Dict[str, Any], templates.Kernel) -> List[templates.Kernel]
        process_data = self.__splitter.split(data)
        kernels = self.__kernel_setup.setup_kernels(
            process_kernel, process_data
        )
        return kernels

    def __make_processes(self, kernels, duplex):
        # type: (List[templates.Kernel], bool) -> None
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
