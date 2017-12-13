import numpy
import pytest

from PyPWA.libs.components.process import foreman, templates

TEST_DATA = {"data": numpy.random.rand(100)}


"""
Test Duplex
"""

class DuplexKernel(templates.Kernel):

    def __init__(self):
        self.data = None  # type: numpy.ndarray

    def setup(self):
        pass

    def process(self, data=False):
        # type: (str) -> numpy.ndarray
        return numpy.sum(self.data)


class DuplexInterface(templates.KernelInterface):
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
    process_builder = foreman.CalculationForeman(3)
    process_builder.main_options(TEST_DATA, DuplexKernel(), DuplexInterface())
    interface = process_builder.fetch_interface()
    yield interface
    interface.stop(request.param)


def test_duplex_calculated_matches_expected(duplex_interface):
    final_value = duplex_interface.run("go")
    numpy.testing.assert_approx_equal(
        final_value, numpy.sum(TEST_DATA['data'])
    )


def test_duplex_reports_is_alive(duplex_interface):
    assert duplex_interface.is_alive == True


"""
Test Simplex
"""

class SimplexKernel(templates.Kernel):

    def __init__(self):
        self.data = False  # type: numpy.ndarray

    def setup(self):
        pass

    def process(self, data=False):
        return numpy.sum(self.data)


class SimplexInterface(templates.KernelInterface):
    IS_DUPLEX = False

    def run(self, connections, args):
        value = numpy.zeros(len(connections))
        for index, connection in enumerate(connections):
            value[index] = connection.recv()

        return numpy.sum(value)


@pytest.fixture(params=[True, False])
def simplex_interface(request):
    process_builder = foreman.CalculationForeman(3)
    process_builder.main_options(
        TEST_DATA, SimplexKernel(), SimplexInterface()
    )
    interface = process_builder.fetch_interface()
    yield interface
    interface.stop(request.param)


def test_simplex_sum_matches_expected(simplex_interface):
    sum = simplex_interface.run()
    numpy.testing.assert_approx_equal(sum, numpy.sum(TEST_DATA['data']))

"""
Test Errors
"""

class KernelError(templates.Kernel):

    def __init__(self):
        self.data = False  # type: numpy.ndarray

    def setup(self):
        pass

    def process(self, data=False):
        raise RuntimeError


class InterfaceError(templates.KernelInterface):

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
    process_builder = foreman.CalculationForeman(3)
    process_builder.main_options(TEST_DATA, KernelError(), broken_interface)
    interface = process_builder.fetch_interface()
    yield interface
    interface.stop()


def test_error_was_handled(interface_with_errors):
    values = interface_with_errors.run()
    assert templates.ProcessCodes.ERROR in values
