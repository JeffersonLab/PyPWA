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
GAMP data reading and writing.

This file holds the GAMP Reader and GAMP Writer. These simply load the
data into memory one event at a time and write to file one event at a
time. Only the previous loaded events are stored, anything later than that
will not be saved in memory by these object.

- GampReader: This reads in GAMP events from disk, GAMP events are deque
  of named tuples, each named tuple representing a particle in the event.
- GampWriter: Takes GAMP events one at a time and attempts to write them
  in a standardized way to file so that other programs can read the output.
"""

import io

import numpy

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs import misc_file_libs
from PyPWA.libs.components.data_processor import data_templates
from PyPWA.libs.math import particle


__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _GampParticleCount(object):

    def __init__(self):
        self.__particle_count = 0

    def get_particle_count(self, file_location):
        # type: (Path) -> None
        particle_count = self.__get_particle_count(file_location)
        file_length = misc_file_libs.get_file_length(file_location)
        self.__particle_count = int(file_length / particle_count)

    @staticmethod
    def __get_particle_count(file_location):
        with file_location.open() as stream:
            return int(stream.readline())

    @property
    def particle_count(self):
        return self.__particle_count


class GampReader(data_templates.Reader):

    def __init__(self, file_location):
        # type: (Path) -> None
        self.__event_count = None
        self._file = None  # type: io.BufferedReader
        self._the_file = file_location
        self.__particle_count = _GampParticleCount()
        self.__particle_count.get_particle_count(file_location)
        self._start_input()

    def _start_input(self):
        try:
            if self._file:
                self._file.close()
        except AttributeError:
            pass
        self._file = self._the_file.open("rt")

    def reset(self):
        self._start_input()

    def next(self):
        first_line = self._file.readline().strip("\n")
        if first_line == "":
            raise StopIteration

        particle_count = int(first_line)
        event = []
        for index in range(particle_count):
            event.append(self._make_particle(self._file.readline()))

        return particle.ParticlePool(event)

    @staticmethod
    def _make_particle(string):
        # type: (str) -> particle.Particle

        data_list = string.strip("\n").split(" ")

        vector = numpy.zeros(1, particle.NUMPY_PARTICLE_DTYPE)
        particle_id = numpy.float64(data_list[0])  # Particle ID
        charge = numpy.float64(data_list[1])  # Particle Charge
        vector['x'] = numpy.float64(data_list[2])  # Particle X Momentum
        vector['y'] = numpy.float64(data_list[3])  # Particle Y Momentum
        vector['z'] = numpy.float64(data_list[4])  # Particle Z Momentum
        vector['e'] = numpy.float64(data_list[5])  # Particle Energy

        return particle.Particle(particle_id, charge, vector)

    def get_event_count(self):
        return self.__particle_count.particle_count

    def close(self):
        self._file.close()

    @property
    def is_particle_pool(self):
        return True


class GampWriter(data_templates.Writer):

    def __init__(self, file_location):
        # type: (Path) -> None
        self.__file = file_location.open("w")

    def write(self, particle_pool):
        # type: (particle.ParticlePool) -> None
        self.__file.write(u"%d\n" % particle_pool.particle_count)
        for the_particle in particle_pool.iterate_over_particles():
            self.__write_particle(the_particle)

    def __write_particle(self, the_particle):
        # type: (particle.Particle) -> None
        if len(the_particle) > 1:
            raise ValueError("Can't write more than one event at a time!")
        self.__file.write(
            u'%s %s %s %s %s %s\n' % (
                the_particle.id.astype(str), the_particle.charge.astype(str),
                the_particle.x[0].astype(str), the_particle.y[0].astype(str),
                the_particle.z[0].astype(str), the_particle.e[0].astype(str)
            )
        )

    def close(self):
        self.__file.close()

    @property
    def is_particle_pool(self):
        return True
