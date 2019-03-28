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

import numpy
from PyPWA import AUTHOR, VERSION
from PyPWA.libs.math.vectors import basic_vectors

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


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


class _ParticleIterator:

    def __init__(self, particle_id: int, array: numpy.ndarray, array_type):
        self.__id = particle_id
        self.__array = array
        self.__type = array_type
        self.__index = -1

    def __repr__(self):
        return (
            f"_ParticleIterator({self.__id}, {self.__array}, {self.__type})"
        )

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        try:
            self.__index += 1
            array = numpy.array(self.__array[self.__index], self.__type)
            return Particle(self.__id, array)
        except IndexError:
            raise StopIteration


class Particle(basic_vectors.FourVector):

    __slots__ = ['__particle_id', '__charge', '__particle_name']

    def __init__(
            self,
            particle_id: int,
            x: Union[int, numpy.ndarray, float, str],
            y: Opt[Union[str, float]] = None,
            z: Opt[Union[str, float]] = None,
            e: Opt[Union[str, float]] = None,
            precision: numpy.floating = numpy.float64
    ):
        super(Particle, self).__init__(x, y, z, e, precision)
        self.__particle_id = particle_id
        self.__particle_name, self.__charge = get_particle_by_id(particle_id)

    def __eq__(self, other: "Particle") -> bool:
        arrays_equal = (other.get_array() == self._vector).all()
        id_equals = self.id == other.id
        return True if arrays_equal and id_equals else False

    def __repr__(self) -> str:
        return f"Particle({self.__particle_id}, {self._vector!r})"

    def __str__(self) -> str:
        if len(self) == 1:
            return (
                f"Particle("
                f"name={self.__particle_name}, id={self.__particle_id},"
                f" x={self.x[0]}, y={self.y[0]},"
                f" z={self.z[0]}, e={self.e[0]})"
            )
        else:
            return (
                f"Particle("
                f"name={self.__particle_name}, id={self.__particle_id},"
                f" x, y, z, e for length={len(self)})"
            )

    def __getitem__(self, item: int) -> "Particle":
        array = numpy.array([self._vector[item]], self._array_type)
        return Particle(self.__particle_id, array)

    def split(self, count: int) -> List["Particle"]:
        new_vectors = super(Particle, self).split(count)
        new_particles = []
        for vector in new_vectors:
            new_particles.append(Particle(self.id, vector))
        return new_particles

    @property
    def id(self) -> int:
        return self.__particle_id

    @property
    def name(self) -> str:
        return self.__particle_name

    @property
    def charge(self) -> int:
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

    @property
    def event_count(self) -> int:
        return len(self.__particle_list[0])

    @property
    def particle_count(self) -> int:
        return len(self.__particle_list)

    @property
    def stored(self) -> List[Particle]:
        return self.__particle_list
