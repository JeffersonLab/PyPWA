import PyPWA.data.data_tools as data_tools
import numpy
import os

DATA_TYPE_FILE = os.path.join(os.path.dirname(__file__), "memory/test_docs/kv_test_data.txt")


def test_data_type_search_extension():
    type_search = data_tools.DataTypeSearch()

    sv_result = type_search.search(DATA_TYPE_FILE.replace(".txt", ".csv"))
    txt_result = type_search.search(DATA_TYPE_FILE)
    yml_result = type_search.search(DATA_TYPE_FILE.replace(".txt", ".yml"))
    pwa_result = type_search.search(DATA_TYPE_FILE.replace(".txt", ".pwa"))

    assert sv_result == "sv", "Expected SV, received {0} instead!".format(sv_result)
    assert txt_result == "kv", "Expected KV, received {0} instead!".format(txt_result)
    assert yml_result == "yaml", "Expected Yaml, received {0} instead!".format(yml_result)
    assert pwa_result == "pwa", "Expected PWA, received {0} instead!".format(pwa_result)


def test_data_type_write():
    sv_result = data_tools.DataTypeWrite.search("something.csv")
    kv_result = data_tools.DataTypeWrite.search("something.txt")
    kv2_result = data_tools.DataTypeWrite.search("something")
    yml_result = data_tools.DataTypeWrite.search("something.yml")
    pwa_result = data_tools.DataTypeWrite.search("something.pWA")

    assert sv_result == "sv", "Expected SV, received {0} instead!".format(sv_result)
    assert kv_result == "kv", "Expected KV, received {0} instead!".format(kv_result)
    assert kv2_result == "kv", "Expected KV, received {0} instead!".format(kv2_result)
    assert yml_result == "yaml", "Expected Yaml, received {0} instead!".format(yml_result)
    assert pwa_result == "pwa", "Expected PWA, received {0} instead!".format(pwa_result)


def test_data_types_arrays():
    type_test = data_tools.DataTypes()

    random_floats = numpy.random.rand(50)
    random_bools = numpy.random.choice([True,False], 50)

    bools = type_test.type(random_bools)
    floats = type_test.type(random_floats)

    assert bools == "listofbools", "Expected 'listofbools' received {0} instead!".format(bools)
    assert floats == "listoffloats", "Expected 'listoffloats', recieved {0} instead!".format(floats)


def test_data_type_dicts():
    type_test = data_tools.DataTypes()

    dictarray = {"x":numpy.random.rand(50), "y":numpy.random.rand(50)}
    dictdict = {"BinN" : numpy.random.rand(50), "data" : dictarray }

    dictofdicts = type_test.type(dictdict)
    dictofarrays = type_test.type(dictarray)

    assert dictofdicts == "dictofdicts", "Expected 'dictofdicts', received {0} instead!".format(dictofdicts)
    assert dictofarrays == "dictofarrays", "Expected 'dictofarrays', received {0} instead!".format(dictofarrays)
