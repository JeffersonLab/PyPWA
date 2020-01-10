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

import numpy as npy
import pytest

from PyPWA.libs import process

TEST_DATA = {"data": npy.random.rand(100)}


"""
Test Simplex Processes
"""


class SimplexKernel(process.Kernel):

    def __init__(self):
        self.data: npy.ndarray = False

    def setup(self):
        pass

    def process(self, data=False):
        return npy.sum(self.data)


class SimplexInterface(process.Interface):

    def run(self, connections, args):
        value = npy.zeros(len(connections))
        for index, connection in enumerate(connections):
            value[index] = connection.recv()

        return npy.sum(value)


@pytest.fixture
def simplex_interface(request):
    interface = process.make_processes(
        TEST_DATA, SimplexKernel(), SimplexInterface(), 3, False
    )

    yield interface
    interface.close()


def test_simplex_sum_matches_expected(simplex_interface):
    calculated_sum = simplex_interface.run()
    npy.testing.assert_approx_equal(calculated_sum, npy.sum(TEST_DATA['data']))


"""
Test Duplex
"""


class DuplexKernel(process.Kernel):

    def __init__(self):
        self.data: npy.ndarray = None

    def setup(self):
        pass

    def process(self, data: str = False) -> npy.ndarray:
        return npy.sum(self.data)


class DuplexInterface(process.Interface):

    def run(self, connections, arguments):
        for connection in connections:
            connection.send(arguments[0])

        value = npy.zeros(len(connections))
        for index, connection in enumerate(connections):
            value[index] = connection.recv()

        return npy.sum(value)


@pytest.fixture
def duplex_interface(request):
    interface = process.make_processes(
        TEST_DATA, DuplexKernel(), DuplexInterface(), 3, True
    )
    yield interface
    interface.close()


def test_duplex_calculated_matches_expected(duplex_interface):
    final_value = duplex_interface.run("go")
    npy.testing.assert_approx_equal(
        final_value, npy.sum(TEST_DATA['data'])
    )


def test_duplex_reports_is_alive(duplex_interface):
    assert duplex_interface.is_alive


"""
Test Errors
"""


class KernelError(process.Kernel):

    def __init__(self):
        self.data: npy.ndarray = False

    def setup(self):
        pass

    def process(self, data=False):
        raise RuntimeError("Testing Errors are caught in processing")


class InterfaceError(process.Interface):

    def __init__(self, is_duplex: bool):
        self.__duplex = is_duplex

    def run(self, connections, args):
        if self.__duplex:
            for connection in connections:
                connection.send("go")

        returned = [0] * len(connections)
        for index, connection in enumerate(connections):
            returned[index] = connection.recv()

        return returned


@pytest.fixture(params=[True, False])
def get_duplex_state(request):
    interface = InterfaceError(request.param)
    return interface, request.param


def test_process_error_handling(get_duplex_state):
    interface = process.make_processes(
        TEST_DATA, KernelError(), get_duplex_state[0], 3, get_duplex_state[1]
    )
    values = interface.run()
    assert process.ProcessCodes.ERROR in values
    interface.close()
