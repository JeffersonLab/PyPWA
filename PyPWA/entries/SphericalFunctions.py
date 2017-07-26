import spherical_functions
import numpy
import re

class _BreakupData(object):

    def __init__(self, data):
        self.__theta_list = []
        self.__phi_list = []
        self.events = 0
        with open(data, 'r') as file:
            self.__split_data(file)

    def __split_data(self, file):
        for line in file:
            temp_list = re.split('\s', line)
            self.__theta_list.append(float(temp_list[0]))
            self.__phi_list.append(float(temp_list[1]))
            self.events += 1

    def theta(self):
        return self.__theta_list

    def phi(self):
        return self.__phi_list


class SphericalHarmonics(object):

    def __init__(self, ell, m, data):
        mp = 0
        gamma = 0
        self.__results_sum = None
        self.__find_angles = _BreakupData(data)
        self.__calculate_harmonics(gamma, ell, mp, m)

    def __calculate_harmonics(self, gamma, ell, mp, m):
        sph = []
        events = self.__find_angles.events
        theta_list = self.__find_angles.theta()
        phi_list = self.__find_angles.phi()

        for i in range(0, events):
            sph.append(spherical_functions.Wigner_D_element(phi_list[i],
                                                       theta_list[i],
                                                       gamma, ell, mp, m))
        self.__create_numpy_array(sph)

    def __create_numpy_array(self, result):
        result_numpy = numpy.array(result)
        self.__results_sum = result_numpy.sum()

    def get_results(self):
        return self.__results_sum
