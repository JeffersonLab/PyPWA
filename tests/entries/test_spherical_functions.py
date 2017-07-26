import pytest
import os
import re
import numpy
import spherical_functions
from PyPWA.entries import SphericalFunctions
ANGLE_TEST_DATA = os.path.join(os.path.dirname(__file__),
                               "../data/test_docs/angles.txt")


@pytest.fixture()
def file_parser():
    return SphericalFunctions._BreakupData(ANGLE_TEST_DATA)


@pytest.fixture()
def data_splitter():
    theta_list = []
    phi_list = []
    with open(ANGLE_TEST_DATA,  'r') as file:
        for line in file:
            temp_list = re.split('\s', line)
            theta_list.append(float(temp_list[0]))
            phi_list.append(float(temp_list[1]))

    yield theta_list, phi_list

def test_reading(file_parser, data_splitter):
    assert file_parser.theta() == data_splitter[0]
    assert file_parser.phi() == data_splitter[1]


@pytest.fixture()
def sphere_harmonics():
    return SphericalFunctions.SphericalHarmonics(0, 0, ANGLE_TEST_DATA)

@pytest.fixture()
def calculate_harmonics(file_parser, data_splitter):
    sph = []
    theta_list = data_splitter[0]
    phi_list = data_splitter[1]
    for i in range(0, file_parser.events):
        sph.append(spherical_functions.Wigner_D_element(theta_list[i],
                                                        phi_list[i],
                                                        0, 0, 0, 0))
    numpy_arr = numpy.array(sph).sum()
    return numpy_arr


def test_harmonics(sphere_harmonics, calculate_harmonics):
    assert sphere_harmonics.get_results() == calculate_harmonics
