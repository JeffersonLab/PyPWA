import unittest
import numpy
from PyPWA.proc import process_calculation, process_communication


def the_function(the_array, the_params):
    the_size = len(the_array[list(the_array)[0]])
    values = numpy.zeros(shape=the_size)
    for event in range(the_size):
        values[event] = the_params["A1"] * the_array["x"][event]
    return values


def the_setup():
    pass

data = {
    'BinN': numpy.array([0.24418789, 0.10050128, 0.9089618, 0.40875684, 0.53606013, 0.52099577]),
    'QFactor': numpy.array([0.49851558, 0.73195453, 0.7000174, 0.0933503, 0.63582723, 0.26120629]),
    'data': {
        'x': numpy.array([0.16308575, 0.12278721, 0.47615786, 0.6785825, 0.81275147, 0.93995425])
    }
}

accept = {
    'BinN': numpy.array([0.3520956, 0.80065876, 0.39763468, 0.17696008, 0.17404278, 0.71206781]),
    'QFactor': numpy.array([0.81609241, 0.94909706, 0.90525941, 0.90906724, 0.28092015, 0.5138446]),
    'data': {
        'x': numpy.array([0.78418863, 0.67792675, 0.20024854, 0.17331546, 0.88287882, 0.42427133])
    }
}


class TestRejectionAcceptanceMethod(unittest.TestCase):
    def test(self):

        expected = numpy.array([0.87104099, 0.65580649, 2.54315913, 3.62430913, 4.3409056, 5.02029565])

        send_to, receive_from = process_communication.ProcessPipes.return_pipes(1)

        process = process_calculation.RejectionAcceptanceAmplitude(the_function, the_setup, data["data"],
                                                                   {"A1": 5.341}, send_to[0], 0)

        process.start()
        received = receive_from[0].recv()

        numpy.testing.assert_array_almost_equal(received[1], expected)
        self.assertEqual(received[0], 0)


class TestExtendedLikelihoodAmplitude(unittest.TestCase):
    def test(self):
        processed = 1/200

        processed_data = the_function(data["data"], {"A1": 5.341})
        processed_accepted = the_function(accept["data"], {"A1": 5.341})

        expected = -(numpy.sum(data["QFactor"] * data["BinN"] * numpy.log(processed_data))) + \
                    (processed * numpy.sum(accept["BinN"] * processed_accepted))

        send_to, receive_from = process_communication.ProcessPipes.return_pipes(2)

        process = process_calculation.ExtendedLikelihoodAmplitude(the_function, the_setup, processed, data, accept,
                                                                  send_to[0], receive_from[1])
        process.start()

        send_to[1].send({"A1": 5.341})

        value = receive_from[0].recv()

        send_to[1].send("DIE")

        numpy.testing.assert_almost_equal(value, expected)


class TestUnextendedLikelihodAmplitude(unittest.TestCase):
    def test(self):
        processed_data = the_function(data["data"], {"A1": 5.341})
        expected = -(numpy.sum(data["QFactor"] * data["BinN"] * numpy.log(processed_data)))

        send_to, receive_from = process_communication.ProcessPipes.return_pipes(2)

        process = process_calculation.UnextendedLikelihoodAmplitude(the_function, the_setup, data, send_to[0],
                                                                    receive_from[1])
        process.start()

        send_to[1].send({"A1": 5.341})
        value = receive_from[0].recv()
        send_to[1].send("DIE")

        numpy.testing.assert_almost_equal(value, expected)


