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
Kernel Processing
-----------------
Kernel processing basically is the process of taking a kernel that contains
all the logic needed to process something, make multiple copies of that
kernel, load data into each copy, and then distribute those kernels across
some predefined amount of resources of some type.

- ProcessCodes - Codes that can be sent to or received from the resources.
- KernelProcessing - Main Plugin
- ProcessInterface - Main glue between the resources and the object trying
  to use them
- Kernel - The collection of logic to be distributed.
- KernelInterface - The collection of logic inside the ProcessInterface that
  processes the returned information from the kernels.
"""

from typing import Any, List, Optional as Opt

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Kernel(object):

    # process_id should be set by the Kernel Processing plugin.
    PROCESS_ID = None  # type: int

    def setup(self):
        # type: () -> None
        """
        Anything that should be setup in the thread or process should be
        put here, this will be called only once before any calculation begins.
        """
        raise NotImplementedError()

    def process(self, data=False):
        # type: (Opt[Any]) -> Any
        """
        The actual calculation or function of the program, can optionally
        support values from the main thread / process.

        :param data: Any data that you want to pass to the kernel.
        :return: The final value or object that should be sent back to the
        main thread.
        """
        raise NotImplementedError()


class Interface(object):

    # is_duplex controls whether the kernel will shutdown after its first
    # run or if the kernel will wait for more information. If this is false
    # the kernel will only be able to send data and will shutdown after
    # its first run; however, if this is true then the kernel will stay
    # running and waiting for a value from the interface indefinitely until
    # they are shutdown manually.
    IS_DUPLEX = False

    def run(self, communicator, args):
        # type: (List[Any], Any) -> Any
        """
        The method that will be called to begin the calculation. This is
        the interface between the kernels and the calling object.

        :param communicator: A list of objects that will be used to
        communicate with the kernels.
        :param args: Any values that are sent to the main interface.
        :return: Whatever value that is calculated locally from the kernels.
        """
        raise NotImplementedError("The run method must be extended!")
