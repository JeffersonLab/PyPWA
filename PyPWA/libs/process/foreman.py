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

import logging
import multiprocessing

import ruamel.yaml.comments
import numpy

from PyPWA.libs.process import _processing
from PyPWA.libs.process import _communication
from PyPWA.libs.process import kernels
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _ProcessInterface(object):
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
        if self._duplex:
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

    def __del__(self):
        if self.is_alive:
            self._logger.error(
                "GC TRYING TO KILL PROCESS INTERFACE WHILE PROCESSES ARE "
                "STILL ALIVE."
            )

            self.stop(True)


class CalculationForeman(object):
    def __init__(self):
        """
        This is the main object for the Process Plugin. All this object
        needs is an appropriately set up interface kernel and process
        kernel in order to function.
        """
        self._logger = logging.getLogger(__name__)
        self._num_processes = None  # type: int
        self._interface_kernel = None  # type:
        # _utilities.AbstractInterface

        self._process_kernel = None  # type:
        # list[_utilities.AbstractKernel]

        self._duplex = None  # type: bool
        self._interface = False  # type:

    def populate(self, interface_kernel, process_kernel):
        """

        Args:
            interface_kernel (kernels.AbstractInterface): The object
                that will be used to process the data returned from the
                processes.
            process_kernel (list[_utilities.AbstractKernel]): The objects
                that will be seeded into the processes to execute the
                data.
        """
        self._num_processes = len(process_kernel)
        self._interface_kernel = interface_kernel
        self._process_kernel = process_kernel
        self._duplex = interface_kernel.is_duplex
        self._build()

    def _make_process(self):
        """
        Calls the factory objects to generate the processes

        Returns:
            list[
                list[_communication._CommunicationInterface],
                list[process_calculation.Process]
                ]
        """
        if self._duplex:
            self._logger.debug("Building Duplex Processes.")
            return _processing.DuplexCalculationFactory(
                self._process_kernel
            )

        else:
            self._logger.debug("Building Simplex Processes.")
            return _processing.SimplexCalculationFactory(
                self._process_kernel
            )

    def _build(self):
        """
        Simple method that sets up and builds all the processes needed.
        """
        process, com = self._make_process()
        self._interface = _ProcessInterface(
            self._interface_kernel, com, process, self._duplex
        )

    def fetch_interface(self):
        """
        Returns the built Process Interface

        Returns:
             False: Interface hasn't been built yet.
             _ProcessInterface: If the interface has been built.
        """
        if isinstance(self._interface, bool):

            self._logger.warn(
                "Process Interface was called before it was built!"
            )

            return False
        else:
            return self._interface


class Options(object):
    _options = {

        # Optional
        "number of processes": multiprocessing.cpu_count() * 2
        #  We set this two 2 times the number of CPUs to account for
        #  hyper threading.
    }

    _template = {
        "number of processes": int
    }

    def __init__(self):
        """
        Simple Object to hold the options for the Foreman.
        """
        header = self._build_empty_options_with_comments()
        self._optional = self._build_optional(header)
        self._required = header

    @staticmethod
    def _build_empty_options_with_comments():
        header = ruamel.yaml.comments.CommentedMap()
        content = ruamel.yaml.comments.CommentedMap()

        header[kernels.MODULE_NAME] = content
        header.yaml_add_eol_comment(
            "This is the builtin processing plugin, you can replace this "
            "with your own, or use one of the other options that we have."
            , kernels.MODULE_NAME
        )

        content.yaml_add_eol_comment(
            "This is the max number of processes to have running at any "
            "time in the program, the hard max will always be 2 * the "
            "number of CPUs in your computer so that we don't resource "
            "lock your computer. Will work on any Intel  or AMD "
            "processor, PowerPCs might have difficulty here.",
            "number of processes"
        )

        return header

    def _build_optional(self, header):
        """
        Since there is only one option, and its optional, we only have a
        single building function for the actual options.

        Args:
            header (ruamel.yaml.comments.CommentedMap): The empty
                dictionary with the comments included.

        Returns:
            ruamel.yaml.comments.CommentedMap: The dictionary with the
                optional fields.
        """
        header[kernels.MODULE_NAME]["number of processes"] = \
            self._options["number of processes"]
        return header

    @property
    def return_template(self):
        return self._template

    @property
    def return_required(self):
        return self._required

    @property
    def return_optional(self):
        return self._optional

    @property
    def return_advanced(self):
        return self._optional

    @property
    def return_defaults(self):
        return self._options


class BuildKernels(object):

    def __init__(self, events_dict, kernel, interface, procs):
        chunk_events = self.__split_data(events_dict, procs)
        kernels = self.__create_objects(kernel, chunk_events)
        self._foreman = CalculationForeman()
        self._foreman.populate(interface, kernels)

    @staticmethod
    def __create_objects(kernel_template, data_chunk):
        kernels = []
        for chunk in data_chunk:
            temp_kernel = kernel_template()
            for key in chunk.keys():
                setattr(temp_kernel, key, chunk[key])
            kernels.append(temp_kernel)


    @staticmethod
    def __split_data(events_dict, proc):
        """

        Args:
            events_dict (dict):
            proc (int):

        Returns:

        """
        keys = events_dict.keys()
        new_list = []

        for chunk in range(proc):
            temp_dict = {}
            for key in keys:
                temp_dict[key] = 0
            new_list.append(temp_dict)

        for key in keys:
            for index, events in enumerate(
                    numpy.split(events_dict[key], proc)):
                new_list[index][key] = events

        return new_list
