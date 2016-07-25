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

"""
Gamp data reading and writing.

This file holds the Gamp Reader and Gamp Writer. These simply load the
data into memory one event at a time and write to file one event at a
time. Only the previous loaded events are stored, anything later than that
will not be saved in memory by these object.
"""

import io

import numpy

from PyPWA.libs.data import definitions
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
        self._previous_event = None  # type: numpy.ndarray

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
        first_line = self._file.readline().strip("\n")
        if first_line == "":
            raise StopIteration
        count = int(first_line)
        event = numpy.zeros((count, 6), numpy.float64)
        for index in range(count):
            event[index] = self._make_particle(self._file.readline())
        self._previous_event = event
        return self._previous_event

    @property
    def previous_event(self):
        return self._previous_event

    @staticmethod
    def _make_particle(string):
        """
        Takes the string read in from the GAMP event and parses it into a
        named tuple to store the various values. All values are numpy data
        types.

        Args:
            string (str): The string containing the GAMP Particle

        Returns:
            numpy.ndarray: 2 dimensional array,
                [particle_index][particles]
        """
        the_list = string.strip("\n").split(" ")

        particle = numpy.zeros(6, dtype=numpy.float64)
        particle[0] = numpy.float64(the_list[0])  # Particle ID
        particle[1] = numpy.float64(the_list[1])  # Particle Charge
        particle[2] = numpy.float64(the_list[2])  # Particle X Momentum
        particle[3] = numpy.float64(the_list[3])  # Particle Y Momentum
        particle[4] = numpy.float64(the_list[4])  # Particle Z Momentum
        particle[5] = numpy.float64(the_list[5])  # Particle Energy

        return particle

    def close(self):
        self._file.close()


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
            numpy.ndarray: the file that is to be written to disk.
        """
        self._file.write(str(len(data)) + "\n")
        for particle in data:
            self._file.write(
                repr(particle[0]) + " " + repr(particle[1]) + " " +
                repr(particle[2]) + " " + repr(particle[3]) + " " +
                repr(particle[4]) + " " + repr(particle[5]) + "\n"
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

    @staticmethod
    def __index_gamp(file_location):
        """
        Indexes the gamp file for the maximum particle count and event
        count.

        Args:
            file_location (str):  The location of the file being read.

        Returns:
            list[event_index, particle_index]
        """
        event_index = 0
        particle_index = 0
        with io.open(file_location) as stream:
            for index, line in enumerate(stream):
                filtered_line = line.strip("\n").strip()
                if len(filtered_line) == 1:
                    event_index += 1
                    if int(filtered_line) > particle_index:
                        particle_index = int(filtered_line)

        return [event_index, particle_index]

    def parse(self, file_location):
        """
        Parses Gamp Files into a single list.

        Args:
            file_location (str): The location of the GAMP File.

        Returns:
            numpy.ndarray: A list containing all the GampEvents from the
                data file.
        """
        indexes = self.__index_gamp(file_location)
        reader = GampReader(file_location)
        events = numpy.zeros((indexes[0], indexes[1], 6), numpy.float64)

        for index, event in enumerate(reader):
            if not len(event) == indexes[1]:
                event = numpy.resize(event, (indexes[1], 6))
            events[index] = event

        reader.close()
        return events

    @staticmethod
    def __filter_events(event):
        """
        Filters out zero events and returns a the array without those
        events.

        Args:
            event (numpy.ndarray): The event you want zero particles
                removed

        Returns:
            numpy.ndarray: The event with the zero particles striped of
                it.
        """
        while True:
            for index, particle in enumerate(event):
                if particle[0] == 0 and particle[5] == 0:
                    event = numpy.delete(event, index, axis=0)
                    break
            break

        return event

    def write(self, file_location, data):
        """
        Writes the GAMP events from memory to disk, this method can be
        used for single GAMP events but its recommended that you use
        GampWriter for single GAMP event writing or something similar.

        Args:
            file_location (str): The location where to write the GAMP
                file.
            data (numpy.ndarray): The list containing all the GampEvents
                that are to be written to disk.
        """
        writer = GampWriter(file_location)
        for event in data:
            new_event = self.__filter_events(event)
            writer.write(new_event)
        writer.close()


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
        self._file.seek(0)
        count = 0
        while True:
            # Limit how much of the file is tested
            if count == 3 and not self._full:
                break
            number = self._file.readline().strip("\n").strip()

            # If the test has run at least once and has reached the end
            # then end the test
            if count and number == "":
                break

            # If we failed to find the particle count when it was
            # expected end the test with a fail.
            try:
                int(number)
            except ValueError as Error:
                raise definitions.IncompatibleData(
                    "Expected particle count. Found " + repr(Error) +
                    str(count)
                )

            # If we failed to find all the particle data where it was
            # expected then end the test with a fail
            try:
                for index in range(int(number)):
                    data_length = len(self._file.readline().split(" "))
                    if data_length != 6:
                        raise ValueError(
                            "Particle doesn't have all the data "
                            "required by the gamp standard. Has " +
                            repr(data_length) + " at index " + repr(index)
                        )

            except Exception as Error:
                raise definitions.IncompatibleData(
                    "Unexpected exception raised, caught " + repr(Error) +
                    " where it wasn't expected."
                )

            count += 1

    def _test_length(self):
        """
        Tests to make sure that the first number matches the number of
        events. I know that this can be made to be better, however it
        alludes me at this moment.

        Raises:
            PyPWA.libs.data.exceptions.IncompatibleData:
                Raised when the tests fail for this object and the data.
        """
        self._file.seek(0)
        while True:
            number = self._file.readline().strip().strip("\n")
            try:
                if number == "":
                    break
                for index in range(int(number)):
                    self._file.readline()
            except Exception as Error:
                raise definitions.IncompatibleData(
                    "Unexpected exception raised, caught " + str(Error) +
                    " where it wasn't expected."
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
