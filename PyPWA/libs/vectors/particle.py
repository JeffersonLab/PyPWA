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
import pandas as pd
from PyPWA.libs.vectors import FourVector
from PyPWA import info as _info

try:
    from IPython.display import display
except ImportError:
    display = print


__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


_PROTON_GEV = .9382720813


def get_particle_by_id(particle_id: int) -> str:
    """
    ... seealso::
        https://www.star.bnl.gov/public/comp/simu/gstar/Manual/particle_id.html

    :return: Tuple containing particle's name, particle's charge
    """
    try:
        return {
            1:  'Gamma',        2: 'Positron',
            3:  'Electron',     4:  'Neutrino',
            5:  'Muon +',       6:  'Muon -',
            7:  'Pion 0',       8:  'Pion +',
            9:  'Pion -',       10: 'Kaon 0 Long',
            11: 'Kaon +',       12: 'Kaon -',
            13: 'Neutron',      14: 'Proton',
            15: 'Antiproton',   16: 'Kaon 0 Short',
            17: 'Eta',          18: 'Lambda',
            19: 'Sigma +',      20: 'Sigma 0',
            21: 'Sigma -',      22: 'Xi 0',
            23: 'Xi -',         24: 'Omega -',
            25: 'Antineutron',  26: 'Antilambda',
            27: 'Antisigma -',  28: 'Antisigma 0',
            29: 'Antisigma +',  30: 'Antixi 0',
            31: 'Antixi +',     32: 'Antiomega +',
            45: 'Deuteron',     46: 'Triton',
            47: 'Alpha',        48: 'Geantino',
            49: 'He3',          50: 'Cerenkov',
        }[particle_id]
    except KeyError:
        return "Unknown"


class Particle(FourVector):
    """Numpy backed Particle object for vector operations inside
    PyPWA.

    By default, Particle is represented through the particles
    angles and mass. However, internally the particle is stored
    as four momenta just as it's stored in the GAMP format.

    Parameters
    ----------
    particle_id : int
        The Particle ID, used to determine the particle's name and charge.
    charge : int
        The particle's Charge as read from the GAMP file.
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

    __slots__ = [
        "_e", "_x", "_y", "_z", "__particle_id", "__particle_name", "__charge"
    ]

    def __init__(
            self,
            particle_id: int,
            charge: int,
            e: Union[int, np.ndarray, float, pd.DataFrame],
            x: Opt[Union[float, pd.Series, np.ndarray]] = None,
            y: Opt[Union[float, pd.Series, np.ndarray]] = None,
            z: Opt[Union[float, pd.Series, np.ndarray]] = None
    ):
        super(Particle, self).__init__(e, x, y, z)
        self.__particle_id = particle_id
        self.__charge = charge
        self.__particle_name = get_particle_by_id(particle_id)

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

    def _repr_html_(self):
        df = pd.DataFrame()
        df['Θ'], df['ϕ'] = self.get_theta(), self.get_phi()
        df['Mass'] = self.get_mass()
        return (
            f'<h2>{self.__particle_id}: {self.__particle_name}</h2>'
            f'{df._repr_html_()}'
        )

    def display_raw(self):
        """
        Displays the contents of the Particle as Four Momenta
        """
        df = pd.DataFrame()
        df['e'], df['x'], df['y'], df['z'] = self.e, self.x, self.y, self.z

        name = f"{self.__particle_id}: {self.__particle_name}"
        display(name)
        display(df)

    def __getitem__(
            self, item: Union[int, str, slice]
    ) -> Union["Particle", pd.Series]:
        if isinstance(item, (int, slice)) or \
                isinstance(item, np.ndarray) and item.dtype in (bool, int):
            return Particle(
                self.__particle_id, self.__charge,
                self._e[item], self._x[item], self._y[item], self._z[item]
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
            particles.append(
                Particle(self.__particle_id, self.__charge, e, x, y, z)
            )
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
    Stores a collection of particles together as a list.

    By default the particles are represented as their angles and mass,
    however internally the particles are still stored as the Four Momenta.
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

    def _repr_pretty_(self, p, cycle):
        if cycle:
            return 'ParticlePool( ?.)'
        else:
            for particle in self.__particle_list:
                particle._repr_pretty_(p, cycle)
                p.text('\n')

    def _repr_html_(self):
        html = ""
        for p in self.__particle_list:
            html += p._repr_html_()
        return html

    def display_raw(self):
        """
        Display's the file
        """
        for p in self.__particle_list:
            print('\n')
            p.display_raw()

    def __len__(self):
        return len(self.__particle_list)

    def __getitem__(self, item):
        if isinstance(item, np.ndarray) and item.dtype == bool:
            return self._mask(item)
        return self.__particle_list[item]

    def __eq__(self, other):
        if not isinstance(other, ParticlePool):
            return False
        if other.event_count != self.event_count:
            return False
        if other.particle_count != self.particle_count:
            return False

        particle_pair = zip(self.iter_particles(), other.iter_particles())
        for current_particle, other_particle in particle_pair:
            if current_particle != other_particle:
                return False

        return True

    def _mask(self, mask):
        print("PP Masking")
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
        """
        Split's the particles in N groups.

        This is required to be a method on any object that needs to be
        passed to the processing module.

        Parameters
        ----------
        count : int
            How many ParticlePools to return

        Returns
        -------
        List[ParticlePool]
            A list of particle pools that can be passed to different
            process groups.
        """
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
