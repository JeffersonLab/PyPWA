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
The backbone of all vectors
---------------------------
This is the base abstract class for the vectors inside PyPWA, this is
what allows for them to split, be iterated over, compared, accessed like
a dictionary, and have properties. It even contains some mathematics and
error checking that _should_ be universal for all vectors.
"""

from typing import List, Union, Tuple

import numpy

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class _VectorIterator(object):

    def __init__(self, vector_class, vector_array, array_type):
        self.__class = vector_class
        self.__array = vector_array
        self.__type = array_type
        self.__index = -1

    def __repr__(self):
        return "{0}({1!r}, {2!r}, {3!r})".format(
            self.__class__.__name__,
            self.__class, self.__array, self.__type
        )

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        try:
            self.__index += 1
            new_array = numpy.array(self.__array[self.__index], self.__type)
            return self.__class(new_array)
        except IndexError:
            raise StopIteration


class AbstractVector(object):

    # Slots can be used for improved memory usage and performance.
    # Here they are used for type safety, this prevents you from assigning
    # a ThreeVector an e component by accident.
    __slots__ = ['_array_type', '_vector', '__vector_class']

    def __init__(
            self,
            array,  # type: Union[numpy.ndarray, int]
            vector_class,  # type: type(self)
            array_type,  # type: List[Tuple[str, str]]
    ):
        # type: (...) -> None
        if isinstance(array, int):
            self._vector = numpy.zeros(array, dtype=array_type)
        else:
            self._vector = array
        self._array_type = array_type
        self.__vector_class = vector_class

    def __repr__(self):
        # type: () -> str
        return "{0}({1!r})".format(
            self.__class__.__name__, self._vector
        )

    def __eq__(self, other):
        # type: (type(self)) -> bool
        array = other.get_array()
        return (array == self._vector).all()

    def __add__(self, vector):
        # type: (type(self)) -> type(self)
        new_vector = numpy.zeros(len(self), self._vector.dtype)
        for name in self._vector.dtype.names:
            new_vector[name] = self._vector[name] + vector.get_array()[name]
        return self.__vector_class(new_vector)

    def __sub__(self, vector):
        # type: (type(self)) -> type(self)
        new_vector = numpy.zeros(len(self), self._vector.dtype)
        for name in self._vector.dtype.names:
            new_vector[name] = self._vector[name] - vector.get_array()[name]
        return self.__vector_class(new_vector)

    def __mul__(self, vector):
        # type: (Union[float, type(self)]) -> type(self)
        if isinstance(vector, self.__vector_class):
            return self._vector_multiplication(vector)
        else:
            return self.__multiply_by_scalar(vector)

    def _vector_multiplication(self, vector):
        # type: (type(self)) -> type(self)
        raise NotImplementedError

    def __multiply_by_scalar(self, scalar):
        # type: (float) -> numpy.ndarray
        new_vector = numpy.zeros(len(self), self._vector.dtype)
        for name in self._vector.dtype.names:
            new_vector[name] = self._vector[name] * scalar
        return self.__vector_class(new_vector)

    def __len__(self):
        # type: () -> int
        return len(self._vector)

    def __iter__(self):
        return _VectorIterator(
            self.__vector_class, self._vector, self._array_type
        )

    def __getitem__(self, item):
        # type: (int) -> self(type)
        new_array = numpy.array([self._vector[item]], self._array_type)
        return self.__vector_class(new_array)

    def get_copy(self):
        # type: () -> type(self)
        return self.__vector_class(self._vector.copy())

    def get_array(self):
        # type: () -> numpy.ndarray
        return self._vector

    def get_dot(self, vector):
        # type: (type(self)) -> type(self)
        if isinstance(vector, self.__vector_class):
            return self._dot_product(vector)
        else:
            raise ValueError("Can only dot product vectors of the same type!")

    def _dot_product(self, vector):
        # type: (type(self)) -> type(self)
        raise NotImplementedError

    def split(self, count):
        # type: (int) -> List[self]
        new_vectors = numpy.split(self._vector, count)
        return [self.__vector_class(vector) for vector in new_vectors]

    def get_length(self):
        # type: () -> numpy.ndarray
        return numpy.sqrt(self.x**2 + self.y**2 + self.z**2)

    def get_theta(self):
        # type: () -> numpy.ndarray
        return numpy.arccos(self.get_cos_theta())

    def get_phi(self):
        # type: () -> numpy.ndarray
        return numpy.arctan2(self.y, self.x)

    def get_sin_theta(self):
        # type: () -> numpy.ndarray
        return (self.x**2 + self.y**2) / self.get_length()

    def get_cos_theta(self):
        # type: () -> numpy.ndarray
        return self.z / self.get_length()

    @property
    def x(self):
        # type: () -> numpy.ndarray
        return self._vector['x']

    @x.setter
    def x(self, value):
        # type: (Union[float, numpy.ndarray]) -> None
        self._vector['x'] = value

    @property
    def y(self):
        # type: () -> numpy.ndarray
        return self._vector['y']

    @y.setter
    def y(self, value):
        # type: (Union[float, numpy.ndarray]) -> None
        self._vector['y'] = value

    @property
    def z(self):
        # type: () -> numpy.ndarray
        return self._vector['z']

    @z.setter
    def z(self, value):
        # type: (Union[float, numpy.ndarray]) -> None
        self._vector['z'] = value
