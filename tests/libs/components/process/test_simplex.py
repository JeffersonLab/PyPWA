import numpy
import pytest

from PyPWA.libs.components import process

TEST_DATA = {"data": numpy.random.rand(100)}


"""
Test Simplex Processes
"""


class SimplexKernel(process.Kernel):

    def __init__(self):
        self.data = False  # type: numpy.ndarray

    def setup(self):
        pass

    def process(self, data=False):
        return numpy.sum(self.data)


class SimplexInterface(process.Interface):
    IS_DUPLEX = False

    def run(self, connections, args):
        value = numpy.zeros(len(connections))
        for index, connection in enumerate(connections):
            value[index] = connection.recv()

        return numpy.sum(value)


@pytest.fixture(params=[True, False])
def simplex_interface(request):
    interface = process.make_processes(
        TEST_DATA, SimplexKernel(), SimplexInterface(), 3
    )

    yield interface
    interface.stop(request.param)


def test_simplex_sum_matches_expected(simplex_interface):
    sum = simplex_interface.run()
    numpy.testing.assert_approx_equal(sum, numpy.sum(TEST_DATA['data']))
