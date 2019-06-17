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

import numpy as npy
from typing import Union, Optional as Opt

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.math.vectors import _abstract_vectors

__credits__ = ["Mark Jones", "Stephanie Bramlett"]
__author__ = AUTHOR
__version__ = VERSION


class ThreeVector(_abstract_vectors.AbstractVector):

    __slots__ = []

    def __init__(
            self,
            x: Union[int, npy.ndarray, float, str],
            y: Opt[Union[str, float]] = 0,
            z: Opt[Union[str, float]] = 0,
            precision: npy.floating = npy.float64
    ):
        array_type = [('x', precision), ('y', precision), ('z', precision)]
        if y or z:
            array = npy.array([(x, y, z)], array_type)
        else:
            array = x

        super(ThreeVector, self).__init__(array, ThreeVector, array_type)

    def __str__(self) -> str:
        if len(self) == 1:
            return f"ThreeVector(x={self.x[0]}, y={self.y[0]}, z={self.z[0]})"
        else:
            return f"ThreeVector(x, y, z; len={len(self)})"

    def _vector_multiplication(
            self, other_vector: "ThreeVector") -> "ThreeVector":
        new_x = self.y * other_vector.z - self.z * other_vector.y
        new_y = self.z * other_vector.x - self.x * other_vector.z
        new_z = self.x * other_vector.y - self.y * other_vector.x
        return self.__make_new_vector(new_x, new_y, new_z)

    def __make_new_vector(
            self, x: npy.ndarray, y: npy.ndarray, z: npy.ndarray
    ) -> "ThreeVector":
        new_vector = npy.column_stack((x, y, z))
        new_vector = new_vector.ravel().view(self._array_type)
        return ThreeVector(new_vector)

    def _dot_product(self, vector: "ThreeVector") -> npy.ndarray:
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def get_length_squared(self) -> npy.ndarray:
        return self.x**2 + self.y**2 + self.z**2


class FourVector(_abstract_vectors.AbstractVector):

    __slots__ = []

    def __init__(
            self,
            x: Union[int, npy.ndarray, float, str],
            y: Opt[Union[str, float]] = None,
            z: Opt[Union[str, float]] = None,
            e: Opt[Union[str, float]] = None,
            precision: npy.floating = npy.float64
    ):
        array_type = [
            ('x', precision), ('y', precision),
            ('z', precision), ('e', precision)
        ]
        if False in [isinstance(v, type(None)) for v in (y, z, e)]:
            array = npy.asarray([(x, y, z, e)], array_type)
        else:
            array = x

        super(FourVector, self).__init__(array, FourVector, array_type)

    def __str__(self) -> str:
        if len(self._vector) == 1:
            return (
                f"FourVector"
                f"(x={self.x[0]}, y={self.y[0]}, z={self.z[0]}, e={self.e[0]})"
            )
        else:
            return f"FourVector(x, y, z, e; len={len(self)})"

    def _vector_multiplication(self, vector):
        raise ValueError("Four Vectors can not be cross multiplied!")

    def _dot_product(self, vector: "FourVector") -> npy.ndarray:
        e = self.e * vector.e
        x = self.x * vector.x
        y = self.y * vector.y
        z = self.z * vector.z
        return e - x - y - z

    def get_three_vector(self) -> ThreeVector:
        return ThreeVector(self._vector[['x', 'y', 'z']].copy())

    def get_length_squared(self) -> npy.ndarray:
        return self.e**2 - self.get_length()**2

    def get_mass(self):
        return npy.sqrt(self.get_dot(self))

    @property
    def e(self) -> npy.ndarray:
        return self._vector['e']

    @e.setter
    def e(self, value: Union[float, npy.ndarray]):
        self._vector['e'] = value
