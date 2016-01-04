import numpy
import os

import PyPWA.libs.proc.calculation_tools as calculation_tools

DATA = {
    'BinN': numpy.array([0.24418789, 0.10050128, 0.9089618, 0.40875684, 0.53606013, 0.52099577]),
    'QFactor': numpy.array([0.49851558, 0.73195453, 0.7000174, 0.0933503, 0.63582723, 0.26120629]),
    'data': {
        'x': numpy.array([0.16308575, 0.12278721, 0.47615786, 0.6785825, 0.81275147, 0.93995425])
    }
}

DICT_SPLIT = calculation_tools.DictionarySplitter()

CWD = os.path.join(os.path.dirname(__file__), "test_functions/")
FILE_NAME = "true_functions"


def test_no_split():
    split_data = DICT_SPLIT.split(DATA, 1)
    assert split_data == [DATA]


def test_split_lenght():
    split_data_2 = DICT_SPLIT.split(DATA, 2)
    split_data_6 = DICT_SPLIT.split(DATA, 6)

    assert len(split_data_2) == 2
    assert len(split_data_6) == 6


def test_split_by_two():
    split_data = DICT_SPLIT.split(DATA, 2)

    expected = [
        {
            'BinN': numpy.array([0.24418789, 0.10050128, 0.9089618]),
            'QFactor': numpy.array([0.49851558, 0.73195453, 0.7000174]),
            'data': {
                'x': numpy.array([0.16308575, 0.12278721, 0.47615786])
            }
        },
        {
            'BinN': numpy.array([0.40875684, 0.53606013, 0.52099577]),
            'QFactor': numpy.array([0.0933503, 0.63582723, 0.26120629]),
            'data': {
                'x': numpy.array([0.6785825, 0.81275147, 0.93995425])
            }
        }
    ]

    for index in range(2):
        numpy.testing.assert_array_almost_equal(split_data[index]["BinN"], expected[index]["BinN"])
        numpy.testing.assert_array_almost_equal(split_data[index]["QFactor"], expected[index]["QFactor"])
        numpy.testing.assert_array_almost_equal(split_data[index]["data"]["x"], expected[index]["data"]["x"])


def test_function_loading_full():
    function_loading = calculation_tools.FunctionLoading(CWD, FILE_NAME, "the_function", "the_setup")
    function = function_loading.return_amplitude
    setup = function_loading.return_setup

    assert function() == True
    assert setup() == True
