import unittest
import numpy
from PyPWA.proc import process_calculation, process_communication
import data

class TestRejectionAcceptanceMethod(unittest.TestCase):
    def test(self):

        expected = numpy.array([0.87104099, 0.65580649, 2.54315913, 3.62430913, 4.3409056, 5.02029565])

        send_to, receive_from = process_communication.ProcessPipes.return_pipes(1)

        process = process_calculation.RejectionAcceptanceAmplitude(data.the_function, data.the_setup, data.data["data"],
                                                                   {"A1": 5.341}, send_to[0], 0)

        process.start()
        received = receive_from[0].recv()

        numpy.testing.assert_array_almost_equal(received[1], expected)
        self.assertEqual(received[0], 0)


class TestExtendedLikelihoodAmplitude(unittest.TestCase):
    def test(self):
        processed = 1/200

        processed_data = data.the_function(data.data["data"], {"A1": 5.341})
        processed_accepted = data.the_function(data.accept["data"], {"A1": 5.341})

        expected = -(numpy.sum(data.data["QFactor"] * data.data["BinN"] * numpy.log(processed_data))) + \
                    (processed * numpy.sum(data.accept["BinN"] * processed_accepted))

        send_to, receive_from = process_communication.ProcessPipes.return_pipes(2)

        process = process_calculation.ExtendedLikelihoodAmplitude(data.the_function, data.the_setup, processed,
                                                                  data.data, data.accept, send_to[0], receive_from[1])
        process.start()

        send_to[1].send({"A1": 5.341})

        value = receive_from[0].recv()

        send_to[1].send("DIE")

        numpy.testing.assert_almost_equal(value, expected)


class TestUnextendedLikelihodAmplitude(unittest.TestCase):
    def test(self):
        processed_data = data.the_function(data.data["data"], {"A1": 5.341})
        expected = -(numpy.sum(data.data["QFactor"] * data.data["BinN"] * numpy.log(processed_data)))

        send_to, receive_from = process_communication.ProcessPipes.return_pipes(2)

        process = process_calculation.UnextendedLikelihoodAmplitude(data.the_function, data.the_setup, data.data, send_to[0], receive_from[1])
        process.start()

        send_to[1].send({"A1": 5.341})
        value = receive_from[0].recv()
        send_to[1].send("DIE")

        numpy.testing.assert_almost_equal(value, expected)


