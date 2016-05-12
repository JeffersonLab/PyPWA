# The MIT License (MIT)
#
# Copyright (c) 2014-2016 JLab.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Multiprocessing Calculation
"""

import logging

from PyPWA.libs.process import _processing
from PyPWA.libs.process import _communication
from PyPWA.libs.process import utilities
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
        This object provides all the functions necessary to determine the state
        of the processes and to pass information to the processes. This is the
        main object that the program and users will use to access the processes.

        Args:
            interface_kernel: Object with a run method to be used to handle
                returned data.
            process_com (list[_communication._CommunicationInterface]): Objects
                needed to exchange data with the processes.
            processes (list[multiprocessing.Process]): List of the processing
                processes.
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
        communication and the received arguments to the kernel, then saves the
        value that was returned so that it can be called at a later time if
        needed.

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
                self._logger.warn("KILLING PROCESSES, THIS IS !EXPERIMENTAL! "
                                  "AND WILL PROBABLY BREAK THINGS.")
                for process in self._processes:
                    process.terminate()
            else:
                self._logger.warn(
                    "The communication object is Simplex, can not shut down "
                    "processes. You must execute the processes and fetch the "
                    "value from the interface before simplex functions will "
                    "shutdown, or force the thread to die. [EXPERIMENTAL]"
                )

    @property
    def is_alive(self):
        """
        Method to check the status of the process.

        Returns:
            bool: True if the processes are still spawned, False if they have
                terminated.
        """
        return self._processes[0].is_alive()

    def __del__(self):
        if self.is_alive:
            self._logger.error("GC TRYING TO KILL PROCESS INTERFACE WHILE "
                               "PROCESSES ARE STILL ALIVE.")
            self.stop(True)


class CalculationForeman(object):
    def __init__(self, interface_kernel, process_kernel):
        """
        This is the main object for the Process Plugin. All this object needs
        is an appropriately set up interface kernel and process kernel in order
        to function.

        Args:
            interface_kernel (utilities.AbstractInterface): The object that will
                be used to process the data returned from the processes.
            process_kernel (list[utilities.AbstractKernel]): The objects that
                will be seeded into the processes to execute the data.
        """
        self._logger = logging.getLogger(__name__)
        self._num_processes = len(process_kernel)
        self._interface_kernel = interface_kernel
        self._process_kernel = process_kernel
        self._duplex = interface_kernel.is_duplex
        self._interface = False

    def _make_process(self):
        """
        Calls the factory objects to generate the processes

        Returns:
            list[list[_communication._CommunicationInterface],list[process_calculation.Process]]
        """
        if self._duplex:
            self._logger.debug("Building Duplex Processes.")
            return _processing.DuplexCalculationFactory(self._process_kernel,
                                                        self._num_processes)
        else:
            self._logger.debug("Building Simplex Processes.")
            return _processing.SimplexCalculationFactory(self._process_kernel,
                                                         self._num_processes)

    def build(self):
        """
        Simple method that sets up and builds all the processes needed.
        """
        process, com = self._make_process()
        self._interface = _ProcessInterface(self._interface_kernel, com, process,
                                            self._duplex)

    def fetch_interface(self):
        """
        Returns the built Process Interface

        Returns:
             False: Interface hasn't been built yet.
             _ProcessInterface: If the interface has been built.
        """
        if isinstance(self._interface, bool):
            self._logger.warn("Process Interface was called before it was "
                              "built!")
            return False
        else:
            return self._interface
