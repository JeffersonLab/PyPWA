import numpy
import pytest

from PyPWA.libs.process import processes, communication


def process_function(the_array, the_params):
    the_size = len(the_array[list(the_array)[0]])
    values = numpy.zeros(shape=the_size)
    for event in range(the_size):
        values[event] = the_params["A1"] * the_array["x"][event]
    return values


def setup():
    pass

DATA = {
    'BinN': numpy.array([0.24418789, 0.10050128, 0.0, 0.40875684, 0.53606013, 0.0]),
    'QFactor': numpy.array([0.49851558, 0.73195453, 0.7000174, 0.0933503, 0.63582723, 0.26120629]),
    'data': {
        'x': numpy.array([0.16308575, 0.12278721, 0.47615786, 0.6785825, 0.81275147, 0.93995425])
    }
}

ACCEPTED = {
    'BinN': numpy.array([0.0, 0.80065876, 0.39763468, 0.17696008, 0.0, 0.71206781]),
    'QFactor': numpy.array([0.81609241, 0.94909706, 0.90525941, 0.90906724, 0.28092015, 0.5138446]),
    'data': {
        'x': numpy.array([0.78418863, 0.67792675, 0.20024854, 0.17331546, 0.88287882, 0.42427133])
    }
}

SEND_TO, RECEIVE_FROM = communication.ProcessPipes.return_pipes(2)


def test_rejection_acceptance_method_value():
    expected = numpy.array([0.87104099, 0.65580649, 2.54315913, 3.62430913, 4.3409056, 5.02029565])
    process = processes.RejectionAcceptanceAmplitude(process_function, setup, DATA["data"],
                                                     {"A1": 5.341}, SEND_TO[0], 0)

    process.start()
    received = RECEIVE_FROM[0].recv()

    numpy.testing.assert_array_almost_equal(received[1], expected)
    assert received[0] == 0


def test_extended_binned_likelihood():
    processed = 1/200

    processed_data = process_function(DATA["data"], {"A1": 5.341})
    processed_accepted = process_function(ACCEPTED["data"], {"A1": 5.341})

    expected = -(numpy.sum(DATA["QFactor"] * DATA["BinN"] * numpy.log(processed_data))) + \
                (processed * numpy.sum(ACCEPTED["BinN"] * processed_accepted))

    process = processes.ExtendedLikelihoodAmplitude(process_function, setup, processed, DATA, ACCEPTED,
                                                    SEND_TO[0], RECEIVE_FROM[1])
    process.start()

    SEND_TO[1].send({"A1": 5.341})

    value = RECEIVE_FROM[0].recv()

    SEND_TO[1].send("DIE")  # I <3 telling processes to die

    numpy.testing.assert_almost_equal(value, expected)


def test_unextended_binned_value():
    processed_data = process_function(DATA["data"], {"A1": 5.341})
    expected = -(numpy.sum(DATA["QFactor"] * DATA["BinN"] * numpy.log(processed_data)))

    process = processes.UnextendedLikelihoodAmplitude(process_function, setup, DATA, SEND_TO[0],
                                                      RECEIVE_FROM[1])
    process.start()

    SEND_TO[1].send({"A1": 5.341})
    value = RECEIVE_FROM[0].recv()
    SEND_TO[1].send("DIE")

    numpy.testing.assert_almost_equal(value, expected)


def test_abstract_calls():
    abstract_one = processes.AbstractProcess()
    with pytest.raises(NotImplementedError):
        abstract_one.setup()
    with pytest.raises(NotImplementedError):
        abstract_one.processing()

    abstract_two = processes.AbstractLikelihoodAmplitude(setup, SEND_TO[0], RECEIVE_FROM[1])
    with pytest.raises(NotImplementedError):
        abstract_two.likelihood({"A1": 5.341})
