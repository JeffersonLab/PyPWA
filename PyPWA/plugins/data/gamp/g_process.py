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

from typing import List

import numpy

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.file import misc
from PyPWA.libs.file.processor import data_templates
from PyPWA.libs.math import vectors

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


def _get_particle_pool(
        filename: Path, precision: numpy.floating, particle_length: int = 1
) -> vectors.ParticlePool:
    with filename.open() as stream:
        count = int(stream.readline())
        lines = [stream.readline() for i in range(count)]

    events = []
    for line in lines:
        p_id, charge, x, y, z, e = line.strip("\n").split(" ")
        events.append(
            vectors.Particle(int(p_id), particle_length, precision=precision)
        )
    return vectors.ParticlePool(events)


class GampReader(data_templates.Reader):

    def __init__(self, filename: Path, precision: numpy.floating):
        self.__event_count = None
        self.__precision = precision  # Vectors don't support flexible types
        self.__file = filename
        self.__file_handle = filename.open()
        self.__particle_pool = _get_particle_pool(filename, precision)

    def __repr__(self) -> str:
        return f"GampReader({self.__file}, {self.__precision})"

    def next(self) -> vectors.ParticlePool:
        particle_line = self.__file_handle.readline().strip("\n")
        if particle_line == "":
            raise StopIteration
        self.__update_particle_pool()
        return self.__particle_pool

    def __update_particle_pool(self):
        for p in self.__particle_pool.iter_particles():
            line = self.__file_handle.readline()
            p_id, charge, x, y, z, e = line.strip("\n").split(" ")
            p.x, p.y, p.z, p.e = (x, y, z, e)

    def get_event_count(self) -> int:
        if not self.__event_count:
            with self.__file.open() as stream:
                particle_count = int(stream.readline())
                file_length = misc.get_file_length(self.__file)
                self.__event_count = int(file_length / (particle_count + 1))
        return self.__event_count

    def close(self):
        self.__file_handle.close()

    def reset(self):
        self.__file_handle.seek(0)

    @property
    def is_particle_pool(self) -> bool:
        return True

    @property
    def fields(self) -> List[str]:
        return [p.id for p in self.__particle_pool.iter_particles()]


class GampWriter(data_templates.Writer):

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__file_handle = filename.open("w")

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.__filename)

    def write(self, data: vectors.ParticlePool):
        self.__file_handle.write(u"{0}\n".format(data.particle_count))
        for p in data.iter_particles():
            self.__file_handle.write(
                u'{p.id} {p.charge} {p.x[0]} {p.y[0]} {p.z[0]} '
                u'{p.e[0]}\n'.format(p=p)
            )

    def close(self):
        self.__file_handle.close()


class GampMemory(data_templates.Memory):

    def __repr__(self) -> str:
        return "GampMemory()"

    def parse(
            self, filename: Path, precision: numpy.floating
    ) -> vectors.ParticlePool:
        with GampReader(filename, precision) as reader:
            empty_pool = _get_particle_pool(filename, precision, len(reader))
            for ei, e in enumerate(reader):
                for pi, p in enumerate(e.iterate_over_particles()):
                    # You must use get array to get a reference and not a copy
                    empty_pool.stored[pi].get_array()[ei] = p.get_array()
        return empty_pool

    def write(self, filename: Path, data: vectors.ParticlePool):
        with GampWriter(filename) as stream:
            for event in data.iter_events():
                stream.write(event)


class GampReadPackage(data_templates.ReadPackage):

    def __init__(self, filename: Path, precision: numpy.floating):
        self.__filename = filename
        self.__precision = precision
        self.__reader = GampReader(filename, precision)
        self.__parser = GampMemory()

    def __repr__(self) -> str:
        return f"GampReadPackage({self.__filename!r}, {self.__precision})"

    def get_reader(self) -> GampReader:
        return self.__reader

    def parse(self) -> vectors.particle:
        return self.__parser.parse(self.__filename, self.__precision)

    def get_bytes(self) -> int:
        with self.__filename.open() as stream:
            num_particles = int(stream.readline().strip("\n"))
            num_events = self.__reader.get_event_count()
            num_bytes = self.__precision().nbytes
        return num_particles * 4 * num_events * num_bytes

    def get_event_count(self) -> int:
        return self.__reader.get_event_count()
