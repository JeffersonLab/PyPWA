import numpy
import os
import pytest

import PyPWA.libs.data.memory.kv

TEST_KV_DICT_FILE = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_data.txt")
TEST_KV_DICT_FILE_2 = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_data2.txt")

TEST_KV_FLOAT_FILE = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_float.txt")
TEST_KV_BOOL_FILE = os.path.join(os.path.dirname(__file__), "test_docs/kv_test_bool.txt")


def test_read_dict_of_arrays():
    kv_loader = PyPWA.libs.data.memory.kv.DictOfArrays()

    data = kv_loader.parse(TEST_KV_DICT_FILE)

    numpy.testing.assert_approx_equal(data["ctAD"][3], 0.915743, 5)
    numpy.testing.assert_approx_equal(data["QFactor"][9], 0.762221, 5)
    assert len(list(data)) == 6


def test_dict_of_arrays_write_and_read():
    dictionary = {"something": numpy.random.rand(10), "else": numpy.random.rand(10)}

    kv_loader = PyPWA.libs.data.memory.kv.DictOfArrays()

    kv_loader.write(TEST_KV_DICT_FILE_2, dictionary)

    loaded = kv_loader.parse(TEST_KV_DICT_FILE_2)

    numpy.testing.assert_array_almost_equal(dictionary["something"], loaded["something"])
    numpy.testing.assert_array_almost_equal(dictionary["else"], loaded["else"])
    os.remove(TEST_KV_DICT_FILE_2)


def test_list_of_floats():
    data = numpy.random.rand(50)
    kv_loader = PyPWA.libs.data.memory.kv.ListOfFloats()
    kv_loader.write(TEST_KV_FLOAT_FILE, data)
    loaded = kv_loader.parse(TEST_KV_FLOAT_FILE)

    os.remove(TEST_KV_FLOAT_FILE)

    numpy.testing.assert_array_almost_equal(data, loaded)


def test_list_of_booleans():
    data = numpy.random.choice([True, False], 50)
    kv_loader = PyPWA.libs.data.memory.kv.ListOfBooleans()
    kv_loader.write(TEST_KV_BOOL_FILE, data)
    loaded = kv_loader.parse(TEST_KV_BOOL_FILE)

    os.remove(TEST_KV_BOOL_FILE)

    numpy.testing.assert_array_almost_equal(loaded, data)


def test_abstract_methods():
    abstract = PyPWA.libs.data.memory.kv.KvInterface()
    with pytest.raises(NotImplementedError):
        abstract.parse(TEST_KV_DICT_FILE)
    with pytest.raises(NotImplementedError):
        abstract.write(TEST_KV_DICT_FILE_2, {"something": 1})
    with pytest.raises(NotImplementedError):
        PyPWA.libs.data.memory.kv.KvInterface.write(TEST_KV_DICT_FILE_2, {"something": 1})
