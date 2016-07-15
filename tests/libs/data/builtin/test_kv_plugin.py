#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Simple Tests for EVIL Data type

The EVIL data type is a legacy data type originally written for PyPWA
Version 1, though now considered obsolete we still support it for
backwards compatibility.

See Also:
    PyPWA.libs.data.builtin.kv
"""

import collections
import logging
import os

import numpy
import pytest

import PyPWA.libs.data.builtin.kv as kv

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"


# Define global variables for the entire test file. These files contain
# the information needed to test the data loader and writer.

KV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/kv_test_data.txt"
)

KV_FLOAT_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/kv_floats_test_data.txt"
)

KV_BOOL_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/kv_bool_test_data.txt"
)

KV_WRITE_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/kv_write_test.txt"
)

SV_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "test_docs/sv_test_data.csv"
)

TEMP_WRITE_LOCATION = os.path.join(
    os.path.dirname(__file__), "test_docs/temporary_write_data"
)


def test_KvInterface_CallAbstractMethods_RaiseNotImplementedError():
    """
    Simple function to ensure that the abstract methods are calling back
    what we are expecting.
    """
    abstract_object = kv.KvInterface()

    with pytest.raises(NotImplementedError):
        abstract_object.parse(KV_TEST_DATA)

    with pytest.raises(NotImplementedError):
        abstract_object.write(KV_WRITE_DATA, 3)
        # The 3 doesn't matter here as an abstract method doesn't care
        # about its inputs.


def test_KvInterface_FileLengthMethod_ReturnLengthOfFile():
    """
    Checks that the file_length method returns the proper number of lines.
    """
    abstract_object = kv.KvInterface()
    assert abstract_object.file_length(KV_FLOAT_DATA) == 12


def EVILValidator_CheckType_ReturnType(data, expected_value):
    """
    Wrapper around Validator method to reduce code reuse.

    Args:
        data (str): The location of the file to parse
        expected_value (str):  The expected data type to be returned from
            the validator
    """
    evil_validator_test = kv.EVILValidator(data)
    value = evil_validator_test.evil_type
    assert value == expected_value


def test_EVILValidator_CheckEvilDictType_ReturnDictOfArrays():
    """
    Tests that Validator Reads KV_TEST_DATA as DictOfArrays
    """
    EVILValidator_CheckType_ReturnType(KV_TEST_DATA, "DictOfArrays")


def test_EVILValidator_CheckEvilBoolType_ReturnListOfBools():
    """
    Tests that Validator Reads KV_BOOL_DATA as ListOfBools
    """
    EVILValidator_CheckType_ReturnType(KV_BOOL_DATA, "ListOfBools")


def test_EVILValidator_CheckEvilFloatType_ReturnListOfFloats():
    """
    Tests that Validator Reads KV_FLOAT_DATA as ListOfFloats
    """
    EVILValidator_CheckType_ReturnType(KV_FLOAT_DATA, "ListOfFloats")


def test_EVILValidator_CheckFailedType_RaiseIncompatibleData():
    """
    Tests that Validator fails when reading SV_TEST_DATA
    """
    with pytest.raises(IOError):
        EVILValidator_CheckType_ReturnType(SV_TEST_DATA, "Something")


def EVILWriteMemory_CheckWriteRead_RandomGenEqualDisk(data):
    """
    Simple wrapper to ensure that tests are set up right using the
    SomewhatIntelligentSelector.

    Args:
        data: The test data.

    Returns:
        list[received data, read data]: A list of all the data written
            into the disk and read from the disk.
    """
    writer = kv.SomewhatIntelligentSelector()
    writer.write(TEMP_WRITE_LOCATION, data)
    new_data = writer.parse(TEMP_WRITE_LOCATION)
    os.remove(TEMP_WRITE_LOCATION)
    return [data, new_data]


def test_SomewhatIntelligentSelector_FloatValid_ReadWriteTrue():
    """
    Tests that floats are written and read correctly
    """
    # Setup data and loop it through the read/write function.
    data = numpy.random.rand(2000)
    loaded, written = EVILWriteMemory_CheckWriteRead_RandomGenEqualDisk(
        data
    )

    # Perform the tests
    numpy.testing.assert_array_almost_equal(loaded, written)
    numpy.testing.assert_almost_equal(written[0], data[0])
    assert isinstance(written[0], numpy.float64)


def test_SomewhatIntelligentSelector_BoolValid_ReadWriteTrue():
    """
    Tests that bools are written and read correctly.
    """
    # Setup Data
    data = numpy.zeros(2000, dtype=bool)
    for index in range(len(data)):
        data[index] = numpy.random.choice([0, 1])

    loaded, written = EVILWriteMemory_CheckWriteRead_RandomGenEqualDisk(
        data
    )

    # Run tests
    numpy.testing.assert_array_equal(loaded, written)


def test_SomewhatIntelligentSelector_DictValid_ReadWriteTrue():
    """
    Tests that tuples are written and read correctly.
    """
    # Setup tests
    x = numpy.zeros(1000, [("x", "f8"), ("y", "f8")])
    x["x"] = numpy.random.rand(1000)
    x["y"] = numpy.random.rand(1000)

    loaded, written = EVILWriteMemory_CheckWriteRead_RandomGenEqualDisk(
        x
    )

    # Run tests
    numpy.testing.assert_array_equal(loaded["x"], written["x"])


def test_SomewhatIntelligentSelector_StringInvalid_RaiseRuntimeError():
    """
    Tests to make sure that it crashes properly when something that isn't
    supported is sent to the plugin.
    """
    # Setup tests
    x = "A random string that EVIL shouldn't know how to handle"
    selector = kv.SomewhatIntelligentSelector()

    # Run test
    with pytest.raises(RuntimeError):
        selector.write(TEMP_WRITE_LOCATION, x)


def test_EVILIteration_ReadWriteEvents_EventsEqual():
    """
    Tests the EVIL Writer and EVIL Reader by generating data then writing
    that data to disk, reading it back in, then comparing.
    """
    particle = numpy.zeros(1, [("x", "f8"), ("y", "f8")])
    data = collections.deque()
    for number in range(10):
        particle["x"] = numpy.random.rand()
        particle["y"] = numpy.random.rand()
        data.append(particle)

    writer = kv.EVILWriter(TEMP_WRITE_LOCATION)
    for event in data:
        writer.write(event)

    writer.close()

    new_data = collections.deque()

    reader = kv.EVILReader(TEMP_WRITE_LOCATION)

    for x in reader:
        logging.debug(x)
        new_data.append(x)

    os.remove(TEMP_WRITE_LOCATION)
    numpy.testing.assert_almost_equal(new_data[0]["x"], data[0]["x"])