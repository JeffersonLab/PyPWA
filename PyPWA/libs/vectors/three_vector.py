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

import numpy as np
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
            x: Union[int, np.ndarray, float, pd.DataFrame],
            y: Opt[Union[float, pd.Series, np.ndarray]] = None,
            z: Opt[Union[float, pd.Series, np.ndarray]] = None
    ):
        if isinstance(x, ThreeVector):
            self._x = x._x
            self._y = x._y
            self._z = x._z
        self._x, self._y, self._z = _base_vector.sanitize_vector_input(x, y, z)
        super(ThreeVector, self).__init__(self._x, self._y, self._z)

    def __repr__(self) -> str:
        return f"ThreeVector(x={self._x}, y={self._y}, z={self._z})"

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text("ThreeVector( ?.)")
        else:
            if isinstance(self._x, np.ndarray):
                if all(self._z) == 0.0:
                    theta = np.NaN
                else:
                    theta = self.get_theta().mean()

                phi = self.get_phi().mean()
            else:
                if self._z == 0:
                    theta = np.NaN
                else:
                    theta = self.get_theta()

                phi = self.get_phi()

            p.text(f"ThreeVector(x̅Θ={theta}, x̅ϕ={phi})")

    def __eq__(self, vector: "ThreeVector") -> bool:
        if isinstance(vector, ThreeVector):
            if isinstance(self._x, np.ndarray):
                return (
                    all(self._x == vector._x) and all(self._y == vector._y) and
                    all(self._z == vector._z)
                )
            else:
                return (
                        self._x == vector._x and self._y == vector._y and
                        self._z == vector._z
                )
        else:
            return False

    def __add__(self, vector: Union["ThreeVector", float]) -> "ThreeVector":
        if isinstance(vector, ThreeVector):
            if len(vector) == len(self):
                return ThreeVector(
                    self._x + vector._x, self._y + vector._y,
                    self._z + vector._z
                )
            else:
                raise ValueError("Vectors have different lengths!")
        elif isinstance(vector, (int, float, np.float)):
            return ThreeVector(
                self._x + vector, self._y + vector, self._z + vector
            )
        else:
            raise ValueError(f"Can not add ThreeVector and {type(vector)}")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, vector: Union["ThreeVector", float]) -> "ThreeVector":
        if isinstance(vector, (int, float, np.float, ThreeVector)):
            return self.__add__(-1 * vector)
        else:
            raise ValueError(f"Can not subtract ThreeVector and {type(vector)}")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, vector: Union["ThreeVector", float]) -> "ThreeVector":
        if isinstance(vector, ThreeVector):
            new_x = self._y * vector._z - self._z * vector._y
            new_y = self._z * vector._x - self._x * vector._z
            new_z = self._x * vector._y - self._y * vector._x
            return ThreeVector(new_x, new_y, new_z)
        elif isinstance(vector, (int, float, np.float)):
            return ThreeVector(
                self._x * vector, self._y * vector, self._z * vector
            )
        else:
            raise ValueError(f"Can not multiply ThreeVector by {type(vector)}")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __len__(self):
        return len(self._vector)

    def __getitem__(
            self, item: Union[int, str, slice]
    ) -> Union["ThreeVector", pd.Series]:
        if isinstance(item, (slice, int)) or \
                isinstance(item, np.ndarray) and item.dtype == bool:
            return ThreeVector(
                self._x[item], self._y[item], self._z[item]
            )
        elif isinstance(item, str) and item in ("x", "y", "z"):
            return getattr(self, f"_{item}").copy()
        else:
            raise ValueError(f"Can not index with {item!r}")

    def split(self, count) -> List["ThreeVector"]:
        vectors = []
        xs = np.split(self._x, count)
        ys = np.split(self._y, count)
        zs = np.split(self._z, count)
        for x, y, z in zip(xs, ys, zs):
            vectors.append(ThreeVector(x, y, z))
        return vectors

    def get_copy(self):
        return ThreeVector(self._x.copy(), self._y.copy(), self._z.copy())

    def get_dot(self, vector: "ThreeVector") -> np.ndarray:
        if isinstance(vector, ThreeVector):
            return (
                    self._x * vector._x + self._y * vector._y +
                    self._z * vector._z
            )
        else:
            raise ValueError("Dot product only works with another ThreeVector")

    def get_length_squared(self) -> Union[np.ndarray, float]:
        return self._x**2 + self._y**2 + self._z**2
