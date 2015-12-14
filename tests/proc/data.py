import numpy


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