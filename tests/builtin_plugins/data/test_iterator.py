import collections
import os

import numpy
import pytest

from PyPWA.builtin_plugins.data import iterator

CSV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/sv_test_data.csv"
)

GAMP_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/gamp_test_data.gamp"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "builtin/test_docs/temporary_write_data"
)


def test_Iterator_ReadData_DataMatches():
    handler = iterator.Iterator()
    reader = handler.return_reader(CSV_TEST_DATA)
    first_line = reader.next()
    assert first_line["ctAD"] == -0.265433


@pytest.mark.xfail(reason="Tests for unsupported data type.")
def test_Iterator_LoopingData_DataMatches():
    handler = iterator.Iterator()

    particle = numpy.zeros(1, [("x", "f8"), ("y", "f8")])
    data = collections.deque()
    for number in range(10):
        particle["x"] = numpy.random.rand()
        particle["y"] = numpy.random.rand()
        data.append(particle)

    writer = handler.return_writer(TEMP_WRITE_LOCATION, 1)
    for event in data:
        writer.write(event)
    writer.close()

    reader = handler.return_reader(TEMP_WRITE_LOCATION)
    for event in data:
        new_event = reader.next_event
        numpy.testing.assert_array_equal(new_event, event)
    reader.close()
    os.remove(TEMP_WRITE_LOCATION)
