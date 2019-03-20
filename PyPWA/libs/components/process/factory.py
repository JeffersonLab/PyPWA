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
import copy
import multiprocessing
import numpy
from typing import Dict, List, Tuple, Union

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.components.process import _processes
from PyPWA.libs.components.process import templates as t
from PyPWA.libs.math import vectors

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


_main = Tuple[List[_processes._AbstractProcess], List[multiprocessing.Pipe]]
_pipe = Tuple[List[multiprocessing.Pipe], List[multiprocessing.Pipe]]
_supported_types = Union[numpy.ndarray, vectors.ParticlePool]
_data = Dict[str, _supported_types]
_data_packet = List[_data]


def make_processes(data, template_kernel, interface, number_of_processes):
    # type: (_data, t.Kernel, t.Interface, int) -> _processes.ProcessInterface
    packets = _ProcessData.make_data_packets(data, number_of_processes)
    kernels = _create_kernels_containing_data(template_kernel, packets)
    processes, communication = _create_processes(kernels, interface.IS_DUPLEX)

    for process in processes:
        process.start()

    return _processes.ProcessInterface(interface, communication, processes)


class _ProcessData(object):

    @classmethod
    def make_data_packets(cls, data, number_of_processes):
        # type: (_data, int) -> _data_packet
        list_of_dicts = [dict() for i in range(number_of_processes)]

        for key in data.keys():
            split_data = cls.__split_data(data[key], number_of_processes)

            for index, data_packet in enumerate(split_data):
                list_of_dicts[index][key] = data_packet
        return list_of_dicts

    @staticmethod
    def __split_data(data, number_of_processes):
        # type: (_supported_types, int) -> List[_supported_types]
        if isinstance(data, numpy.ndarray):
            return numpy.array_split(data, number_of_processes)

        elif isinstance(data, vectors.ParticlePool):
            return data.split(number_of_processes)

        else:
            raise ValueError("Unknown data {0!r}".format(data))


def _create_kernels_containing_data(process_kernel, data_packets):
    # type: (t.Kernel, _data_packet) -> List[t.Kernel]
    kernels_with_data = []
    for data in data_packets:
        new_kernel = copy.deepcopy(process_kernel)

        for key in data.keys():
            setattr(new_kernel, key, data[key])

        kernels_with_data.append(new_kernel)
    return kernels_with_data


def _create_processes(kernels, is_duplex):
    # type: (List[t.Kernel], bool) -> _main
    receives, sends = _get_pipes_for_communication(len(kernels), is_duplex)
    processor_class = _processes.Duplex if is_duplex else _processes.Simplex

    processes = []
    for index, kernel, send_pipe in zip(range(len(kernels)), kernels, sends):
        kernel.PROCESS_ID = index
        processes.append(processor_class(kernel, send_pipe))
    return processes, receives


def _get_pipes_for_communication(num_of_pipes, is_duplex):
    # type: (int, bool) -> _pipe
    main, child = [0] * num_of_pipes, [0] * num_of_pipes
    for pipe_index in range(num_of_pipes):
        # Simplex pipes are: receiver, sender = multiprocess.Pipe(False)
        main[pipe_index], child[pipe_index] = multiprocessing.Pipe(is_duplex)
    return main, child
