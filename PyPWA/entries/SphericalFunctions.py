import re
import os

import numpy
import spherical_functions


class _BreakupData(object):

    def __init__(self, data):
        self.__split_data(data)

    def __split_data(self, file):
        self.__theta_array = numpy.loadtxt(file, usecols=0)
        self.__phi_array = numpy.loadtxt(file, usecols=1)

    def theta(self):
        return self.__theta_array

    def phi(self):
        return self.__phi_array


class SphericalHarmonics(object):

    def __init__(self, ell, m, data):
        mp = 0
        gamma = 0
        self.__results_sum = None
        self.__find_angles = _BreakupData(data)
        self.__calculate_harmonics(gamma, ell, mp, m)

    def __calculate_harmonics(self, gamma, ell, mp, m):
        spherical_funcs = []
        theta_array = self.__find_angles.theta()
        phi_array = self.__find_angles.phi()
        events = len(phi_array)

        for i in range(0, events):
            spherical_funcs.append(
                spherical_functions.Wigner_D_element(
                    phi_array[i], theta_array[i], gamma, ell, mp, m
                )
            )
        self.__create_numpy_array(spherical_funcs)

    def __create_numpy_array(self, result):
        result_numpy = numpy.array(result)
        self.__results_sum = result_numpy.sum()

    def get_results(self):
        return self.__results_sum
