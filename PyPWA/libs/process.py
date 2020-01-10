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
Creates kernel based processes.
===============================

A kernel based process is a process in which a kernel interface is
populated with some data and packaged into a Process. When that process
is spawned it will either await data being sent to it (Duplex) or
immediately start processing the data and send it (Simplex).
This was written to parallelize statistical analysis inside the package
for data with independent events.

File Layout
-----------
- Templates and Abstract Classes
- Predefined Types
- Process creation functions
- Process and Interface Objects


.. note::
    Duplex processes will not shutdown automatically, you must shut them
    down from the returned interface object. This is done so that when
    new parameters are passed to the Duplex Processes there will not
    be an associated "startup" cost.
"""

import copy
import time
from abc import ABC, abstractmethod
from enum import Enum
from multiprocessing import cpu_count, Pipe, Process
from multiprocessing.connection import Connection
from typing import Any, Dict, List, Tuple, Union

import numpy as npy
import pandas as pd

from PyPWA import info as _info
from PyPWA.libs import vectors

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


MAX_PROC = cpu_count()


"""
Templates and Abstract Classes
"""


class Kernel(ABC):

    PROCESS_ID: int = 0

    """Kernel that will be placed inside each spawned process

    The kernel has two essentially parts: The setup and process.
    - Setup is called once before any processing begins. This is to
      initialize any needed modules or move data.
    - Process is called each time new data is received. This is
      where you would place your intensity function, or something
      similar.

    .. warning::
        Do not change the value of process_id! It's value will be
        set by make_process so that your data will be able to
        stitched back into order.
    """

    @abstractmethod
    def setup(self):
        """
        Anything that should be setup in the process should be put here,
        this will be called only once before any calculation begins.
        """
        ...

    @abstractmethod
    def process(self, data: Any = False) -> Any:
        """
        The actual calculation or function of the program, can optionally
        support values from the main thread / process.

        :param data: Any data that you want to pass to the kernel.
        :return: The final value or object that should be sent back to the
        main thread.
        """
        ...


class Interface(ABC):

    def run(self, communicator: List[Any], args: Any) -> Any:
        """
        The method that will be called to begin the calculation. This is
        the interface between the kernels and the calling object.

        :param communicator: A list of objects that will be used to
                             communicate with the kernels.
        :param args: Any values that are sent to the main interface.
        :return: Whatever value that is calculated locally from the kernels.
        """
        ...


"""
Predefined Types
"""


_main = Tuple[List["_SmartProcess"], List[Connection]]
_pipe = Tuple[List[Connection], List[Connection]]
_supported_types = Union[npy.ndarray, vectors.ParticlePool, pd.DataFrame]
_data = Dict[str, _supported_types]
_data_packet = List[_data]


"""
Process creation functions
"""


def make_processes(
        data: _data, template_kernel: Kernel,
        interface: Interface, number_of_processes: int = MAX_PROC,
        use_duplex: bool = True
) -> "ProcessInterface":

    packets = _make_data_packets(data, number_of_processes)
    kernels = _create_kernels_containing_data(template_kernel, packets)
    processes, communication = _create_processes(kernels, use_duplex)

    for process in processes:
        process.start()

    return ProcessInterface(interface, communication, processes)


def _make_data_packets(data: _data, number_of_processes: int) -> _data_packet:
    list_of_dicts = [dict() for i in range(number_of_processes)]

    for key in data.keys():
        if isinstance(data[key], (npy.ndarray, pd.Series, pd.DataFrame)):
            split = npy.array_split(data[key], number_of_processes)
        elif isinstance(data[key], vectors.ParticlePool):
            split = data[key].split(number_of_processes)
        else:
            raise ValueError(f"Unknown data {data[key]!r}")

        for index, data_packet in enumerate(split):
            list_of_dicts[index][key] = data_packet
            
    return list_of_dicts


def _create_kernels_containing_data(
        process_kernel: Kernel, data_packets: _data_packet) -> List[Kernel]:
    kernels_with_data = []
    for data in data_packets:
        new_kernel = copy.deepcopy(process_kernel)

        for key in data.keys():
            setattr(new_kernel, key, data[key])

        kernels_with_data.append(new_kernel)
    return kernels_with_data


def _create_processes(kernels: List[Kernel], is_duplex: bool) -> _main:
    receives, sends = _get_pipes_for_communication(len(kernels), is_duplex)

    processes = []
    for index, (kernel, send_pipe) in enumerate(zip(kernels, sends)):
        kernel.PROCESS_ID = index
        processes.append(_SmartProcess(kernel, send_pipe))
    return processes, receives


def _get_pipes_for_communication(num_of_pipes: int, is_duplex: bool) ->_pipe:
    main = []
    child = []
    for pipe_index in range(num_of_pipes):
        # Simplex pipes are: receiver, sender = multiprocess.Pipe(False)
        left, right = Pipe(is_duplex)
        main.append(left)
        child.append(right)
    return main, child


"""
Process and Interface Objects
"""


class ProcessCodes(Enum):

    SHUTDOWN = 1
    ERROR = 2


class ProcessInterface:

    def __init__(
            self, interface_kernel: Interface,
            process_com: List[Connection], processes: List["_SmartProcess"]):
        self.__connections = process_com
        self.__interface = interface_kernel
        self.__processes = processes

    def run(self, *args):
        try:
            return self.__interface.run(self.__connections, args)
        except Exception as error:
            self.close()
            raise error

    def close(self):
        for connection in self.__connections:
            if connection.writable:
                connection.send(ProcessCodes.SHUTDOWN)
            connection.close()

        time.sleep(2)

        for process in self.__processes:
            if process.is_alive():
                process.terminate()

    @property
    def is_alive(self) -> bool:
        return any([proc.is_alive() for proc in self.__processes])


class _SmartProcess(Process):

    def __init__(self, kernel: Kernel, connect: Connection):
        super(_SmartProcess, self).__init__()
        self.__kernel = kernel
        self.__connection = connect
        self.daemon = True

    def run(self):
        if self.__connection.readable:
            self.__run_duplex()
        else:
            self.__run_simplex()

    def __run_duplex(self):
        try:
            self.__kernel.setup()
        except Exception as error:
            self.__handle_error(error)
            raise
        else:
            self.__loop()

    def __loop(self):
        while True:
            received = self.__connection.recv()
            if received == ProcessCodes.SHUTDOWN:
                self.__connection.close()
                break
            self.__process(received)

    def __process(self, received_data):
        try:
            value = self.__kernel.process(received_data)
        except Exception as error:
            self.__handle_error(error)
            raise
        else:
            self.__connection.send(value)

    def __run_simplex(self):
        try:
            self.__kernel.setup()
            self.__connection.send(self.__kernel.process())
        except Exception as error:
            self.__handle_error(error)
            raise

    def __handle_error(self, error):
        self.__connection.send(ProcessCodes.ERROR)
        self.__connection.send(error)
        self.__connection.close()
