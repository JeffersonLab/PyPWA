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

import numpy

from PyPWA.libs.data.builtin import gamp
from PyPWA.configurator import data_types
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Joshua Pond", "Mark Jones"]
__credits__ = ["Joshua Pond", "Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

# TODO: Liquidate the logic into upper level libraries


class GampTranslator(object):
    """
    This class is a convince class used to convert a gamp .txt file
    into a 3 dimensional numpy ndarray saved in numpy's .npy file
    format
    """

    def _read_file(self, gamp_file):
        """
        This function parses a whole gamp file and returns the 3
        dimensional array. The first dimension is the event number.
        The second is the line number in that event (0 is the number of
        particles, >0 is a particle). The third is the index within
        an individual particle.
        """
        reader = gamp.GampReader(gamp_file)
        events = numpy.ones(shape=(1, 1, 6), dtype=numpy.float64)

        for event_index, event in enumerate(reader):
            for particle_index, particle in enumerate(event):
                if particle_index == 0:
                    events.resize(1 + event_index, len(particle) + 1, 6)
                    events[event_index, 0, 0] = len(event)

                events = self._event_parse(
                    events, event_index, particle_index, particle
                )

        return events

    @staticmethod
    def _event_parse(event, event_index, particle_index, particle):
        """
        Takes the numpy array and the GampParticle and loads the particle
        data into the Numpy Array

        Args:
            event (numpy.ndarray): The event array
            event_index (int): Current event index
            particle_index (int): Current Particle index
            particle (collections.namedtuple): The particle

        Returns:

        """
        event[event_index, particle_index, 0] = particle.id
        event[event_index, particle_index, 0] = particle.charge
        event[event_index, particle_index, 0] = particle.x_momentum
        event[event_index, particle_index, 0] = particle.y_momentum
        event[event_index, particle_index, 0] = particle.z_momentum
        event[event_index, particle_index, 0] = particle.energy
        return event

    def translate(self, gamp_file, save_file):
        """
        This function will run the readFile function and then save the
        array to the specified file name.

        Args:
            gamp_file (string): The gamp file needs to be translated.
            save_file (string): The file name the user wants the file
                named(will end in .npy).

        Returns:
            The 3D numpy array of gamp _events
        """
        gamp_numpy_data = self._read_file(gamp_file)
        numpy.save(save_file, gamp_numpy_data)
        return gamp_numpy_data

    @staticmethod
    def write_event(data_slice):
        """
        This function takes a slice of the _events array ([n,:,:]) and
        returns the pythonPWA gampEvent object of that slice.

        Args:
            data_slice (numpy ndarray): The 2 dimensional array of a
                single event from the events 3D array.
        
        Returns:
            data_types.GampEvent
        """
        number_of_particles = int(data_slice[0, 0])

        gamp_maker = data_types.GampParticle()
        gamp_event = data_types.GampEvent(number_of_particles)

        for i in range(number_of_particles):
            data_list = data_slice[i + 1, :]

            particle = gamp_maker.make_particle(
                # ID, Charge
                data_list[0], data_list[1],
                # X momentum, Y momentum, Z momentum
                data_list[2], data_list[3], data_list[4],
                # Energy
                data_list[5]
            )

            gamp_event.append(particle)

        return gamp_event
    
    def write_file(self, out_file, data):
        """
        This function will convert the 3 dimensional array of gamp data
        back into a text file of those _events.

        Args:
            out_file (string): The file name the user wants the file
                named(will end in .txt).
            data (numpy.ndarray): The 3D that will be converted.
        """
        writer = gamp.GampWriter(out_file)
        for i in range(data.shape[0]):
            event = self.write_event(data[i, :, :])
            writer.write(event)
        writer.close()
