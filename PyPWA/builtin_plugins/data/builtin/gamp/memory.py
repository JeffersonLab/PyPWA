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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data.builtin.gamp import iterator

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class GampMemory(data_templates.TemplateMemory):
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
        reader = iterator.GampReader(file_location)
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
        writer = iterator.GampWriter(file_location)
        for event in data:
            new_event = self.__filter_events(event)
            writer.write(new_event)
        writer.close()
