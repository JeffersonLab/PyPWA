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

The EVIL data type is a legacy data type originally written for PyPWA Version 1,
though now considered obsolete we still support it for backwards compatibility.

See Also:
    PyPWA.libs.data.builtin.kv
"""

import os

import pytest

import PyPWA.libs.data.builtin.kv as kv

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"


# Define global variables for the entire test file. These files contain the
# information needed to test the data loader and writer.

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


def test_KvInterface_CallAbstractMethods_RaiseNotImplementedError():
    """
    Simple function to ensure that the abstract methods are calling back what
    we are expecting.
    """
    abstract_object = kv.KvInterface()

    with pytest.raises(NotImplementedError):
        abstract_object.parse(KV_TEST_DATA)

    with pytest.raises(NotImplementedError):
        abstract_object.write(KV_WRITE_DATA, 3)
        # The 3 doesn't matter here as an abstract method doesn't care about
        # its inputs.


def test_KvInterface_FileLengthMethod_ReturnLengthOfFile():
    """
    Checks that the file_length method returns the proper number of lines.
    """
    abstract_object = kv.KvInterface()
    assert abstract_object.file_length(KV_FLOAT_DATA) == 12


def EVILValidator_CheckType_RetrunType(data, expected_value):
    """
    Wrapper around Validator method to reduce code reuse.

    Args:
        data (str): The location of the file to parse
        expected_value (str):  The expected data type to be returned from the
            validator
    """
    evil_validator_test = kv.EVILValidator(data)
    value = evil_validator_test.evil_type
    assert value == expected_value


def test_EVILValidator_CheckEvilDictType_ReturnDictOfArrays():
    """
    Tests that Validator Reads KV_TEST_DATA as DictOfArrays
    """
    EVILValidator_CheckType_RetrunType(KV_TEST_DATA, "DictOfArrays")


def test_EVILValidator_CheckEvilBoolType_ReturnListOfBools():
    """
    Tests that Validator Reads KV_BOOL_DATA as ListOfBools
    """
    EVILValidator_CheckType_RetrunType(KV_BOOL_DATA, "ListOfBools")


def test_EVILValidator_CheckEvilFloatType_ReturnListOfFloats():
    """
    Tests that Validator Reads KV_FLOAT_DATA as ListOfFloats
    """
    EVILValidator_CheckType_RetrunType(KV_FLOAT_DATA, "ListOfFloats")


def test_EVILValidator_CheckFailedType_RaiseIncompatibleData():
    """
    Tests that Validator fails when reading SV_TEST_DATA
    """
    with pytest.raises(IOError):
        EVILValidator_CheckType_RetrunType(SV_TEST_DATA, "Something")

