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

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.file import misc
from PyPWA.libs.file.processor import templates, DataType
from PyPWA.libs.math import vectors

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


_COUNT = 3  # number of events to check


class _GampDataPlugin(templates.IDataPlugin):

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @property
    def plugin_name(self):
        return "gamp"

    def get_memory_parser(self):
        return _GampMemory()

    def get_writer(self, file_location):
        return _GampWriter(file_location)

    def get_reader(self, file_location):
        return _GampReader(file_location)

    def get_read_test(self):
        return _GampDataTest()

    @property
    def supported_extensions(self):
        return [".gamp"]

    @property
    def supported_data_types(self):
        return [DataType.TREE_VECTOR]


metadata = _GampDataPlugin()


class _GampDataTest(templates.IReadTest):

    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

    def can_read(self, filename):
        # type: (Path) -> bool
        with filename.open() as stream:
            for i in range(_COUNT):
                line = stream.readline().strip("\n")
                if line == "":
                    if i == 0:
                        return False
                    return True

                try:
                    particle_count = int(line)
                except Exception:
                    return False

                for l in range(particle_count):
                    if len(stream.readline().split(" ")) != 6:
                        return False
        return True


def _get_particle_pool(
        filename: Path, particle_length: int = 1) -> vectors.ParticlePool:
    with filename.open() as stream:
        count = int(stream.readline())
        lines = [stream.readline() for i in range(count)]

    events = []
    for line in lines:
        p_id, charge, x, y, z, e = line.strip("\n").split(" ")
        events.append(vectors.Particle(int(p_id), particle_length))
    return vectors.ParticlePool(events)


class _GampReader(templates.ReaderBase):

    def __init__(self, filename: Path):
        self.__event_count = None
        self.__file = filename
        self.__file_handle = filename.open()
        self.__particle_pool = _get_particle_pool(filename)

    def __repr__(self) -> str:
        return f"GampReader({self.__file})"

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


class _GampWriter(templates.WriterBase):

    def __init__(self, filename: Path):
        self.__filename = filename
        self.__file_handle = filename.open("w")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__filename})"

    def write(self, data: vectors.ParticlePool):
        # I like f-strings, but this is the fastest way to make a string
        self.__file_handle.write("%i\n" % data.particle_count)
        for p in data.iter_particles():
            self.__file_handle.write(
                "%d %d %.20f %.20f %.20f %.20f\n" % (
                    p.id, p.charge, p.x[0], p.y[0], p.z[0], p.e[0]
                )
            )

    def close(self):
        self.__file_handle.close()


class _GampMemory(templates.IMemory):

    def __repr__(self) -> str:
        return "GampMemory()"

    def parse(self, filename: Path) -> vectors.ParticlePool:
        with _GampReader(filename) as reader:
            empty_pool = _get_particle_pool(filename, len(reader))
            for ei, e in enumerate(reader):
                for pi, p in enumerate(e.iter_particles()):
                    # You must use get array to get a reference and not a copy
                    empty_pool.stored[pi].get_array()[ei] = p.get_array()
        return empty_pool

    def write(self, filename: Path, data: vectors.ParticlePool):
        with _GampWriter(filename) as stream:
            for event in data.iter_events():
                stream.write(event)
