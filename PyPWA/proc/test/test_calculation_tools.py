import unittest
import numpy
import PyPWA.proc.calculation_tools

data = {
    'BinN': numpy.array([0.24418789,  0.10050128,  0.9089618,  0.40875684,  0.53606013, 0.52099577]),
    'QFactor': numpy.array([0.49851558,  0.73195453,  0.7000174,  0.0933503,  0.63582723, 0.26120629]),
    'data': {
        'x': numpy.array([0.16308575,  0.12278721,  0.47615786,  0.6785825,  0.81275147, 0.93995425])
    }
}


class TestNoSplit(unittest.TestCase):
    def test_no_split(self):
        global data
        splitter = PyPWA.proc.calculation_tools.DictionarySplitter()
        split_data = splitter.split(data, 1)

        self.assertEquals(split_data, [data])


class TestLength(unittest.TestCase):
    def test(self):
        global data
        splitter = PyPWA.proc.calculation_tools.DictionarySplitter()
        split_data_2 = splitter.split(data, 2)
        split_data_6 = splitter.split(data, 6)

        self.assertEquals(len(split_data_2), 2)
        self.assertEquals(len(split_data_6), 6)


class TestSplitByTwo(unittest.TestCase):
    def test(self):
        global data
        splitter = PyPWA.proc.calculation_tools.DictionarySplitter()
        split_data = splitter.split(data, 2)

        expected = [
            {
                'BinN': numpy.array([0.24418789,  0.10050128,  0.9089618]),
                'QFactor': numpy.array([0.49851558,  0.73195453,  0.7000174]),
                'data': {
                    'x': numpy.array([0.16308575,  0.12278721,  0.47615786])
                }
            },
            {
                'BinN': numpy.array([0.40875684,  0.53606013,  0.52099577]),
                'QFactor': numpy.array([0.0933503,  0.63582723,  0.26120629]),
                'data': {
                    'x': numpy.array([0.6785825,  0.81275147,  0.93995425])
                }
            }
        ]

        for index in range(2):
            numpy.testing.assert_array_almost_equal(split_data[index]["BinN"], expected[index]["BinN"])
            numpy.testing.assert_array_almost_equal(split_data[index]["QFactor"], expected[index]["QFactor"])
            numpy.testing.assert_array_almost_equal(split_data[index]["data"]["x"], expected[index]["data"]["x"])


if __name__ == '__main__':
    unittest.main()
