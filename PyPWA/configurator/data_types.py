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
Provides the data types used throughout the program, from GAMP to Generic
"""

import collections
import logging

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class GampParticle(object):

    _particles = {  # Holds name / id associations for Gamp.
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

    def __init__(self):
        """
        Simple object that makes the particles for GAMP. Supplies a static tuple
        with all fields stored in a read only state.
        """
        self._the_particle = collections.namedtuple("GampParticle",
                                                    ["name", "id", "charge",
                                                     "x", "y", "z", "energy"]
                                                    )

    def make_particle(self, the_id, charge, x, y, z, energy):
        """
        Method that builds the particle using the supplied information. Acts as
        a wrapper around a namedtuple that has some logic to aid in adding
        information to the particle.

        Args:
            the_id: The Particle's ID
            charge: The Charge of the particle.
            x: The X momentum of the particle.
            y: The Y momentum of the particle.
            z: The Z momentum of the particle.
            energy: The energy of the particle.

        Returns:
            collections.namedtuple: The particle and its associated information.

        """
        name = self._particles[the_id]
        return self._the_particle(name, the_id, charge, x, y, z, energy)


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


class GenericEvent(object):

    def __init__(self, particle_names):
        """
        Makes Generic Event Objects based off of NamedTuples. Should provide
        a minor improvement in speed without too much change in design.

        Args:
            particle_names (list[str]): List of the names of the particles.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

        final_particle_names = particle_names + ["standard_parsed_values"]

        self._logger.debug("Final Particle Names inside Generic Event = " +
                           str(final_particle_names))

        self._master_particle = collections.namedtuple(
            "GenericEvent", final_particle_names)

        self._particle_names = particle_names

    def make_particle(self, data):
        """
        Makes the particle using the data that was sent to the method.
        Args:
            data (list): The data that is to be loaded into the
                namedtuple.

        Returns:
            namedtuple: The final event that is to be sent back.
        """
        data.append(self._particle_names)
        names = self._particle_names + ["standard_parsed_values"]

        self._logger.debug("Name Values: " + str(names))
        self._logger.debug("Data Values: " + str(data))

        return self._master_particle(**dict(zip(names, data)))
