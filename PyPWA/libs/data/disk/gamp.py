# The MIT License (MIT)
#
# Copyright (c) 2014-2016 JLab.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Gamp data reading and writing.

This file holds the Gamp Reader and Gamp Writer. These simply load the data into
memory one event at a time and write to file one event at a time. Only the
previous loaded events are stored, anything later than that will not be saved
in memory by these object.
"""

import collections
import io

import numpy

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class GampReader(object):

    _particles = {
        1: "Gamma",
        2: "Positron",
        3: "Electron",
        4: "Neutrino",
        5: "Muon +",
        6: "Muon -",
        7: "Pion 0",
        8: "Pion +",
        9: "Pion -",
        10: "Kaon 0 Long",
        11: "Kaon +",
        12: "Kaon -",
        13: "Neutron",
        14: "Proton",
        15: "Antiproton",
        16: "Kaon 0 Short",
        17: "Eta",
        18: "Lambda",
        19: "Sigma +",
        20: "Sigma 0",
        21: "Sigma -",
        22: "Xi 0",
        23: "Xi -",
        24: "Omega",
        25: "Antineutron",
        26: "Antilambda",
        27: "Antisigma -",
        28: "Antisigma 0",
        29: "Antisigma +",
        30: "Antixi 0",
        31: "Antixi +"
    }

    def __init__(self, gamp_file):
        """
        This reads in Gamp events from disk, Gamp events are deque of named
        tuples, each named tuple representing a particle in the event.

        Args:
            gamp_file: (str) Name of the GAMP file, can be any size.
        """

        super(GampReader, self).__init__()
        self._the_file = gamp_file
        self._file = False
        self._previous_event = None
        self._particle_master = collections.namedtuple("GampParticle",
                                                       ["name", "id", "charge",
                                                        "x", "y", "z", "energy"]
                                                       )

        self._start_input()

    def _start_input(self):
        """
        Checks to see if the file is opened, and if it is close it so that it
        may be reopened.
        """
        if self._file:
            self._file.close()
        self._file = io.open(self._the_file, "rt")

    def reset(self):
        """
        Calls the _start_input method again which will close the file then
        reopen it back at the beginning of the file.
        """
        self._start_input()

    def __next__(self):
        return self.next_event

    @property
    def next_event(self):
        """
        Structures the read in event from the GAMP file into a deque then passes
        it to the calling function.

        Returns:
            deque: The next deque event.

        Raises:
            StopIterator: End of file has been found.
        """
        count = int(self._file.readline().strip("\n"))
        event = collections.deque(maxlen=count)
        for index in range(count):
            event.append(self._make_particle(self._file.readline()))
        self._previous_event = event
        return self._previous_event

    @property
    def previous_event(self):
        return self._previous_event

    def _make_particle(self, string):
        """
        Takes the string read in from the GAMP event and parses it into a named
        tuple to store the various values. All values are numpy data types.

        Args:
            string: The string containing the GAMP Particle

        Returns:
            GampParticle(namedtuple): The particle stored in a namedtuple.
        """
        the_list = string.strip("\n").split(" ")
        particle = self._particle_master(
            self._particles[int(the_list[0])], numpy.uint8(the_list[0]),
            numpy.int8(the_list[1]), numpy.float64(the_list[2]),
            numpy.float64(the_list[3]), numpy.float64(the_list[4]),
            numpy.float64(the_list[5])
        )

        return particle

    def __del__(self):
        self._file.close()


class GampWriter(object):

    def __init__(self, gamp_file):
        """
        Takes GAMP events one at a time and attempts to write them in a
        standardized way to file so that other programs can read the output.

        Args:
            gamp_file: (str) Where to write the GAMP data.
        """
        self._file = io.open(gamp_file, "w")

    def __del__(self):
        self._file.close()

    def write_event(self, event):
        """
        Writes the events the disk one event at a time, wont close the disk
        access until the close function is called or until the object is
        deleted.

        Args:
            event: (deque) the file that is to be written to disk.
        """
        self._file.write(str(len(event))+"\n")

        for particle in event:
            self._file.write(str(particle.id) + " " + str(particle.charge) + " " + str(particle.x) + " " +
                             str(particle.y) + " " + str(particle.z) + " " + str(particle.energy) + "\n")

    def close(self):
        self._file.close()


class GampEvent(collections.deque):

    def __init__(self, particle_count):
        """
        Extends a deque list, adds functions that attempt to help use and test
        the GampEvents.

        Args:
            particle_count: (int) The number of particles in the event.
        """
        super(GampEvent, self).__init__(maxlen=particle_count)

    def search(self, query):
        """
        Searches for a specific particle based off of the particles name. Not an
        efficient function or reliable, probably shouldn't be used yet.

        Args:
            query: (str) The name of the specified particle.

        Returns:
            GampParticle(namedtuple): The requested particle.
        """
        for particle in self:
            if particle.name == query:
                return particle
