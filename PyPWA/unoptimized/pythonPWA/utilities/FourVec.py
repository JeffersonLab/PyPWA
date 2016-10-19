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

import numpy

from PyPWA.unoptimized.pythonPWA.utilities.ThreeVec import ThreeVector
from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Stephanie Bramlett", "Mark Jones"]
__credits__ = ["Stephanie Bramlett", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


class FourVector(tuple):

    def __init__(self, energy, x=0, y=0, z=0, three_vec=False):
        """

        Args:
            energy (numpy.float64):
            x (numpy.float64):
            y (numpy.float64):
            z (numpy.float64):
            three_vec (ThreeVector):
        """
        super(FourVector, self).__init__()

        self.energy = energy
        if three_vec:
            self.x = three_vec.x
            self.y = three_vec.y
            self.z = three_vec.z
        else:
            self.x = x
            self.y = y
            self.z = z

        self.three_vector = ThreeVector(x, y, z)

    def __repr__(self):
        """

        Returns:
            str:
        """
        return str([self.energy, self.x, self.y, self.z])

    def __add__(self, four_vector):
        """

        Args:
            four_vector (FourVector):

        Returns:
            FourVector:
        """
        sum_energy = self.energy + four_vector.energy
        sum_x = self.x + four_vector.x
        sum_y = self.y + four_vector.y
        sum_z = self.z + four_vector.z
        return FourVector(sum_energy, sum_x, sum_y, sum_z)

    def __sub__(self, four_vector):
        """

        Args:
            four_vector (FourVector):

        Returns:
            FourVector:
        """
        difference_energy = self.energy - four_vector.energy
        difference_x = self.x - four_vector.x
        difference_y = self.y - four_vector.y
        difference_z = self.z - four_vector.z

        return FourVector(
            difference_energy, difference_x, difference_y, difference_z
        )

    def times(self, lorentz_transform):
        """

        Args:
            lorentz_transform (LorentzTransform):

        Returns:
            FourVector
        """
        transposed = self.matrix.transpose()
        the_list = transposed.dot(lorentz_transform.m).flatten().tolist()
        vectors = the_list[0]
        return FourVector(vectors[0], vectors[1], vectors[2], vectors[3])

    def dot(self, four_vector):
        dot_energy = self.energy * four_vector.E
        dot_x = self.x * four_vector.x
        dot_y = self.y * four_vector.y
        dot_z = self.z * four_vector.z
        return dot_energy - dot_x - dot_y - dot_z

    @property
    def matrix(self):
        return numpy.matrix([[self.energy], [self.x], [self.y], [self.z]])

    @property
    def length(self):
        x_squared = numpy.float64(self.x**2)
        y_squared = numpy.float64(self.y**2)
        z_squared = numpy.float64(self.z**2)
        return numpy.sqrt(x_squared + y_squared + z_squared)

    @property
    def length_squared(self):
        energy_squared = numpy.float64(self.energy) ** 2
        length_squared = numpy.float64(self.length) ** 2
        return energy_squared - length_squared

    @property
    def phi(self):
        return self.three_vector.phi()

    @property
    def theta(self):
        return self.three_vector.theta()

    @property
    def cos_theta(self):
        return self.three_vector.cos_theta



