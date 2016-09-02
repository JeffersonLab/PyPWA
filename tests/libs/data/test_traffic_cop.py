import collections

import numpy
import os

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


def test_Iterator_ReadData_DataMatches():
    handler = traffic_cop.Iterator()
    empty_reader = handler.return_reader(CSV_TEST_DATA)
    reader = empty_reader(CSV_TEST_DATA)
    first_line = reader.next()
    assert first_line["ctAD"] == -0.265433


def test_Iterator_LoopingData_DataMatches():
    handler = traffic_cop.Iterator()

    particle = numpy.zeros(1, [("x", "f8"), ("y", "f8")])
    data = collections.deque()
    for number in range(10):
        particle["x"] = numpy.random.rand()
        particle["y"] = numpy.random.rand()
        data.append(particle)

    unloaded_writer = handler.return_writer(TEMP_WRITE_LOCATION, 1)
    writer = unloaded_writer(TEMP_WRITE_LOCATION)
    for event in data:
        writer.write(event)
    writer.close()

    unloaded_reader = handler.return_reader(TEMP_WRITE_LOCATION)
    reader = unloaded_reader(TEMP_WRITE_LOCATION)
    for event in data:
        new_event = reader.next_event
        numpy.testing.assert_array_equal(new_event, event)
    reader.close()
    os.remove(TEMP_WRITE_LOCATION)

