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
The processes and their factories are defined here. The current supported
methods are Duplex for worker processes and Simplex for offload processes.
"""

import logging
import multiprocessing

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.process._communication import CommunicationFactory

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _DuplexProcess(multiprocessing.Process):
    daemon = True  # This is set to true so that if the main process
    # dies the child processes will die as well.
    __logging_level = None
    __logging_file = None
    __logger = None

    def __init__(self, index, kernel, communicator):
        """
        Main object for duplex processes. These processes are worker
        processes and as such will continue to run indefinitely until
        they are shut down by the main process or until the main process
        dies.

        Args:
            kernel (kernels.AbstractKernel): The kernel that will hold
                all the information and logic needed for the process to
                process the data that it receives from the main process.
            communicator (_communication._DuplexCommunication): This is
                the way that the process will communicate with the
                children and vice versa.
        """
        super(_DuplexProcess, self).__init__()
        self._kernel = kernel
        self._kernel.PROCESS_ID = index
        self._communicator = communicator

    def run(self):
        """
        This method defines the main loop for the duplex function, this
        defines how the process works.

        Returns:
            0: When the process is closed cleanly.
        """
        self.__set_logger()
        self.__logger.debug(
            "Starting logging in proc index %d" % self._kernel.PROCESS_ID
        )
        self._kernel.setup()
        while True:
            value = self._communicator.receive()
            if isinstance(value, str) and value == "DIE":
                self.__logger.debug(
                    "Shutting down %d" % self._kernel.PROCESS_ID
                )
                break
            else:
                self._communicator.send(self._kernel.process(value))
        return 0

    def __set_logger(self):
        self.__logger = logging.getLogger(__name__ + "._DuplexProcess")


class _SimplexProcess(multiprocessing.Process):
    daemon = True  # Set to true so that if the main process dies,
    # the children will die as well.
    __logging_level = None
    __logging_file = None
    __logger = None

    def __init__(self, index, single_kernel, communicator):
        """
        The simplex process is the simple offload process, anything
        passed to here will be ran immediately then send to the result
        back to the main process and die.

        Args:
            single_kernel (kernels.AbstractKernel): The kernel that
                will contain all the data and logic needed for the
                process to function.
            communicator (_communication._SimplexSend): The only way to
                send data back to the main process after its been
                processed.
        """
        super(_SimplexProcess, self).__init__()
        self._kernel = single_kernel
        self._kernel.PROCESS_ID = index
        self._communicator = communicator

    def run(self):
        """
        The main loop for the process. This method is simple as it only
        calls the setup function from the run kernel, processes the data,
        then sends that returned data back to the main process.

        Returns:
            0: On success.
        """
        self.__set_logger()
        self._kernel.setup()
        self.__logger.debug(
            "Starting logging in proc index %d" % self._kernel.PROCESS_ID
        )
        self._communicator.send(self._kernel.process())
        return 0

    def __set_logger(self):
        self.__logger = logging.getLogger(__name__ + "._SimplexProcess")


class CalculationFactory(object):

    @staticmethod
    def simplex_build(process_kernels):
        """
        Call this method to actually build the offload processes.

        Args:
            process_kernels (list[kernels.AbstractKernel]):
                The pre-loaded process objects.

        Returns:
            list[list[_SimplexProcess],list[_communication._SimplexReceives]]

        See Also:
            PyPWA.libs.process._communication._SimplexReceives for more
                information about the inter-process communication.
        """

        count = len(process_kernels)
        processes = []

        sends, receives = CommunicationFactory.simplex_build(count)

        for index, internals in enumerate(zip(process_kernels, sends)):
            processes.append(
                _SimplexProcess(index, internals[0], internals[1])
            )

        return [processes, receives]

    @staticmethod
    def duplex_build(process_kernels):
        """
        Call this method to actually build the required number of worker
        processes.

        Returns:
            list[list[_DuplexProcess],list[_communication._DuplexCommunication]]

        See Also:
            PyPWA.libs.process._communication._DuplexCommunication for
                more information about inter-process communication.
        """
        count = len(process_kernels)
        processes = []
        main_com, process_com = CommunicationFactory.duplex_build(count)

        for index, internals in enumerate(zip(process_kernels, process_com)):
            processes.append(
                _DuplexProcess(index, internals[0], internals[1])
            )

        return [processes, main_com]
