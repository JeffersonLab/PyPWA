import PyPWA.data.file_manager as file_manager
import os
import numpy

MANAGER = file_manager.MemoryInterface()

YML_TMP = os.path.join(os.path.dirname(__file__), "memory/test_docs/yml_tmp.yml")
KV_TMP = os.path.join(os.path.dirname(__file__), "memory/test_docs/kv_tmp.txt")


def test_kv_data():
    data = numpy.random.rand(50)
    MANAGER.write(KV_TMP, data)
    read = MANAGER.parse(KV_TMP)

    numpy.testing.assert_array_almost_equal(data, read)
    os.remove(KV_TMP)


def test_yml_data():
    data = {"Likelihood": {"General": "Something"} }
    MANAGER.write(YML_TMP, data)
    read = MANAGER.parse(YML_TMP)

    assert read["Likelihood"]["General"] == "Something", "Expected 'Something'," \
                                            " got {0} instead!".format(read["Likelihood"]["General"])
    os.remove(YML_TMP)

