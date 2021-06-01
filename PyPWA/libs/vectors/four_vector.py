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

import numpy as np
import pandas
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
    e : int, np.ndarray, float, or DataFrame
        Can be an integer to specify size, a structured array or DataFrame
        with x y z and e values, a single float value, or a Series or
        single dimensional array, If you provide a float, series, or
        array, you need to provide a float for the other options as well.
    x : int, np.ndarray, float, or Series, optional
    y : int, np.ndarray, float, or Series, optional
    z : int, np.ndarray, float, or Series, optional

    See Also
    --------
    ThreeVector : For storing a standard X, Y, Z vector
    Particle : For storing a particle, adds support for a particle ID
    """

    __slots__ = ["_x", "_y", "_z", "_e"]

    def __init__(
            self,
            e: Union[int, np.ndarray, float, pd.DataFrame],
            x: Opt[Union[float, pd.Series, np.ndarray]] = None,
            y: Opt[Union[float, pd.Series, np.ndarray]] = None,
            z: Opt[Union[float, pd.Series, np.ndarray]] = None
    ):
        if isinstance(e, FourVector):
            self._e = e._e
            self._x = e._x
            self._y = e._y
            self._z = e._z
        else:
            self._e, self._x, self._y, self._z = \
                _base_vector.sanitize_vector_input(e, x, y, z, True)
        super(FourVector, self).__init__(self._x, self._y, self._z)

    def __repr__(self):
        return f"FourVector(e={self.e}, x={self.x}, y={self.y}, z={self.z})"

    def _repr_html_(self):
        df = pandas.DataFrame()
        df['Θ'] = self.get_theta()
        df['̅ϕ'] = self.get_phi()
        df['Mass'] = self.get_mass()
        return df._repr_html_()

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text("FourVector( ?.)")

        else:
            theta, phi, mass = self._get_repr_data()
            p.text(f"FourVector(x̅Θ={theta}, x̅ϕ={phi}, x̅Mass={mass})")

    def _get_repr_data(self):
        # Theta needs to be set to NaN if we're working with
        # uninitialized values
        if isinstance(self._e, np.ndarray):
            if all(self._z) == 0.0:
                theta = np.NaN
            else:
                theta = self.get_theta().mean()

            phi = self.get_phi().mean()
            mass = self.get_mass().mean()
        else:
            if self._z == 0.0:
                theta = np.NaN
            else:
                theta = self.get_theta()

            phi = self.get_phi()
            mass = self.get_mass()
        return theta, phi, mass

    def display_raw(self):
        df = pandas.DataFrame()
        df['e'], df['x'] = self.e, self.x
        df['y'], df['z'] = self.y, self.z
        print(df)

    def __eq__(self, vector: "FourVector") -> bool:
        return self._compare_vectors(vector)

    def _compare_vectors(self, other):
        if all([hasattr(other, attr)] for attr in self.__slots__):
            equality = []
            for slot in self.__slots__:
                result = np.equal(getattr(self, slot), getattr(other, slot))

                if isinstance(self._x, np.ndarray):
                    equality.append(all(result))
                else:
                    equality.append(result)

            return all(equality)

        else:
            return False

    def __truediv__(self, scalar: Union[float, int]) -> "FourVector":
        if isinstance(scalar, (int, float)):
            return FourVector(
                self._e / scalar, self._x / scalar,
                self._y / scalar, self._z / scalar
            )
        else:
            raise ValueError("FourVectors can only be divided by scalars")

    def __rtruediv__(self, other: Union[float, int]):
        return self.__truediv__(other)

    def __mul__(self, scalar: Union[float, int]) -> "FourVector":
        if isinstance(scalar, (int, float)):
            return FourVector(
                self._e * scalar, self._x * scalar,
                self._y * scalar, self._z * scalar
            )
        else:
            raise ValueError("FourVectors can only be multiplied by scalars")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, vector: Union["FourVector", float]) -> "FourVector":
        if isinstance(vector, FourVector):
            if len(vector) == len(self):
                return FourVector(
                    self._e + vector._e, self._x + vector._x,
                    self._y + vector._y, self._z + vector._z
                )
            else:
                raise ValueError("Vectors have different lengths!")
        elif isinstance(vector, (int, float)):
            return FourVector(
                self._e + vector, self._x + vector,
                self._y + vector, self._z + vector
            )
        else:
            raise ValueError(f"Can not add FourVector and {type(vector)}")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, vector: Union["FourVector", float]) -> "FourVector":
        if isinstance(vector, (int, float, FourVector)):
            return self.__add__(-1 * vector)
        else:
            raise ValueError(f"Can not subtract FourVector and {type(vector)}")

    def __rsub__(self, other):
        return self.__sub__(other)

    def __len__(self):
        if isinstance(self._x, float):
            return 0
        return len(self._x)

    def __getitem__(
            self, item: Union[int, str, slice]
    ) -> Union["FourVector", pd.Series]:
        if isinstance(item, (slice, int)) or \
                isinstance(item, np.ndarray) and item.dtype == bool:
            return FourVector(
                self._e[item], self._x[item], self._y[item], self._z[item]
            )
        elif isinstance(item, str) and item in ("e", "x", "y", "z"):
            return getattr(self, f"_{item}").copy()
        else:
            raise ValueError(f"Can not index with {item!r}")

    def split(self, count) -> List["FourVector"]:
        vectors = []
        es = np.split(self._e, count)
        xs = np.split(self._x, count)
        ys = np.split(self._y, count)
        zs = np.split(self._z, count)
        for e, x, y, z in zip(es, xs, ys, zs):
            vectors.append(FourVector(e, x, y, z))
        return vectors

    def get_copy(self):
        return FourVector(
            self._e.copy(), self._x.copy(), self._y.copy(), self._z.copy()
        )

    def get_dot(self, vector: "FourVector") -> Union[pd.Series, float]:
        if isinstance(vector, FourVector):
            e = self._e * vector._e
            x = self._x * vector._x
            y = self._y * vector._y
            z = self._z * vector._z
            return e - x - y - z
        else:
            raise ValueError("Dot product only works with another FourVector")

    def get_three_vector(self) -> three_vector.ThreeVector:
        return three_vector.ThreeVector(self._x, self._y, self._z)

    def get_length_squared(self) -> Union[float, np.ndarray]:
        return self._e**2 - self.get_length()**2

    def get_mass(self) -> Union[float, np.ndarray]:
        return np.sqrt(self.get_dot(self))

    @property
    def e(self) -> Union[float, np.ndarray]:
        if isinstance(self._e, np.ndarray):
            return self._e.copy()
        return self._e

    @e.setter
    def e(self, value: Union[float, np.ndarray, pd.Series]):
        if isinstance(value, np.ndarray):
            if len(value) != len(self._e):
                raise ValueError("Size does not match vector!")
            self._e = value
        else:
            self._e *= 0
            self._e += np.float64(value)
