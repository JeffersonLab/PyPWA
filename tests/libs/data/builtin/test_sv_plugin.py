import collections
import os

import pytest
import numpy

from PyPWA.libs.data import definitions
from PyPWA.libs.data.builtin import sv

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/sv_test_data.csv"
)

TSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/sv_test_data.tsv"
)

KV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/kv_test_data.txt"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "test_docs/temporary_write_data"
)


def test_Validator_CheckCSVFile_TestPass():
    """
    Checks that it returns valid for CSV Data
    """
    validator = sv.SvValidator(CSV_TEST_DATA)
    validator.test()


def test_Validator_CheckTSVFile_TestPass():
    """
    Checks that it returns valid for TSV Data
    """
    validator = sv.SvValidator(TSV_TEST_DATA)
    validator.test()


def test_Validator_CheckKVFile_TestFail():
    """
    Checks that validator fails when data is not CSV or TSV
    """
    validator = sv.SvValidator(KV_TEST_DATA)

    with pytest.raises(definitions.IncompatibleData):
        validator.test()


def test_SvMemory_CheckStaticData_ValuesMatch():
    """
    Checks that parsed data equals real data.
    """
    parser = sv.SvMemory()
    data = parser.parse(CSV_TEST_DATA)

    assert data["ctAD"][0] == numpy.float64(-0.265433)
    assert data["QFactor"][3] == numpy.float64(0.832133)


def test_SvMemory_CheckLoopingData_ValuesMatchExact():
    """
    Creates random data, writes it out, then reads it back in.
    If it matches then the test will pass.
    """
    data = numpy.zeros(10000, [("x", "f8"), ("y", "f8")])
    data["x"] = numpy.random.rand(10000)
    data["y"] = numpy.random.rand(10000)

    memory_handle = sv.SvMemory()
    memory_handle.write(TEMP_WRITE_LOCATION, data)
    new_data = memory_handle.parse(TEMP_WRITE_LOCATION)

    os.remove(TEMP_WRITE_LOCATION)
    numpy.testing.assert_array_equal(new_data, data)


def test_SvMemory_CheckLoopingReaderAndWrite_ValuesMatchExact():
    """
    Creates random data, writes it out with the writer, then reads it
    back in with the reader and checks that it matches.
    """
    particle = numpy.zeros(1, [("x", "f8"), ("y", "f8")])
    data = collections.deque()
    for number in range(10):
        particle["x"] = numpy.random.rand()
        particle["y"] = numpy.random.rand()
        data.append(particle)

    writer = sv.SvWriter(TEMP_WRITE_LOCATION)
    for event in data:
        writer.write(event)

    writer.close()
    reader = sv.SvReader(TEMP_WRITE_LOCATION)
    for event in data:
        new_event = reader.next_event
        numpy.testing.assert_array_equal(new_event, event)

    assert new_event == reader.previous_event
    reader.reset()
    reader.close()

    os.remove(TEMP_WRITE_LOCATION)
