import os
import unittest
import PyPWA.data.memory.kv
import numpy

TEST_KV_DICT_FILE = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_data.txt")
TEST_KV_DICT_FILE_2 = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_data2.txt")

TEST_KV_FLOAT_FILE = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_float.txt")
TEST_KV_BOOL_FILE = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_bool.txt")


class TestReadDictOfArrays(unittest.TestCase):
    def test(self):
        kv_loader = PyPWA.data.memory.kv.DictOfArrays()

        data = kv_loader.parse(TEST_KV_DICT_FILE)

        self.assertAlmostEqual(data["ctAD"][3], 0.915743, 5 )
        self.assertAlmostEqual(data["QFactor"][9], 0.762221, 5)
        self.assertEqual(len(list(data)), 6)


def test_dict_of_arrays_write_and_read():
    dictionary = {"something": numpy.random.rand(10), "else": numpy.random.rand(10)}

    kv_loader = PyPWA.data.memory.kv.DictOfArrays()

    kv_loader.write(TEST_KV_DICT_FILE_2, dictionary)

    loaded = kv_loader.parse(TEST_KV_DICT_FILE_2)

    numpy.testing.assert_array_almost_equal(dictionary["something"], loaded["something"])
    numpy.testing.assert_array_almost_equal(dictionary["else"], loaded["else"])
    os.remove(TEST_KV_DICT_FILE_2)


class TestListOfFloats(unittest.TestCase):
    def test(self):
        data = numpy.random.rand(50)
        kv_loader = PyPWA.data.memory.kv.ListOfFloats()
        kv_loader.write(TEST_KV_FLOAT_FILE, data)
        loaded = kv_loader.parse(TEST_KV_FLOAT_FILE)

        os.remove(TEST_KV_FLOAT_FILE)

        numpy.testing.assert_array_almost_equal(data, loaded)


class TestListOfBooleans(unittest.TestCase):
    def test(self):
        data = numpy.random.choice([True, False], 50)
        kv_loader = PyPWA.data.memory.kv.ListOfBooleans()
        kv_loader.write(TEST_KV_BOOL_FILE, data)
        loaded = kv_loader.parse(TEST_KV_BOOL_FILE)

        os.remove(TEST_KV_BOOL_FILE)

        numpy.testing.assert_array_almost_equal(loaded, data)
