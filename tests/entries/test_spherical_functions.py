import pytest
import os
from PyPWA.entries import SphericalFunctions
ANGLE_TEST_DATA = os.path.join(os.path.dirname(__file__),
                               "../data/test_docs/angles.txt")


@pytest.fixture()
def file_parser():
    return SphericalFunctions._BreakupData(ANGLE_TEST_DATA)


def test_reading(file_parser):
    assert file_parser.theta() == ['.1', '.2', '.3', '.4']
    assert file_parser.phi() == ['.1', '.2', '.1', '.4']


@pytest.fixture()
def spher_harmonics():
    return SphericalFunctions.SphericalHarmonics(0, 0, ANGLE_TEST_DATA)