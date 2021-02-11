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

from typing import List, Union, Tuple, Optional as Opt

import numpy as np
import pandas
from PyPWA.libs.vectors import FourVector
from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


_PROTON_GEV = .9382720813


def get_particle_by_id(particle_id: int) -> Tuple[str, int]:
    """
    ... seealso::
        https://www.star.bnl.gov/public/comp/simu/gstar/Manual/particle_id.html

    :return: Tuple containing particle's name, particle's charge
    """
    return {
        1:  ('Gamma', 0),         2:  ('Positron', 1),
        3:  ('Electron', -1),     4:  ('Neutrino', 0),
        5:  ('Muon +', 1),        6:  ('Muon -', -1),
        7:  ('Pion 0', 0),        8:  ('Pion +', 1),
        9:  ('Pion -', -1),       10: ('Kaon 0 Long', 0),
        11: ('Kaon +', 1),        12: ('Kaon -', -1),
        13: ('Neutron', 0),       14: ('Proton', 1),
        15: ('Antiproton', -1),   16: ('Kaon 0 Short', 0),
        17: ('Eta', 0),           18: ('Lambda', 0),
        19: ('Sigma +', 1),       20: ('Sigma 0', 0),
        21: ('Sigma -', -1),      22: ('Xi 0', 0),
        23: ('Xi -', -1),         24: ('Omega -', -1),
        25: ('Antineutron', 0),   26: ('Antilambda', 0),
        27: ('Antisigma -', -1),  28: ('Antisigma 0', 0),
        29: ('Antisigma +', 1),   30: ('Antixi 0', 0),
        31: ('Antixi +', 1),      32: ('Antiomega +', 1),
        45: ('Deuteron', 1),      46: ('Triton', 1),
        47: ('Alpha', 2),         48: ('Geantino', 0),
        49: ('He3', 2),           50: ('Cerenkov', 0)
    }[particle_id]


class Particle(FourVector):
    """Numpy backed Particle object for vector operations inside
    PyPWA.

    Parameters
    ----------
    particle_id : int
        The Particle ID, used to determine the particle's name and charge.
    e : int, npy.ndarray, float, or DataFrame
        Can be an integer to specify size, a structured array or DataFrame
        with x y z and e values, a single float value, or a Series or
        single dimensional array, If you provide a float, series, or
        array, you need to provide a float for the other options as well.
    x : int, npy.ndarray, float, or DataFrame, optional
    y : int, npy.ndarray, float, or DataFrame, optional
    z : int, npy.ndarray, float, or DataFrame, optional

    See Also
    --------
    FourVector : For storing a FourVector without particle ID
    ParticlePool : For storing a collection of particles
    """

    __slots__ = ["_vector", "__particle_id", "__particle_name", "__charge"]

    def __init__(
            self,
            particle_id: int,
            e: Union[int, np.ndarray, float, pandas.DataFrame],
            x: Opt[Union[float, pandas.Series, np.ndarray]] = None,
            y: Opt[Union[float, pandas.Series, np.ndarray]] = None,
            z: Opt[Union[float, pandas.Series, np.ndarray]] = None
    ):
        super(Particle, self).__init__(e, x, y, z)
        self.__particle_id = particle_id
        self.__particle_name, self.__charge = get_particle_by_id(particle_id)

    def __eq__(self, other: "Particle") -> bool:
        arrays_equal = self._compare_vectors(other)
        id_equals = self.id == other.id
        return arrays_equal and id_equals

    def __repr__(self) -> str:
        return (
            f"Particle(id={self.__particle_id}, e={self.e},"
            f" x={self.x}, y={self.y}, z={self.z})"
        )

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text("Particle( ?.)")
        else:
            theta, phi, mass = self._get_repr_data()
            p.text(
                f"Particle("
                f"Name={self.__particle_name}"
                f" PID={self.__particle_id},"
                f" x̅Θ={theta},"
                f" x̅ϕ={phi},"
                f" x̅Mass={mass})"
            )

    def __getitem__(
            self, item: Union[int, str, slice]
    ) -> Union["Particle", pandas.Series]:
        if isinstance(item, (int, slice)) or \
                isinstance(item, np.ndarray) and item.dtype == bool:
            return Particle(
                self.__particle_id, self._e, self._x, self._y, self._z
            )
        elif isinstance(item, str) and item in ("x", "y", "z", "e"):
            return getattr(self, f"_{item}").copy()
        else:
            raise ValueError(f"Can not index with {item!r}")

    def split(self, count: int) -> List["Particle"]:
        """
        Splits the Particle for distributed computing.

        Will return N Particles which together will have the same number
        of elements as the original Particle.

        Parameters
        ----------
        count : int
            The amount of Particles to produce from current particle.

        Returns
        -------
        List[Particle] :
            The list of Particles

        """
        particles = []
        es = np.split(self._e, count)
        xs = np.split(self._x, count)
        ys = np.split(self._y, count)
        zs = np.split(self._z, count)
        for e, x, y, z in zip(es, xs, ys, zs):
            particles.append(Particle(self.__particle_id, e, x, y, z))
        return particles

    def get_copy(self):
        """
        Returns a deep copy of the Particle.

        Returns
        -------
        Particle:
            Copy of the particle.
        """

        return Particle(
            self.__particle_id, self._e.copy(), self._x.copy(),
            self._y.copy(), self._z.copy()
        )

    @property
    def id(self) -> int:
        """
        Immutable provided ID at initialization.
        """
        return self.__particle_id

    @property
    def name(self) -> str:
        """
        Immutable name for the particle produced from the ID.
        """
        return self.__particle_name

    @property
    def charge(self) -> int:
        """
        Immutable charge for the particle produced from the ID.
        """
        return self.__charge


class _PoolEventIterator:

    def __init__(self, particle_list: List[Particle]):
        self.__pool = particle_list
        self.__iteration_index = -1

    def __repr__(self) -> str:
        return f"_PoolEventIterator({self.__pool})"

    def __iter__(self):
        return self

    def __next__(self) -> "ParticlePool":
        return self.next()

    def next(self) -> "ParticlePool":
        self.__iteration_index += 1
        if self.__iteration_index == len(self.__pool[0]):
            raise StopIteration

        if len(self.__pool[0]) == 1:
            new_pool = self.__pool

        else:
            new_pool = []
            for old_particle in self.__pool:
                new_pool.append(old_particle[self.__iteration_index])

        return ParticlePool(new_pool)


class _PoolParticleIterator:

    def __init__(self, particle_list):
        self.__pool = particle_list
        self.__iteration_index = -1

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__pool)

    def __iter__(self):
        return self

    def __next__(self) -> Particle:
        return self.next()

    def next(self) -> Particle:
        self.__iteration_index += 1
        if self.__iteration_index == len(self.__pool):
            raise StopIteration

        return self.__pool[self.__iteration_index]


class ParticlePool:
    """
    Stores a collection of particles together.



    """

    def __init__(self, particle_list: List[Particle]):
        self.__particle_list = particle_list

    def __repr__(self) -> str:
        string = ""
        for index, particle in enumerate(self.__particle_list):
            if index == self.particle_count - 1:
                string += repr(particle)
            else:
                string += repr(particle) + ","
        return f"ParticlePool({string})"

    def __len__(self):
        return len(self.__particle_list)

    def __getitem__(self, item):
        if isinstance(item, np.ndarray) and item.dtype == bool:
            return self._mask(item)
        return self.__particle_list[item]

    def _mask(self, mask):
        if not len(mask) == len(self.__particle_list[0]):
            raise IndexError("Mask is the wrong length!")

        masked_data = list()
        for particle in self.iter_particles():
            masked_data.append(particle[mask])

        return ParticlePool(masked_data)

    def iter_particles(self):
        return _PoolParticleIterator(self.__particle_list)

    def iter_events(self):
        return _PoolEventIterator(self.__particle_list)

    def get_particles_by_id(self, particle_id: int) -> List[Particle]:
        p = [p for p in self.__particle_list if p.id == particle_id]
        return self._raise_if_empty(p)

    def get_particles_by_name(self, particle_name) -> List[Particle]:
        p = [p for p in self.__particle_list if p.name == particle_name]
        return self._raise_if_empty(p)

    @staticmethod
    def _raise_if_empty(value: List[Particle]) -> List[Particle]:
        if len(value) == 0:
            raise ValueError("No particles found!")
        else:
            return value

    def split(self, count):
        particles = [[] for i in range(count)]
        for particle in self.__particle_list:
            split_particles = particle.split(count)
            for index, particle_segment in enumerate(split_particles):
                particles[index].append(particle_segment)
        return [ParticlePool(pool) for pool in particles]

    def get_event_mass(self) -> np.ndarray:
        found_photon, found_proton = 0, 0
        vector_sum = FourVector(self.event_count)
        for event_particle in self.iter_particles():
            if not found_photon and event_particle.id == 1:
                found_photon = True
            elif not found_proton and event_particle.id == 14:
                found_proton = True
            else:
                vector_sum += event_particle
        return vector_sum.get_mass()

    def get_t(self) -> np.ndarray:
        proton = self.get_particles_by_name("Proton")[0]
        momenta = proton.x ** 2 + proton.y ** 2 + proton.z ** 2
        energy = (proton.e - _PROTON_GEV) ** 2
        return energy - momenta

    def get_s(self) -> np.ndarray:
        proton = self.get_particles_by_name("Proton")[0]
        momenta = proton.x ** 2 + proton.y ** 2 + proton.z ** 2
        energy = (proton.e + _PROTON_GEV) ** 2
        return energy - momenta

    def get_t_prime(self) -> np.ndarray:
        # Get initial values
        proton = self.get_particles_by_name("Proton")[0]
        s_value = self.get_s()
        sqrt_s = np.sqrt(s_value)
        mx2 = self.get_event_mass() ** 2

        # Calculate for Px and Ex
        ex = (s_value * mx2 * _PROTON_GEV ** 2) / 2 * sqrt_s
        px = np.sqrt((ex ** 2) - mx2)

        # Calculate t0
        t0_left = (mx2 / (2 * sqrt_s)) ** 2
        t0_right = (((proton.e * _PROTON_GEV) / sqrt_s) - px) ** 2
        t0 = t0_left - t0_right

        return self.get_t() - t0

    @property
    def event_count(self) -> int:
        return len(self.__particle_list[0])

    @property
    def particle_count(self) -> int:
        return len(self.__particle_list)

    @property
    def stored(self) -> List[Particle]:
        return self.__particle_list
