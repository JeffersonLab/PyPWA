"""
Gamp Data Types
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import numpy

class GeantParticleName(object):
    """Handles Geant Particle IDs
    Attributes:
        particles (dict): Geant IDs and associated Particle Names
    """
    particles = {
    1 : "Gamma",
    2 : "Positron",
    3 : "Electron",
    4 : "Neutrino",
    5 : "Muon +",
    6 : "Muon -",
    7 : "Pion 0",
    8 : "Pion +",
    9 : "Pion -",
    10 : "Kaon 0 Long",
    11 : "Kaon +",
    12 : "Kaon -",
    13 : "Neutron",
    14 : "Proton",
    15 : "Antiproton",
    16 : "Kaon 0 Short",
    17 : "Eta",
    18 : "Lambda",
    19 : "Sigma +",
    20 : "Sigma 0",
    21 : "Sigma -",
    22 : "Xi 0",
    23 : "Xi -",
    24 : "Omega",
    25 : "Antineutron",
    26 : "Antilambda",
    27 : "Antisigma -",
    28 : "Antisigma 0",
    29 : "Antisigma +",
    30 : "Antixi 0",
    31 : "Antixi +"
    }


    def particle_name(self, particle_id):
        """Returns particle name from ID
        Args:
            particle_id (int): Geant Particle ID
        Returns:
            str: Particle Name
        """
        return self.particles[particle_id]


class GampParticle(object):
    x = numpy.int(0)
    y = numpy.float64(0.0)
    z = numpy.float64(0.0)
    id = numpy.int(1)
    charge = numpy.bool(1)
    energy = numpy.float64(0.0)


    def __init__(self, id, charge, x, y, z, energy ):
        self.id = numpy.int(id)
        self.postive
        self.x = numpy.float64(x)
        self.y = numpy.float64(y)
        self.z = numpy.float64(z)
        self.charge = numpy.float64(charge)


    def __str__(self):
        return "id={0},charge={1},x={2},y={3},z={4},charge={5}".format(self.id, self.sharge, self.x, self.y, self.z, self.energy)


    def __repr__(self):
        return ("id=%s,x=%s,y=%s,z=%s,charge=%s" % (repr(self.id), repr(self.x), repr(self.y), repr(self.z), repr(self.charge)))


class GampEvent(object):
    def __init__(self, particles):
        self.particles = particles
        self.amount = len(particles)
        self.previous = None
        self.current = None
        self.count = 0


    def __iter__(self):
        return self


    def __next__(self):
        return self.next()


    def next(self):
        if self.count == (self.amount):
            raise StopIteration
        self.previous = self.current
        self.current = self.particles[self.count]
        self.count += 1
        return self.current
