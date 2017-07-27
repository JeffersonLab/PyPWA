import os
import re

import numpy
import pytest
import spherical_functions

from PyPWA.entries import SphericalFunctions

ANGLE_TEST_DATA = os.path.join(
    os.path.dirname(__file__), "../data/test_docs/angles.txt"
)


@pytest.fixture()
def file_parser():
    return SphericalFunctions._BreakupData(ANGLE_TEST_DATA)


@pytest.fixture()
def data_splitter():
    theta_list = numpy.loadtxt(ANGLE_TEST_DATA, usecols=0)
    phi_list = numpy.loadtxt(ANGLE_TEST_DATA, usecols=1)

    yield theta_list, phi_list


def test_reading(file_parser, data_splitter):
    numpy.testing.assert_array_equal(file_parser.theta(), data_splitter[0])
    numpy.testing.assert_array_equal(file_parser.phi(), data_splitter[1])


@pytest.fixture()
def sphere_harmonics():
    return SphericalFunctions.SphericalHarmonics(0, 0, ANGLE_TEST_DATA)


@pytest.fixture()
def calculate_harmonics(data_splitter):
    sph = []
    theta_list = data_splitter[0]
    phi_list = data_splitter[1]
    for i in range(0, len(phi_list)):
        sph.append(
            spherical_functions.Wigner_D_element(
                theta_list[i], phi_list[i], 0, 0, 0, 0
            )
        )
    numpy_arr = numpy.array(sph).sum()
    return numpy_arr


def test_harmonics(sphere_harmonics, calculate_harmonics):
    assert sphere_harmonics.get_results() == calculate_harmonics
