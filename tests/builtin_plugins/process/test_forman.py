import logging
import time

import numpy
import pytest

from PyPWA.builtin_plugins.process import foreman, _communication
from PyPWA.core.shared.interfaces import internals


def test_DuplexProcess_SumOfIntegers_Return50():
    """
    Tests that an array with 50 ones sent to a duplex process when summed
    returns a value of 50.
    """
    # Generate test data
    test_data = {"the_data": numpy.ones(50)}

    # Create a test process kernel
    class TestKernel(internals.Kernel):

        __logger = logging.getLogger("TEST")
        the_data = False  # type: numpy.ndarray

        def setup(self):
            self.__logger.debug("Test setup called!")

        def process(self, data=False):
            if data[0] == "go":  # data is a tuple.
                if isinstance(self.the_data, numpy.ndarray):
                    return numpy.sum(self.the_data)
                else:
                    return "FAILED"
            else:
                return "NO GO"

    # Create a test interface
    class TestInterface(internals.KernelInterface):
        IS_DUPLEX = True

        def run(self, communicator, arguments):
            for the_communicator in communicator:
                the_communicator.send(arguments)

            value = numpy.zeros(len(communicator))
            for index, the_communicator in enumerate(communicator):
                value[index] = the_communicator.receive()

            return numpy.sum(value)

    # Initialize the Foreman
    process_builder = foreman.CalculationForeman(3)
    process_builder.main_options(test_data, TestKernel(), TestInterface())

    # Attach to interface
    interface = process_builder.fetch_interface()

    final_value = interface.run("go")
    if interface.is_alive:
        interface.stop()

        time.sleep(3)
        if interface.is_alive:
            interface.stop(True)

    assert final_value == 50


def test_SimplexProcess_SumIntegers_Return50():
    """
    Tests that an array filled with 50 ones when summed in the simplex
    processes will return a value of 50.
    """
    # Test data
    test_data = {"the_data": numpy.ones(50)}

    # Create Kernel
    class TestKernel(internals.Kernel):
        the_data = False  # type: numpy.ndarray

        def setup(self):
            pass

        def process(self, data=False):
            return numpy.sum(self.the_data)

    # Create Interface
    class TestInterface(internals.KernelInterface):
        IS_DUPLEX = False

        def run(self, communicator, args):
            value = numpy.zeros(len(communicator))
            for index, the_communicator in enumerate(communicator):
                value[index] = the_communicator.receive()

            return numpy.sum(value)

    # Setup Foreman
    process_builder = foreman.CalculationForeman(3)
    process_builder.main_options(test_data, TestKernel(), TestInterface())

    # Fetch interface
    interface = process_builder.fetch_interface()

    final_value = interface.run()
    interface.stop()

    assert final_value == 50
    assert interface.previous_value == 50


def test_Kernels_WillFail_RaiseNotImplemented():
    """
    Check that Kernels will raise NotImplementedError if they are not
    overridden.
    """
    kernel = internals.Kernel()
    interface = internals.KernelInterface()

    with pytest.raises(NotImplementedError):
        kernel.process()

    with pytest.raises(NotImplementedError):
        kernel.setup()

    with pytest.raises(NotImplementedError):
        # We don't need the values to be correct, this is only a test.
        interface.run("something", "else")


def test_Communication_UnimplementedMethods_RaiseNotImplemented():
    """
    Check that if the wrong Communication object is used it will raise an
    error.
    """
    # The values don't need to be pipes since they should actually
    # never be called. Also these object should never be access
    # directly by the user.
    receive = _communication._SimplexReceive("send")
    send = _communication._SimplexSend("receive")
    interface = _communication._CommunicationInterface()

    with pytest.raises(_communication.SimplexError):
        receive.send("something")

    with pytest.raises(_communication.SimplexError):
        send.receive()

    with pytest.raises(NotImplementedError):
        interface.send("something")

    with pytest.raises(NotImplementedError):
        interface.receive()
