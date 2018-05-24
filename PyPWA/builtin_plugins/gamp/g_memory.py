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
Gamp data reading and writing.

This file holds the Gamp Reader and Gamp Writer. These simply load the
data into memory one event at a time and write to file one event at a
time. Only the previous loaded events are stored, anything later than that
will not be saved in memory by these object.

- GampMemory: Loads GAMP Data into memory to bypass the disk bottleneck with
    calculations. DO NOT USE THIS FOR LARGE GAMP FILES! THIS OBJECT WILL
    QUICKLY OVERFILL THE MEMORY OF YOUR PC, EVEN WITH THE NUMPY OPTIMIZATIONS!
"""

import numpy
from typing import Dict, Any

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.builtin_plugins.gamp import g_iterator
from PyPWA.libs.components.data_processor import data_templates
from PyPWA.libs.math import particle

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION



class _GampIndex(object):

    def __init__(self):
        self.__event_index = None  # type: int
        self.__particle_index = None  # type: int
        self.__variable_particle_count = None  # type: bool

    def get_gamp_info(self, path):
        # type: (Path) -> None
        self.__reset_object_values()
        with path.open() as stream:
            for line in stream:
                sanitized_line = line.strip("\n").strip()
                if len(sanitized_line) == 1:
                    self.__process_line(sanitized_line)

    def __reset_object_values(self):
        self.__event_index = 0
        self.__particle_index = 0
        self.__variable_particle_count = False

    def __process_line(self, line):
        # type: (str) -> None
        self.__event_index += 1
        if int(self.__particle_index) == 0:
            self.__particle_index = int(line)
        elif self.__particle_index < int(line):
            self.__particle_index = int(line)
            self.__variable_particle_count = True

    @property
    def event_count(self):
        # type: () -> int
        return self.__event_index

    @property
    def particle_count(self):
        # type: () -> int
        return self.__particle_index

    @property
    def is_variable(self):
        # type: () -> bool
        return self.__variable_particle_count


class _GampParse(object):

    def __init__(self):
        self.__indexer = _GampIndex()
        self.__temp_pool = None  # type: Dict[int, Dict[str, Any]]

    def parse(self, file_location):
        # type: (Path) -> particle.ParticlePool
        self.__indexer.get_gamp_info(file_location)
        self.__crash_if_not_possible()
        self.__make_particle_dictionary()
        self.__read_gamp_file(file_location)
        return self.__make_particle_pool()

    def __crash_if_not_possible(self):
        if self.__indexer.is_variable:
            raise RuntimeError(
                "GAMP Parser doesn't support changes in particle count yet!"
            )

    def __make_particle_dictionary(self):
        temp_pool = dict()
        for index in range(self.__indexer.event_count):
            temp_pool[index] = {
                "id": None, "charge": None,
                "vector": numpy.zeros(
                    self.__indexer.event_count, particle.NUMPY_PARTICLE_DTYPE
                )
            }
        self.__temp_pool = temp_pool

    def __read_gamp_file(self, file_location):
        # type: (Path) -> None
        first_run = True
        with g_iterator.GampReader(file_location) as stream:
            for index, chunk in enumerate(stream):
                if first_run:
                    self.__setup_initial_data(chunk)
                self.__initialize_data(index, chunk)

    def __setup_initial_data(self, chunk):
        # type: (particle.ParticlePool) -> None
        for index in range(self.__indexer.particle_count):
            self.__temp_pool[index]['id'] = chunk[index].id
            self.__temp_pool[index]['charge'] = chunk[index].charge

    def __initialize_data(self, index, chunk):
        # type: (int, particle.ParticlePool) -> None
        for chunk_index in range(len(chunk)):
            self.__temp_pool[chunk_index]['vector'][index] = (
                chunk[chunk_index].get_array()
            )

    def __make_particle_pool(self):
        # type: () -> particle.ParticlePool
        new_pool = []
        for index in range(self.__indexer.particle_count):
            new_pool.append(
                particle.Particle(
                    self.__temp_pool[index]['id'],
                    self.__temp_pool[index]['charge'],
                    self.__temp_pool[index]['vector']
                )
            )

        return particle.ParticlePool(new_pool)


class _GampDump(object):

    def write(self, path, pool):
        # type: (Path, particle.ParticlePool) -> None
        with g_iterator.GampWriter(path) as stream:
            for event in pool:
                stream.write(event)


class GampMemory(data_templates.Memory):

    def __init__(self):
        self.__parser = _GampParse()
        self.__dumper = _GampDump()

    def parse(self, file_location):
        # type: (Path) -> particle.ParticlePool
        return self.__parser.parse(file_location)

    def write(self, file_location, data):
        # type: (Path, particle.ParticlePool) -> None
        self.__dumper.write(file_location, data)
