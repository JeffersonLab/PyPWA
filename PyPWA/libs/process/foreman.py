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
This is the main file for the process plugin. This plugin contains all
the logic needed to generate offload processes and worker processes, this
is all done by extending the kernels with your needed information then
passing those kernels back to the Foreman.
"""

import copy
import logging
import multiprocessing

import numpy

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs.templates import interface_templates
from PyPWA.core_libs.templates import plugin_templates
from PyPWA.libs.process import _communication
from PyPWA.libs.process import _processing

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _ProcessInterface(interface_templates.InterfaceTemplate):
    def __init__(self, interface_kernel, process_com, processes, duplex):
        """
        This object provides all the functions necessary to determine the
        state of the processes and to pass information to the processes.
        This is the main object that the program and users will use to
        access the processes.

        Args:
            interface_kernel: Object with a run method to be used to
                handle returned data.
            process_com (list[_communication._CommunicationInterface]):
                Objects needed to exchange data with the processes.
            processes (list[multiprocessing.Process]): List of the
                processing processes.
        """
        self._logger = logging.getLogger(__name__)
        self._com = process_com
        self._interface_kernel = interface_kernel
        self._processes = processes
        self._held_value = False
        self._duplex = duplex

    def run(self, *args):
        """
        This is the wrapping method for the process kernel, it passes the
        communication and the received arguments to the kernel, then saves
        the value that was returned so that it can be called at a later
        time if needed.

        Args:
            *args: The arguments received through the run interface.
        Returns:
            The returned value from the process kernel.
        """
        self._held_value = self._interface_kernel.run(self._com, args)
        return self._held_value

    @property
    def previous_value(self):
        """
        Returns the previous value calculated from the processes.

        Returns:
            Last value calculated from the processes.
        """
        return self._held_value

    def stop(self, force=False):
        """
        The method used to kill processes.

        Args:
            force (Optional[bool]): Set to true if you want to force the
                processes to stop.
        """
        if self._duplex and not force:
            for pipe in self._com:
                self._logger.debug("Killing duplex processes.")
                pipe.send("DIE")
        else:
            if force:
                self._logger.warn(
                    "KILLING PROCESSES, THIS IS !EXPERIMENTAL! AND WILL "
                    "PROBABLY BREAK THINGS."
                )

                for process in self._processes:
                    process.terminate()
            else:
                self._logger.warn(
                    "The communication object is Simplex, can not shut "
                    "down processes. You must execute the processes and "
                    "fetch the value from the interface before simplex "
                    "functions will shutdown, or force the thread to die "
                    "[EXPERIMENTAL]"
                )

    @property
    def is_alive(self):
        """
        Method to check the status of the process.

        Returns:
            bool: True if the processes are still spawned, False if they
                have terminated.
        """
        return self._processes[0].is_alive()


class CalculationForeman(plugin_templates.KernelProcessingTemplate):

    def __init__(
            self, number_of_processes=multiprocessing.cpu_count() * 2,
            **options
    ):
        """
        This is the main object for the Process Plugin. All this object
        needs is an appropriately set up interface kernel and process
        kernel in order to function.

        Args:
            number_of_processes (Optional[int]): Number of processes to
                use, defaults to twice the available cpus.
            options (Optional[dict]): The options dictionary rendered by
                the configurator. Optional.
        """
        self._process_kernels = False
        self._duplex = False
        self._interface = False
        self._interface_template = False

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        self._number_of_processes = number_of_processes

        if options:
            super(CalculationForeman, self).__init__(options)

    def main_options(self, data, process_template, interface_template):
        """
        The options that need to be passed to it from the main object. The
        data that is needed for processing to occur.

        Args:
            data (dict):  The dictionary containing the data that needs to
                be nested into the process.
            process_template (kernels.AbstractKernel): The kernel that
                has been extended with the needed information for the
                process.
            interface_template (kernels.AbstractInterface): The interface
                that has been extended to process the information to be
                passed and from the processes.
        """
        process_data = self.__split_data(
            data, self._number_of_processes
        )

        self._process_kernels = self.__create_objects(
            process_template, process_data
        )

        self._duplex = interface_template.is_duplex
        self._interface_template = interface_template

        self._interface = self._build()

    def _make_process(self):
        """
        Calls the factory objects to generate the processes

        Returns:
            list[list[_communication._CommunicationInterface],list[process_calculation.Process]]
        """
        if self._duplex:
            self._logger.debug("Building Duplex Processes.")
            return _processing.CalculationFactory.duplex_build(
                self._process_kernels
            )

        else:
            self._logger.debug("Building Simplex Processes.")
            return _processing.CalculationFactory.simplex_build(
                self._process_kernels
            )

    def _build(self):
        """
        Simple method that sets up and builds all the processes needed.
        """
        processes, com = self._make_process()
        for process in processes:
            process.start()

        self._logger.debug("I have {0} processes!".format(len(processes)))

        return _ProcessInterface(
            self._interface_template, com, processes, self._duplex
        )

    @property
    def fetch_interface(self):
        """
        Returns the built Process Interface

        Returns:
             _ProcessInterface: The interface to the processes.
        """
        return self._interface

    @staticmethod
    def __create_objects(kernel_template, data_chunks):
        """
        Creates the objects to be nested into the processes.

        Args:
            kernel_template: The template to use that has all the
                processing logic.
            data_chunks list[dict]: A list of the data chunks to be nested
                into the processes.

        Returns:
            list
        """
        processes = []
        for chunk in data_chunks:
            temp_kernel = copy.deepcopy(kernel_template)
            for key in chunk.keys():
                setattr(temp_kernel, key, chunk[key])
            processes.append(temp_kernel)

        return processes

    @staticmethod
    def __split_data(events_dict, number_of_process):
        """
        Takes a dictionary of numpy arrays and splits them into chunks.

        Args:
            events_dict (dict): The data that needs to be divided into
                chunks.
            number_of_process (int): The number of processes.

        Returns:
            list[dict]: The chunks of data.
        """
        event_keys = events_dict.keys()
        data_chunks = []

        for chunk in range(number_of_process):
            temp_dict = {}
            for key in event_keys:
                temp_dict[key] = 0
            data_chunks.append(temp_dict)

        for key in event_keys:
            for index, events in enumerate(
                    numpy.array_split(events_dict[key], number_of_process)
            ):
                data_chunks[index][key] = events

        return data_chunks
