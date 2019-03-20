import numpy
import pytest

from PyPWA.libs.components import process

TEST_DATA = {"data": numpy.random.rand(100)}


"""
Test Duplex
"""


class DuplexKernel(process.Kernel):

    def __init__(self):
        self.data = None  # type: numpy.ndarray

    def setup(self):
        pass

    def process(self, data=False):
        # type: (str) -> numpy.ndarray
        return numpy.sum(self.data)


class DuplexInterface(process.Interface):

    IS_DUPLEX = True

    def run(self, connections, arguments):
        for connection in connections:
            connection.send(arguments[0])

        value = numpy.zeros(len(connections))
        for index, connection in enumerate(connections):
            value[index] = connection.recv()

        return numpy.sum(value)


@pytest.fixture(params=[True, False])
def duplex_interface(request):
    interface = process.make_processes(
        TEST_DATA, DuplexKernel(), DuplexInterface(), 3
    )
    yield interface
    interface.stop(request.param)


def test_duplex_calculated_matches_expected(duplex_interface):
    final_value = duplex_interface.run("go")
    numpy.testing.assert_approx_equal(
        final_value, numpy.sum(TEST_DATA['data'])
    )


def test_duplex_reports_is_alive(duplex_interface):
    assert duplex_interface.is_alive
