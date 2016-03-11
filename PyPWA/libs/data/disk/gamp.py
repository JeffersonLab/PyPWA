import collections
import numpy
import fileinput
import io
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"


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
        super(GampReader, self).__init__()
        self._the_file = gamp_file
        self._file = False
        self._previous_event = None
        self._particle_master = collections.namedtuple("GampParticle",
                                                       ["name", "id", "charge", "x", "y", "z", "energy"])

        self._start_input()

    def _start_input(self):
        if self._file:
            self._file.close()
        self._file = io.open(self._the_file, "rt")

    def reset(self):
        self._start_input()

    def __next__(self):
        self.next_event

    @property
    def next_event(self):
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
        the_list = string.strip("\n").split(" ")
        particle = self._particle_master(self._particles[int(the_list[0])], numpy.uint8(the_list[0]),
                                         numpy.int8(the_list[1]), numpy.float64(the_list[2]),
                                         numpy.float64(the_list[3]), numpy.float64(the_list[4]),
                                         numpy.float64(the_list[5]))
        return particle

    def __del__(self):
        self._file.close()


class GampWriter(object):

    def __init__(self, gamp_file):
        self._file = io.open(gamp_file, "w")

    def __del__(self):
        self._file.close()

    def write_event(self, event):
        self._file.write(str(len(event))+"\n")

        for particle in event:
            self._file.write(str(particle.id) + " " + str(particle.charge) + " " + str(particle.x) + " " +
                             str(particle.y) + " " + str(particle.z) + " " + str(particle.energy) + "\n")

    def close(self):
        self._file.close()


class GampEvent(collections.deque):

    def __init__(self, particle_count):
        super(GampEvent, self).__init__(maxlen=particle_count)

    def search(self, query):
        for particle in self:
            if particle.name == query:
                return particle
