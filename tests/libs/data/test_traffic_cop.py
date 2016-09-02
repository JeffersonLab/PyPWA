import os
import numpy

from PyPWA.libs.data import traffic_cop


CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/gamp_test_data.gamp"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/temporary_write_data"
)


def test_Memory_ReadData_DataMatches():
    parser = traffic_cop.Memory(cache=False)
    data = parser.parse(CSV_TEST_DATA)
    assert data["QFactor"][3] == 0.832133


def test_Memory_LoopingData_DataMatches():
    parser = traffic_cop.Memory(options={"cache": False})
    data = numpy.zeros(1000, [("data", "f8"), ("more_data", "f8")])
    data["more_data"] = numpy.random.rand(1000)
    data["data"] = numpy.random.rand(1000)

    parser.write(TEMP_WRITE_LOCATION, data)
    new_data = parser.parse(TEMP_WRITE_LOCATION)

    numpy.testing.assert_array_equal(new_data, data)
    os.remove(TEMP_WRITE_LOCATION)


def test_MemoryLoopingDataWithCache_DataMatches():
    parser = traffic_cop.Memory(options={
        "cache": True,
        "clear cache": True,
        "fail": True
    })

    data = numpy.zeros(1000, [("data", "f8"), ("more_data", "f8")])
    data["more_data"] = numpy.random.rand(1000)
    data["data"] = numpy.random.rand(1000)

    parser.write(TEMP_WRITE_LOCATION, data)
    new_data = parser.parse(TEMP_WRITE_LOCATION)

    numpy.testing.assert_array_equal(new_data, data)

    clearer = traffic_cop.Memory(False, True)
    clearer.parse(TEMP_WRITE_LOCATION)
    os.remove(TEMP_WRITE_LOCATION)
