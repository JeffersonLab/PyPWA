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

from PyPWA import LICENSE, STATUS, VERSION

__author__ = ["Stephanie Bramlett", "Mark Jones"]
__credits__ = ["Stephanie Bramlett", "Mark Jones"]
__email__ = "maj@jlab.org"
__maintainer__ = "Mark Jones"
__license__ = LICENSE
__status__ = STATUS
__version__ = VERSION


class ThreeVector(object):

    def __init__(self, x=0, y=0, z=0):
        """

        Args:
            x (numpy.float64):
            y (numpy.float64):
            z (numpy.float64):
        """
        self.x = x
        self.y = y
        self.z = z
        self.vector = [self.x, self.y, self.z]

    def __repr__(self):
        """

        Returns:
            str:
        """
        return str(self.vector)

    def __add__(self, vector):
        """

        Args:
            vector (ThreeVector):

        Returns:
            ThreeVector:
        """
        px = self.x + vector.x
        py = self.y + vector.y
        pz = self.z + vector.z
        return ThreeVector(px, py, pz)

    def __sub__(self, vector):
        """

        Args:
            vector (ThreeVector):

        Returns:
            ThreeVector:
        """
        px = self.x - vector.x
        py = self.y - vector.y
        pz = self.z - vector.z
        return ThreeVector(px, py, pz)

    def __mul__(self, vector):
        """

        Args:
            vector (numpy.float64 | ThreeVector):

        Returns:
            ThreeVector:
        """
        if isinstance(vector, ThreeVector):
            px = self.y * vector.z - self.z * vector.y
            py = self.z * vector.x - self.x * vector.z
            pz = self.x * vector.y - self.y * vector.x
        else:
            px = self.x * vector
            py = self.y * vector
            pz = self.z * vector
        return ThreeVector(px, py, pz)

    def dot(self, three_vec):
        """

        Args:
            three_vec (ThreeVector):

        Returns:
            numpy.float64:
        """
        new_x = self.x * three_vec.x
        new_y = self.y * three_vec.y
        new_z = self.z * three_vec.z
        return new_x + new_y + new_z

    def cos_vector_theta(self, three_vec):
        """

        Args:
            three_vec (ThreeVector):

        Returns:
            numpy.float64:
        """
        if isinstance(three_vec, ThreeVector):
            dot_product = self.dot(three_vec)
            return dot_product / self.length / three_vec.length

    @property
    def length(self):
        return numpy.sqrt(self.x**2 + self.y**2 + self.z**2)

    @property
    def length_square(self):
        return self.length ** 2

    @property
    def cos_theta(self):
        return self.z / self.length

    @property
    def sin_theta(self):
        return (self.x**2 + self.y**2) / self.length

    @property
    def phi(self):
        return numpy.arctan2(self.y, self.x)

    @property
    def theta(self):
        return numpy.arccos(self.cos_theta)
