#  coding=utf-8
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

from typing import List, Union, Optional as Opt

import numpy as npy
import pandas as pd
from . import _base_vector, three_vector

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class FourVector(_base_vector.VectorMath):
    """DataFrame backed FourVector object for vector operations inside
    PyPWA.
    
    Parameters
    ----------
    x : int, npy.ndarray, float, or DataFrame
        Can be an integer to specify size, a structured array or DataFrame
        with x y z and e values, a single float value, or a Series or
        single dimensional array, If you provide a float, series, or
        array, you need to provide a float for the other options as well.
    y : int, npy.ndarray, float, or DataFrame, optional
    z : int, npy.ndarray, float, or DataFrame, optional
    e : int, npy.ndarray, float, or DataFrame, optional

    See Also
    --------
    ThreeVector : For storing a standard X, Y, Z vector
    Particle : For storing a particle, adds support for a particle ID
    """

    __slots__ = ["_vector"]

    def __init__(
            self,
            x: Union[int, npy.ndarray, float, pd.DataFrame],
            y: Opt[Union[float, pd.Series, npy.ndarray]] = None,
            z: Opt[Union[float, pd.Series, npy.ndarray]] = None,
            e: Opt[Union[float, pd.Series, npy.ndarray]] = None
    ):

        self._vector = _base_vector.sanitize_vector_input(x, y, z, e, True)
        super(FourVector, self).__init__(self._vector)

    def __repr__(self) -> str:
        return f"FourVector(\n{self._vector!r})"

    def __str__(self) -> str:
        if len(self) == 1:
            return f"FourVector(\n{str(self._vector)})"
        else:
            return f"FourVector({self.dataframe.describe()})"

    def __eq__(self, vector: "FourVector") -> bool:
        if isinstance(vector, FourVector):
            return self._vector.equals(vector._vector)
        else:
            return False

    def __truediv__(self, other: Union[float, int]) -> "FourVector":
        if isinstance(other, (int, float)):
            return FourVector(self._div_vectors(other))
        else:
            raise ValueError("FourVectors can only be divided by scalars")

    def __rtruediv__(self, other: Union[float, int]):
        if isinstance(other, (int, float)):
            return FourVector(self._div_vectors(other))
        else:
            raise ValueError("FourVectors can only be divided by scalars")

    def __mul__(self, vector: Union[float, int]) -> "FourVector":
        if isinstance(vector, (int, float)):
            return FourVector(self._mul_vectors(vector))
        else:
            raise ValueError("FourVectors can only be multiplied by scalars")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, vector: Union["FourVector", float]) -> "FourVector":
        if isinstance(vector, FourVector):
            if len(vector) == len(self):
                return FourVector(self._add_vectors(vector._vector))
            else:
                raise ValueError("Vectors have different lengths!")
        elif isinstance(vector, (int, float, npy.float)):
            return FourVector(self._add_vectors(vector))
        else:
            raise ValueError(f"Can not add FourVector and {type(vector)}")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, vector: Union["FourVector", float]) -> "FourVector":
        if isinstance(vector, (int, float, npy.float, FourVector)):
            return self.__add__(-1 * vector)
        else:
            raise ValueError(f"Can not subtract FourVector and {type(vector)}")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __len__(self):
        return len(self._vector)

    def __getitem__(
            self, item: Union[int, str, slice]
    ) -> Union["FourVector", pd.Series]:
        if isinstance(item, slice):
            return FourVector(self._vector[item])
        elif isinstance(item, int):
            return FourVector(self._vector[item])
        elif isinstance(item, str) and item in ("x", "y", "z", "e"):
            return self._vector[item].copy()
        elif isinstance(item, npy.ndarray) and item.dtype == bool:
            return self._vector[item]
        else:
            raise ValueError(f"Can not index with {item!r}")

    def split(self, count) -> List["FourVector"]:
        vectors = []
        for vector in npy.split(self._vector, count):
            vectors.append(FourVector(vector))
        return vectors

    def get_copy(self):
        return FourVector(self._vector.copy())

    def get_dot(self, vector: "FourVector") -> Union[pd.Series, float]:
        if isinstance(vector, FourVector):
            e = self.e * vector.e
            x = self.x * vector.x
            y = self.y * vector.y
            z = self.z * vector.z
            return e - x - y - z
        else:
            raise ValueError("Dot product only works with another FourVector")

    def get_three_vector(self) -> three_vector.ThreeVector:
        return three_vector.ThreeVector(self._vector[["x", "y", "z"]])

    def get_length_squared(self) -> Union[float, npy.ndarray]:
        return self.e**2 - self.get_length()**2

    def get_mass(self) -> Union[float, npy.ndarray]:
        return npy.sqrt(self.get_dot(self))

    @property
    def e(self) -> npy.ndarray:
        return self._vector["e"].copy()

    @e.setter
    def e(self, value: Union[float, npy.ndarray, pd.Series]):
        if isinstance(value, str):
            self._vector['e'] = npy.float64(value)
        else:
            self._vector['e'] = value
