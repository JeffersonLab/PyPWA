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
Takes a Kernel, copies it multiple times, loads a packet of data into
each kernel, and then returns a list of those kernels
"""

import copy
from typing import Any, Dict, List

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.interfaces import kernel

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class SetupKernels(object):

    def __init__(self):
        self.__kernel = None  # type: kernel.Kernel
        self.__packed_kernels = None  # type: List[kernel.Kernel]

    def setup_kernels(self, process_kernel, packets):
        # type: (kernel.Kernel, List[Dict[str, Any]]) -> List[kernel.Kernel]
        self.__setup_kernel_details(process_kernel)
        self.__iterate_over_packets(packets)
        return self.__packed_kernels

    def __setup_kernel_details(self, process_kernel):
        # type: (kernel.Kernel) -> None
        self.__kernel = process_kernel
        self.__packed_kernels = []

    def __iterate_over_packets(self, packets):
        # type: (List[Dict[str, Any]]) -> None
        for packet in packets:
            self.__setup_kernel_with_packet(packet)

    def __setup_kernel_with_packet(self, packet):
        # type: (Dict[str, Any]) -> None
        kernel = self.__get_kernel_copy()
        self.__load_data_into_kernel(kernel, packet)
        self.__packed_kernels.append(kernel)

    def __get_kernel_copy(self):
        # type: () -> kernel.Kernel
        return copy.deepcopy(self.__kernel)

    def __load_data_into_kernel(self, process_kernel, packet):
        # type: (kernel.Kernel, Dict[str, Any]) -> None
        for key in packet.keys():
            setattr(process_kernel, key, packet[key])
