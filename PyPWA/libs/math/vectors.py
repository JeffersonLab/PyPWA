#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Vector Classes
--------------
These are the 3 and 4 vector classes, though the meat of these classes
are defined in _abstract_vectors.AbstractVectors.
"""

import numpy
from typing import Union

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.math import _abstract_vectors

__credits__ = ["Mark Jones", "Stephanie Bramlett"]
__author__ = AUTHOR
__version__ = VERSION


class ThreeVector(_abstract_vectors.AbstractVector):

    def __init__(self, array):
        # type: (numpy.ndarray) -> None
        super(ThreeVector, self).__init__(array, ThreeVector)

    def __repr__(self):
        # type: () -> str
        return "ThreeVector(x=%s, y=%s, z=%s)" % (
            self['x'], self['y'], self['z']
        )

    def _vector_multiplication(self, other_vector):
        # type: (ThreeVector) -> ThreeVector
        new_x = self.y * other_vector.z - self.z * other_vector.y
        new_y = self.z * other_vector.x - self.x * other_vector.z
        new_z = self.x * other_vector.y - self.y * other_vector.x
        return self.__make_new_vector(new_x, new_y, new_z)

    @staticmethod
    def __make_new_vector(x, y, z):
        # type: (numpy.ndarray, numpy.ndarray, numpy.ndarray) -> ThreeVector
        new_vector = numpy.column_stack((x, y, z))
        new_vector = new_vector.ravel().view(
            [('x', 'f8'), ('y', 'f8'), ('z', 'f8')]
        )
        return ThreeVector(new_vector)

    def _dot_product(self, vector):
        # type: (ThreeVector) -> numpy.ndarray
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def get_length_squared(self):
        # type: () -> numpy.ndarray
        return self.x**2 + self.y**2 + self.z**2


class FourVector(_abstract_vectors.AbstractVector):

    def __init__(self, array):
        # type: (numpy.ndarray) -> None
        super(FourVector, self).__init__(array, FourVector)

    def __repr__(self):
        # type: () -> str
        return "FourVector(x=%s, y=%s, z=%s, e=%s)" % (
            self['x'], self['y'], self['z'], self['e']
        )

    def _vector_multiplication(self, vector):
        raise ValueError("Four Vectors can not be cross multiplied!")

    def _dot_product(self, vector):
        # type: (FourVector) -> numpy.ndarray
        e = self.e * vector.e
        x = self.x * vector.x
        y = self.y * vector.y
        z = self.z * vector.z
        return e - x - y - z

    def get_three_vector(self):
        # type: () -> ThreeVector
        return ThreeVector(self._vector[['x', 'y', 'z']].copy())

    def get_length_squared(self):
        # type: () -> numpy.ndarray
        return self.e**2 - self.get_length()**2

    @property
    def e(self):
        # type: () -> numpy.ndarray
        return self['e']

    @e.setter
    def e(self, value):
        # type: (Union[float, numpy.ndarray]) -> None
        self['e'] = self._validate_input_value(value)
