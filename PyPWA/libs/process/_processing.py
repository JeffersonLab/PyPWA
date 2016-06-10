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

import multiprocessing

from PyPWA.libs.process import _communication
from PyPWA.libs.process import _utilities
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _DuplexProcess(multiprocessing.Process):
    daemon = True  # This is set to true so that if the main process dies the
    # child processes will die as well.

    def __init__(self, kernel, communicator):
        """
        Main object for duplex processes. These processes are worker processes
        and as such will continue to run indefinitely until they are shut down
        by the main process or until the main process dies.

        Args:
            kernel (_utilities.AbstractKernel): The kernel that will hold all the
                information and logic needed for the process to process the data
                that it receives from the main process.
            communicator (_communication._DuplexCommunication): This is the way
                that the process will communicate with the children and vice
                versa.
        """
        super(_DuplexProcess, self).__init__()
        self._kernel = kernel
        self._communicator = communicator

    def run(self):
        """
        This method defines the main loop for the duplex function, this defines
        how the process works.

        Returns:
            0: When the process is closed cleanly.
        """
        self._kernel.setup()
        while True:
            value = self._communicator.receive()
            if value == "DIE":
                break
            elif value == "IGNORE":
                pass
            else:
                self._communicator.send(self._kernel.process(value))
        return 0


class _SimplexProcess(multiprocessing.Process):
    daemon = True  # Set to true so that if the main process dies, the children
    # will die as well.

    def __init__(self, single_kernel, communicator):
        """
        The simplex process is the simple offload process, anything passed to
        here will be ran immediately then send to the result back to the main
        process and die.

        Args:
            single_kernel (_utilities.AbstractKernel): The kernel that will
                contain all the data and logic needed for the process to
                function.
            communicator (_communication._SimplexSend): The only way to send
                data back to the main process after its been processed.
        """
        super(_SimplexProcess, self).__init__()
        self._kernel = single_kernel
        self._communicator = communicator

    def run(self):
        """
        The main loop for the process. This method is simple as it only calls
        the setup function from the run kernel, processes the data, then sends
        that returned data back to the main process.

        Returns:
            0: On success.
        """
        self._kernel.setup()
        self._communicator.send(self._kernel.process())
        return 0


class SimplexCalculationFactory(object):
    def __init__(self, kernel):
        """
        This object builds the required number of offload processes based on the
        supplied number of kernels.

        Args:
            kernel (list[_utilities.AbstractKernel]): A list of all the kernels
                that need to be nested into the individual processes. It will be
                one process per kernel.
        """
        self._kernel = kernel
        self._count = len(kernel)
        self._processes = []
        self._receives = []

    def build(self):
        """
        Call this method to actually build the offload processes.

        Returns:
            list[list[_SimplexProcess],list[_communication._SimplexReceives]]

        See Also:
            PyPWA.libs.process._communication._SimplexReceives for more
                information about the inter-process communication.
        """
        sends, self._receives = _communication.SimplexFactory(self._count)

        for kernel, send in zip(self._kernel, sends):
            self._processes.append(_SimplexProcess(kernel, send))

        return self.processed

    @property
    def processed(self):
        """
        Holds the generated communication and processes.

        Returns:
            list[list[_SimplexProcess], list[_communication._SimplexReceives]]

        See Also:
            PyPWA.libs.process._communication._SimplexReceives for more
                information about the inter-process communication.
        """
        return [self._processes, self._receives]


class DuplexCalculationFactory(object):
    def __init__(self, kernel):
        """
        This object generates the needed number of worker processes.
        Args:
            kernel (list[_utilities.AbstractKernel]): These are the objects that
                hold all the functioning logic for the processes. This should
                hold all of the needed data and logic needed for the processes
                to function.
        """
        self._kernel = kernel
        self._count = len(kernel)
        self._processes = []
        self._main_com = []

    def build(self):
        """
        Call this method to actually build the required number of worker
        processes.

        Returns:
            list[list[_DuplexProcess],list[_communication._DuplexCommunication]]

        See Also:
            PyPWA.libs.process._communication._DuplexCommunication for more
                information about inter-process communication.
        """
        self._main_com, process_com = _communication.DuplexFactory(self._count)

        for kernel, process_com in zip(self._kernel, process_com):
            self._processes.append(_DuplexProcess(kernel, process_com))

        return self.processed

    @property
    def processed(self):
        """
        Holds the generated communication and processes.

        Returns:
            list[list[_SimplexProcess],list[_communication._DuplexCommunication]]

        See Also:
            PyPWA.libs.process._communication._DuplexCommunication for more
                information about inter-process communication.
        """
        return [self._processes, self._main_com]
