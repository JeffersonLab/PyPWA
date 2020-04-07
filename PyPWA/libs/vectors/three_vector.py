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
from . import _base_vector

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


class ThreeVector(_base_vector.VectorMath):
    """DataFrame backed ThreeVector object for vector operations inside
    PyPWA.

    Parameters
    ----------
    x : int, npy.ndarray, float, or DataFrame
        Can be an integer to specify size, a structured array or DataFrame
        with x y and z values, a single float value, or a Series or
        single dimensional array, If you provide a float, series, or
        array, you need to provide a float for the other options as well.
    y : int, npy.ndarray, float, or DataFrame, optional
    z : int, npy.ndarray, float, or DataFrame, optional

    See Also
    --------
    FourVector : For storing a vector with it's energy.
    """

    __slots__ = ["_vector"]

    def __init__(
            self,
            x: Union[int, npy.ndarray, float, pd.DataFrame],
            y: Opt[Union[float, pd.Series, npy.ndarray]] = None,
            z: Opt[Union[float, pd.Series, npy.ndarray]] = None
    ):

        self._vector = _base_vector.sanitize_vector_input(x, y, z)
        super(ThreeVector, self).__init__(self._vector)

    def __repr__(self) -> str:
        return f"ThreeVector(\n{self._vector!r})"

    def __str__(self) -> str:
        if len(self) == 1:
            return f"ThreeVector(\n{str(self._vector)})"
        else:
            return f"ThreeVector(\n{self._vector.describe()})"

    def __eq__(self, vector: "ThreeVector") -> bool:
        if isinstance(vector, ThreeVector):
            return self._vector.equals(vector._vector)
        else:
            return False

    def __add__(self, vector: Union["ThreeVector", float]) -> "ThreeVector":
        if isinstance(vector, ThreeVector):
            if len(vector) == len(self):
                return ThreeVector(vector._vector + self._vector)
            else:
                raise ValueError("Vectors have different lengths!")
        elif isinstance(vector, (int, float, npy.float)):
            return ThreeVector(self._vector + vector)
        else:
            raise ValueError(f"Can not add ThreeVector and {type(vector)}")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, vector: Union["ThreeVector", float]) -> "ThreeVector":
        if isinstance(vector, (int, float, npy.float, ThreeVector)):
            return self.__add__(-1 * vector)
        else:
            raise ValueError(f"Can not subtract ThreeVector and {type(vector)}")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, vector: Union["ThreeVector", float]) -> "ThreeVector":
        if isinstance(vector, ThreeVector):
            new_x = self.y * vector.z - self.z * vector.y
            new_y = self.z * vector.x - self.x * vector.z
            new_z = self.x * vector.y - self.y * vector.x
            return ThreeVector(new_x, new_y, new_z)
        elif isinstance(vector, (int, float, npy.float)):
            return ThreeVector(vector * self._vector)
        else:
            raise ValueError(f"Can not multiply ThreeVector by {type(vector)}")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __len__(self):
        return len(self._vector)

    def __getitem__(
            self, item: Union[int, str, slice]
    ) -> Union["ThreeVector", pd.Series]:
        if isinstance(item, slice):
            return ThreeVector(self._vector.loc[item])
        elif isinstance(item, int):
            return ThreeVector(self._vector.iloc[item])
        elif isinstance(item, str) and item in ("x", "y", "z"):
            return self._vector[item].copy()
        elif isinstance(item, npy.ndarray) and item.dtype == bool:
            return self._vector[item]
        else:
            raise ValueError(f"Can not index with {item!r}")

    def split(self, count) -> List["ThreeVector"]:
        vectors = []
        for vector in npy.split(self._vector, count):
            vectors.append(ThreeVector(vector))
        return vectors

    def get_copy(self):
        return ThreeVector(self._vector.copy())

    def get_dot(self, vector: "ThreeVector") -> Union[pd.Series]:
        if isinstance(vector, ThreeVector):
            return self.x * vector.x + self.y * vector.y + self.z * vector.z
        else:
            raise ValueError("Dot product only works with another ThreeVector")

    def get_length_squared(self) -> Union[pd.Series, float]:
        return self.x**2 + self.y**2 + self.z**2
