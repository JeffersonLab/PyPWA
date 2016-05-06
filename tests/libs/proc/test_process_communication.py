"""
Tests process communication to ensure that data is passed correctly
"""

import logging

import numpy

import PyPWA.libs.proc.process_communication

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "development"

"""Start the logger for the test sheet"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)


def test_duplex_factory():
    """
    Tests the duplex factory to ensure that data is sent through
    the pipes correctly. Will fail if the pipes timeout or if
    the pipes return the wrong data.
    """
    logger.debug("Loading the duplex factory.")
    the_big_factory = PyPWA.libs.proc.process_communication.DuplexFactory(300)
    logger.debug("Starting the build process.")
    pipes = the_big_factory.build()

    logger.debug("Making test data.")
    the_big_data = numpy.random.rand(300)

    logger.debug("Sending test data through the pipes.")
    for data, pipe in zip(the_big_data, pipes[0]):
        pipe.send(data)

    logger.debug("Testing the other side of the pipes.")
    for data, pipe in zip(the_big_data, pipes[1]):
        assert data == pipe.receive()

    logger.debug("Sending test data through the other side of the pipes.")
    for data, pipe in zip(the_big_data, pipes[1]):
        pipe.send(data)

    logger.debug("Testing the main side of the pipes.")
    for data, pipe in zip(the_big_data, pipes[0]):
        assert data == pipe.receive()



def test_single_factory():
    """
    Tests the singles factory to make sure that the data sent through
    the pipes is returned on the correct end.
    """
    logger.debug("Loading the singles factory.")
    the_single_factory = PyPWA.libs.proc.process_communication.SingleFactory(300)
    logger.debug("Starting the build process.")
    pipes = the_single_factory.build()

    logger.debug("Making test data.")
    the_singles_data = numpy.random.rand(300)

    logger.debug("Sending data through the singles.")
    for data, pipe in zip(the_singles_data, pipes[0]):
        pipe.send(data)

    logger.debug("Testing data on the pipes.")
    for data, pipe in zip(the_singles_data, pipes[1]):
        assert data == pipe.receive()
