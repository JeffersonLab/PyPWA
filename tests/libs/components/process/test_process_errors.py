import numpy
import pytest

from PyPWA.libs.components import process

TEST_DATA = {"data": numpy.random.rand(100)}


"""
Test Errors
"""


class KernelError(process.Kernel):

    def __init__(self):
        self.data = False  # type: numpy.ndarray

    def setup(self):
        pass

    def process(self, data=False):
        raise RuntimeError("Testing Errors are caught in processing")


class InterfaceError(process.Interface):

    IS_DUPLEX = False

    def run(self, connections, args):
        if self.IS_DUPLEX:
            for connection in connections:
                connection.send("go")

        returned = [0] * len(connections)
        for index, connection in enumerate(connections):
            returned[index] = connection.recv()

        return returned


@pytest.fixture(params=[False, True])
def broken_interface(request):
    internal_interface = InterfaceError()
    internal_interface.IS_DUPLEX = request.param
    return internal_interface


@pytest.fixture()
def interface_with_errors(broken_interface):
    interface = process.make_processes(
        TEST_DATA, KernelError(), broken_interface, 3
    )
    yield interface
    interface.stop()


def test_error_was_handled(interface_with_errors):
    values = interface_with_errors.run()
    assert process.ProcessCodes.ERROR in values
