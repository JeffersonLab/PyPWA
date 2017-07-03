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

from multiprocessing.connection import Connection
from typing import List, Tuple

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.process import _connection_factory
from PyPWA.builtin_plugins.process import _processes
from PyPWA.core.shared.interfaces import internals

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


abstract_return = Tuple(List[_processes._AbstractProcess], List[Connection])
simplex_return = Tuple(List[_processes.Simplex], List[Connection])
duplex_return = Tuple(List[_processes.Duplex], List[Connection])


class _ProcessFactory(object):

    def __init__(
            self,
            process,  # type: _processes._AbstractProcess()
            connections  # type: _connection_factory.factory_type
    ):
        # type: (...) -> None
        self.__process_template = process
        self.__connection_factory = connections
        self.__count = 0
        self.__kernels = None  # type: List[internals.Kernel]
        self.__sends = None  # type: List[Connection]
        self.__receives = None  # type: List[Connection]
        self.__processes = None  # type: List[_processes._AbstractProcess]

    def build(self, kernels):
        # type: (List[internals.Kernel]) -> abstract_return
        self.__set_basic_details(kernels)
        self.__get_connections()
        self.__prime_process_list()
        self.__setup_processes()
        return self.__processes, self.__receives

    def __set_basic_details(self, kernels):
        # type: (List[internals.Kernel]) -> None
        self.__count = len(kernels)
        self.__kernels = kernels

    def __get_connections(self):
        child, main = self.__connection_factory(self.__count)
        self.__sends = child
        self.__receives = main

    def __prime_process_list(self):
        self.__processes = [0] * self.__count

    def  __setup_processes(self):
        for index, kernel, send_pipe in self.__process_iterator():
            kernel.name = index
            self.__processes[index] = self.__process_template(
                kernel, send_pipe
            )

    def __process_iterator(self):
        # type: () -> zip
        return zip(range(self.__count), self.__kernels, self.__sends)


def simplex_build(process_kernels):
    # type: (List[internals.Kernel]) -> simplex_return
    factory = _ProcessFactory(
        _processes.Simplex, _connection_factory.simplex_build
    )
    return factory.build(process_kernels)


def duplex_build(process_kernels):
    # type: (List[internals.Kernel]) -> duplex_return
    factory = _ProcessFactory(
        _processes.Duplex, _connection_factory.duplex_build
    )
    return factory.build(process_kernels)
