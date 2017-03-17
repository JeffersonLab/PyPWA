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
This is the main file for the process plugin. This plugin contains all
the logic needed to generate offload processes and worker processes, this
is all done by extending the kernels with your needed information then
passing those kernels back to the Foreman.
"""

import copy
import logging
import multiprocessing

import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.process import _processing
from PyPWA.core.shared.interfaces import internals
from PyPWA.core.shared.interfaces import plugins

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _ProcessInterface(internals.ProcessInterface):

    def __init__(self, interface_kernel, process_com, processes, duplex):
        self._logger = logging.getLogger(__name__)

        self._com = process_com
        self._interface_kernel = interface_kernel
        self._processes = processes
        self._held_value = False
        self._duplex = duplex

    def run(self, *args):
        self._held_value = self._interface_kernel.run(self._com, args)
        return self._held_value

    @property
    def previous_value(self):
        return self._held_value

    def stop(self, force=False):
        if self._duplex and not force:
            self._ask_processes_to_stop()
        else:
            if force:
                self._terminate_processes()
            else:
                self._logger.warn(
                    "The communication object is Simplex, can not shut "
                    "down processes. You must execute the processes and "
                    "fetch the value from the interface before simplex "
                    "functions will shutdown, or force the thread to die "
                    "[EXPERIMENTAL]"
                )

    def _ask_processes_to_stop(self):
        for pipe in self._com:
            self._logger.debug("Attempting to kill processes.")
            pipe.send("DIE")

    def _terminate_processes(self):
        self._logger.warn(
            "KILLING PROCESSES, THIS IS !EXPERIMENTAL! AND WILL "
            "PROBABLY BREAK THINGS."
        )

        for process in self._processes:
            process.terminate()

    @property
    def is_alive(self):
        return self._processes[0].is_alive()


class CalculationForeman(plugins.KernelProcessing):

    def __init__(
            self, number_of_processes=multiprocessing.cpu_count() * 2,):
        self._process_kernels = False
        self._duplex = False
        self._interface = False
        self._interface_template = False

        self._logger = logging.getLogger(__name__)

        self._number_of_processes = number_of_processes

    def main_options(self, data, process_template, interface_template):
        process_data = self.__split_data(
            data, self._number_of_processes
        )

        self._process_kernels = self.__create_objects(
            process_template, process_data
        )

        self._duplex = interface_template.IS_DUPLEX
        self._interface_template = interface_template

        self._interface = self._build()

    def _make_process(self):
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
        processes, com = self._make_process()
        for process in processes:
            process.start()

        self._logger.debug("I have {0} processes!".format(len(processes)))

        return _ProcessInterface(
            self._interface_template, com, processes, self._duplex
        )

    def fetch_interface(self):
        return self._interface

    @staticmethod
    def __create_objects(kernel_template, data_chunks):
        processes = []
        for chunk in data_chunks:
            temp_kernel = copy.deepcopy(kernel_template)
            for key in chunk.keys():
                setattr(temp_kernel, key, chunk[key])
            processes.append(temp_kernel)

        return processes

    @staticmethod
    def __split_data(events_dict, number_of_process):
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
