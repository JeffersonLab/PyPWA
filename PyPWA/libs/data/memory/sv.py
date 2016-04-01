
import csv
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


class SvParser(object):
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def reader(self, file_location):
        with io.open(file_location, "rt") as stream:
            for line_count, throw in enumerate(stream):
                pass

        with io.open(file_location, "rt") as stream:
            sv = csv.reader(stream, delimiter=self.delimiter)

            elements = next(sv)
            parsed = {}
            for element in elements:
                parsed[element] = numpy.zeros(shape=line_count, dtype="float64")

            for index, row in enumerate(sv):
                for count in range(len(row)):
                    parsed[elements[count]][index] = row[count]

        return parsed

    def writer(self, file_location, data):
        raise NotImplementedError("Writing of Variable Separated Values is unsupported at this time")
