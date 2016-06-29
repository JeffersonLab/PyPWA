#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Gamp data reading and writing.

This file holds the Gamp Reader and Gamp Writer. These simply load the
data into memory one event at a time and write to file one event at a
time. Only the previous loaded events are stored, anything later than that
will not be saved in memory by these object.
"""

import collections
import io

import numpy

from PyPWA.libs.data import definitions
from PyPWA.configuratr import data_types
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class GampReader(definitions.TemplateReader):

    def __init__(self, file_location):
        """
        This reads in Gamp events from disk, Gamp events are deque of
        named tuples, each named tuple representing a particle in the
        event.

        Args:
            file_location (str): Name of the GAMP file, can be any size.
        """
        super(GampReader, self).__init__(file_location)
        self._previous_event = None  # type: collections.namedtuple
        self._particle_master = data_types.GampParticle()

        self._start_input()

    def _start_input(self):
        """
        Checks to see if the file is opened, and if it is close it so that
        it may be reopened.
        """
        try:
            if self._file:
                self._file.close()
        except AttributeError:
            pass
        self._file = io.open(self._the_file, "rt")

    def reset(self):
        """
        Calls the _start_input method again which will close the file then
        reopen it back at the beginning of the file.
        """
        self._start_input()

    @property
    def next_event(self):
        """
        Structures the read in event from the GAMP file into a deque then
        passes it to the calling function.

        Returns:
            deque: The next deque event.

        Raises:
            StopIterator: End of file has been found.
        """
        count = int(self._file.readline().strip("\n"))
        event = data_types.GampEvent(count)
        for index in range(count):
            event.append(self._make_particle(self._file.readline()))
        if event == "":
            raise StopIteration
        self._previous_event = event
        return self._previous_event

    @property
    def previous_event(self):
        return self._previous_event

    def _make_particle(self, string):
        """
        Takes the string read in from the GAMP event and parses it into a
        named tuple to store the various values. All values are numpy data
        types.

        Args:
            string (str): The string containing the GAMP Particle

        Returns:
            GampParticle(namedtuple): The particle stored in a namedtuple.
        """
        the_list = string.strip("\n").split(" ")

        particle = self._particle_master.make_particle(
            # Particle ID, Particle Charge
            numpy.uint8(the_list[0]), numpy.int8(the_list[1]),
            # Particle X Momentum, Particle Y Momentum
            numpy.float64(the_list[2]), numpy.float64(the_list[3]),
            # Particle Z Momentum, Particle Energy
            numpy.float64(the_list[4]), numpy.float64(the_list[5])
        )

        return particle


class GampWriter(definitions.TemplateWriter):

    def __init__(self, file_location):
        """
        Takes GAMP events one at a time and attempts to write them in a
        standardized way to file so that other programs can read the
        output.

        Args:
            file_location (str): Where to write the GAMP data.
        """
        super(GampWriter, self).__init__(file_location)
        self._file = io.open(file_location, "w")

    def write(self, data):
        """
        Writes the events the disk one event at a time, wont close the
        disk access until the close function is called or until the object
        is deleted.

        Args:
            data (deque): the file that is to be written to disk.
        """
        self._file.write(str(len(data))+"\n")

        for particle in data:
            self._file.write(
                str(particle.id) + " " + str(particle.charge) + " " +
                str(particle.x) + " " + str(particle.y) + " " +
                str(particle.z) + " " + str(particle.energy) + "\n"
            )

    def close(self):
        self._file.close()


class GampMemory(definitions.TemplateMemory):
    """
    Loads GAMP Data into memory to bypass the disk bottleneck with
    calculations.
    DO NOT USE THIS FOR LARGE GAMP FILES! THIS OBJECT WILL QUICKLY
    OVERFILL THE MEMORY OF YOUR PC, EVEN WITH THE NUMPY AND COLLECTIONS
    OPTIMIZATIONS!
    """

    def parse(self, file_location):
        """
        Parses Gamp Files into a single list.

        Args:
            file_location (str): The location of the GAMP File.

        Returns:
            list[GampEvent]: A list containing all the GampEvents from the
                data file.
        """
        reader = GampReader(file_location)
        events = []
        for event in reader:
            events.append(event)
        return events

    def write(self, file_location, data):
        """
        Writes the GAMP events from memory to disk, this method can be
        used for single GAMP events but its recommended that you use
        GampWriter for single GAMP event writing or something similar.

        Args:
            file_location (str): The location where to write the GAMP
                file.
            data (list): The list containing all the GampEvents that are
                to be written to disk.
        """
        writer = GampWriter(file_location)
        for event in data:
            writer.write(event)


class GampValidator(definitions.TemplateValidator):

    def __init__(self, file_location, full=False):
        """
        Validates the GAMP file to ensure that the file can be read by
        gamp before actually trying to read it. Also is used for the data
        plugin to determine which of its plugins to use when its handed a
        file of an unknown nature.

        Args:
            file_location (str): The location of the file that needs to
                be read.
            full (Optional[bool]): Whether to do a full test of the file
                or not, useful for debugging unknown issues or
                complications with reading in GAMP files.
        """
        super(GampValidator, self).__init__(file_location, full)
        self._file = io.open(file_location, "rt")

    def _check_events(self):
        """
        Checks the events to ensure that the number of particles match the
        number declared by the event.

        Raises:
            PyPWA.libs.data.exceptions.IncompatibleData:
                Raised when the tests fail for this object and the data.
        """
        count = 0
        while True:
            if count == 3 and not self._full:
                break
            elif count == 20 and self._full:
                break
            number = self._file.readline()
            try:
                int(number)
            except ValueError:
                raise definitions.IncompatibleData(
                    "Expected particle count."
                )

            try:
                for index in range(int(number)):
                    if len(self._file.readline().split(",")) != 6:
                        raise definitions.IncompatibleData(
                            "Particle count does not match the number of "
                            "events read in by the Validator."
                        )

            except Exception as Error:
                raise definitions.IncompatibleData(
                    "Unexpected exception raised, caught " + str(Error) +
                    "where it wasn't expected."
                )

    def _test_length(self):
        """
        Tests to make sure that the first number matches the number of
        events. I know that this can be made to be better, however it
        alludes me at this moment.

        Raises:
            PyPWA.libs.data.exceptions.IncompatibleData:
                Raised when the tests fail for this object and the data.
        """
        while True:
            number = self._file.readline()
            try:
                for index in range(int(number)):
                    if self._file.readline() == "":
                        break
            except Exception as Error:
                raise definitions.IncompatibleData(
                    "Unexpected exception raised, caught " + str(Error) +
                    "where it wasn't expected."
                )

    def test(self):
        self._test_length()
        self._check_events()


metadata_data = {
    "name": "gamp",
    "extension": "gamp",
    "validator": GampValidator,
    "reader": GampReader,
    "writer": GampWriter,
    "memory": GampMemory
}
