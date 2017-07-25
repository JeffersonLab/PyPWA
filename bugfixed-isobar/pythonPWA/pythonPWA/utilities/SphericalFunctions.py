import numpy
import spherical_functions
import sys

class BreakupData(object):
    def __init__(self, data):
        self.split_data(data)
        self.theta_line = list
        self.phi_line = list

    def split_data(self, data):
        self.theta_line = data.readline()
        self.phi_line = data.readline()

    def theta(self):
        return self.theta_line

    def phi(self):
        return self.phi_line


class SphericalHarmonics(object):

    def __init__(self, ell, m, data):
        find_angles = BreakupData(data)
        theta = find_angles.theta()
        phi = find_angles.phi()
        self.calculate_harmonics(ell, m, theta, phi)


    def calculate_harmonics(self, ell, m, theta, phi):

        for angle1 in phi:
            for 
        self.results = \
            spherical_functions.Wigner_D_element(angle1, angle2, 0, ell, m)


    def get_results(self):
        return self.results





if __name__ == "__main__":
    #data = file with theta and phi (alpha and beta)
    data = open('data', 'r')
    spherical_harmonics_calculation =\
        SphericalHarmonics(sys.argv[1], sys.argv[2], data)
    list_of_calculations = spherical_harmonics_calculation.get_results()
    print(list_of_calculations)