import csv
import fileinput
import numpy


class SvParser(object):
    def __init__(self, delimiter):
        self.delimiter = delimiter

    def reader(self, file_location):
        for line_count, throw in enumerate(fileinput.input(file_location)):
            pass

        with open(file_location, "rt") as stream:
            sv = csv.reader(stream, delimiter=self.delimiter)

            elements = sv.next()
            parsed = {}
            for element in elements:
                parsed[element] = numpy.zeros(shape=line_count, dtype="float64")

            for index, row in enumerate(sv):
                for count in range(len(row)):
                    parsed[elements[count]][index] = row[count]

        return parsed

    def writer(self, file_location, data):
        raise NotImplementedError("Writing of Variable Separated Values is unsupported at this time")
