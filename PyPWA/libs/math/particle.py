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

from typing import List, Union

import numpy
from PyPWA import AUTHOR, VERSION
from PyPWA.libs.math import vectors

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


NUMPY_PARTICLE_DTYPE = [('x', 'f8'), ('y', 'f8'), ('z', 'f8'), ('e', 'f8')]


class GeantParticleID(object):

    _IDS = {
        1:  'Gamma',        2:  'Positron',     3:  'Electron',
        4:  'Neutrino',     5:  'Muon +',       6:  'Muon -',
        7:  'Pion 0',       8:  'Pion +',       9:  'Pion -',
        10: 'Kaon 0 Long',  11: 'Kaon +',       12: 'Kaon -',
        13: 'Neutron',      14: 'Proton',       15: 'Antiproton',
        16: 'Kaon 0 Short', 17: 'Eta',          18: 'Lambda',
        19: 'Sigma +',      20: 'Sigma 0',      21: 'Sigma -',
        22: 'Xi 0',         23: 'Xi -',         24: 'Omega -',
        25: 'Antineutron',  26: 'Antilambda',   27: 'Antisigma -',
        28: 'Antisigma 0',  29: 'Antisigma +',  30: 'Antixi 0',
        31: 'Antixi +',     32: 'Antiomega +',  45: 'Deuteron',
        46: 'Triton',       47: 'Alpha',        48: 'Geantino',
        49: 'He3',          50: 'Cerenkov'
    }

    @classmethod
    def get_particle_by_id(cls, particle_id):
        return cls._IDS[particle_id]


class Particle(vectors.FourVector):

    def __init__(self, particle_id, charge, array):
        super(Particle, self).__init__(array)
        self.__particle_id = particle_id
        self.__charge = charge
        self.__particle_name = (
            GeantParticleID.get_particle_by_id(particle_id)
        )

    def __getitem__(self, item):
        # type: (Union[int, str]) -> Union[Particle, numpy.ndarray]
        if isinstance(item, str):
            return super(Particle, self).__getitem__(item)
        elif isinstance(item, int):
            event = self._vector[item]
            new_vector = numpy.zeros(1, NUMPY_PARTICLE_DTYPE)
            new_vector[0] = event

            return (
                Particle(self.id, self.charge, new_vector)
            )
        else:
            raise ValueError("Unknown type: %s!" % type(item))

    def __eq__(self, other):
        # type: (Particle) -> bool
        arrays_equal = (other.get_array() == self._vector).all()
        id_equals = self.id == other.id
        return True if arrays_equal and id_equals else False

    def __repr__(self):
        return "{0}({1}, {2}, {3!r}".format(
            self.__class__.__name__, self.__particle_id,
            self.__charge, self._vector
        )

    def __str__(self):
        if len(self) == 1:
            return "{0}(name={1}, id={2}, x={3}, y={4}, z={5}, e={6}".format(
                self.__class__.__name__, self.__particle_name,
                self.__particle_id, self.x[0], self.y[0], self.z[0], self.e[0]
            )
        else:
            return "{0}(name={1}, id={2}, x, y, z, e for length={3}".format(
                self.__class__.__name__, self.__particle_name,
                self.__particle_id, len(self)
            )

    def split(self, count):
        new_vectors = super(Particle, self).split(count)
        new_particles = []
        for vector in new_vectors:
            new_particles.append(Particle(self.id, self.e, vector))
        return new_particles

    @property
    def id(self):
        return self.__particle_id

    @property
    def name(self):
        return self.__particle_name

    @property
    def charge(self):
        return self.__charge


class _PoolEventIterator(object):

    def __init__(self, particle_list):
        self.__pool = particle_list
        self.__iteration_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # type: () -> ParticlePool
        return self.next()

    def next(self):
        # type: () -> ParticlePool
        self.__iteration_index += 1
        if self.__iteration_index > len(self.__pool[0]):
            raise StopIteration

        new_pool = []
        for old_particle in self.__pool:
            new_pool.append(old_particle[self.__iteration_index - 1])

        return ParticlePool(new_pool)


class _PoolParticleIterator(object):

    def __init__(self, particle_list):
        self.__pool = particle_list
        self.__iteration_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # type: () -> Particle
        return self.next()

    def next(self):
        # type: () -> Particle
        self.__iteration_index += 1
        if self.__iteration_index > len(self.__pool):
            raise StopIteration

        return self.__pool[self.__iteration_index - 1]


class ParticlePool(object):

    def __init__(self, particle_list):
        # type: (List[Particle]) -> None
        self.__particle_list = particle_list

    def __repr__(self):
        string = ""
        for index, particle in enumerate(self.__particle_list):
            if index == len(self) - 1:
                string += repr(particle)
            else:
                string += repr(particle) + ",\n"
        return "ParticlePool(%s)" % string

    def __iter__(self):
        return _PoolEventIterator(self.__particle_list)

    def __len__(self):
        return len(self.__particle_list)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__particle_list[item]
        elif isinstance(item, str):
            try:
                return self.get_particles_by_id(int(item))
            except ValueError:
                return self.get_particles_by_name(item)
        else:
            raise ValueError("Can't fetch values using %s!" % type(item))

    def iterate_over_particles(self):
        return _PoolParticleIterator(self.__particle_list)

    def iterate_over_events(self):
        return _PoolEventIterator(self.__particle_list)

    def get_particles_by_id(self, particle_id):
        particles = []
        for particle in self.__particle_list:
            if particle.id == particle_id:
                particles.append(particle)
        return self._raise_if_empty(particles)

    def get_particles_by_name(self, particle_name):
        particles = []
        for particle in self.__particle_list:
            if particle.name == particle_name:
                particles.append(particle)
        return particles

    @staticmethod
    def _raise_if_empty(value):
        # type: (List[Particle]) -> List[Particle]
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
    def event_count(self):
        # type: () -> int
        return len(self.__particle_list[0])

    @property
    def particle_count(self):
        # type: () -> int
        return len(self)
