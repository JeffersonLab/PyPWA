#!/usr/bin/env python

"""
PyPWA.data.handlers: A collection of file handlers for PyPWA
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "0.6"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Alpha"

import numpy, yaml, PyPWA.data.iterators
from abc import ABCMeta, abstractmethod

class DataTemplate:
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, file_location):
        pass

    @abstractmethod
    def write(self, file_location, data):
        pass


class Kv(DataTemplate):
    def parse(self, file_location):
        iterator = PyPWA.data.iterator.LineIterator(file_location)

        file_length = iterator.iterator_length()

        first_line = iterator.next()

        iterator.reset()

        for x in range(len(first_line.split(","))):
            parsed[first_line.split(",")[x].split("=")[0]] = numpy.zeros(shape=file_length, dtype="float64")

        for count, line in enumerate(iterator):
            the_line = line.strip("\n")

            for x in range(len(line.split(","))):
                parsed[the_line.split(",")[x].split("=")[0]][count] = numpy.float64(the_line.split(",")[x].split("=")[1])
    
    def write( file_location, data ):

        kvars = self.data.keys()
        
        try:
            with open(file_location, "w") as stream:
                for event in data.keys():
                    line = ""
                    for kvar in range(len(kvars)):
                        if kvar > 0:
                            line += ","
                        line += "{0}={1}".format(kvars[kvar],str(self.data[kvars[kvar]][event]))
                    line +="\n"
                    stream.write(line)
        except:
            raise


class QFactor(DataTemplate):

    def parse(self, file_location ):
        iterator = PyPWA.data.LineIterator(file_location)

        file_length = iterator.iterator_length()

        parsed = numpy.zeros(shape=file_length, dtype="float64")

        for count, line in enumerate(iterator):
            parsed[count] = line.strip("\n")

    def write(self, file_location, data):

        with open(file_location, "w") as stream:
            for event in data:
                stream.write(str(data) + "\n")

class KvCsv(DataTemplate):
    def parse(self, file_location ):
        iterator = PyPWA.data.iterator.LineIterator(file_location)

        file_length = iterator.iterator_length - 1

        first_line = iterator.next().strip("\n")

        parsed = {}
        the_list = []

        for x in range(len(first_line.split(","))):
            the_list.append(first_line.split(",")[x])
            parsed[first_line.split(',')[x]] = numpy.zeros(shape=file_length, dtype="float64")

        for count, line in enumerate( iterator ):
            the_line = line.strip("\n")

            for index in range(len(the_line.split(","))):
                parsed[the_list[index]][count] = numpy.float64(the_line.split(",")[index])

        return parsed


    def write(self, file_location, data ):
        with open(file_location, "w") as stream:
            keys = data.keys()

            first_line = ""

            for key in keys:
                first_line += key
                if not key == keys[-1]:
                    y += ","

            stream.write(first_line + "\n" )

            for index in range(len(data[keys[0]])):
                for key in keys:
                    if not key == keys[0]:
                        stream.write(",")
                    stream.write(str(data[key][index]))
                stream.write("\n")


class Weights(DataTemplate):

    def parse(self, file_location):
        iterator = PyPWA.data.iterator.SingleIterator(file_location)
        file_length = iterator.iterator_length()

        weights = numpy.zeros(shape=file_length, dtype=bool)

        for count, weight in enumerate(iterator):
            weights[count] = weight

        return weights

    def write(self, file_location, data):
        with open(file_location, "wb", 8096) as stream:
            for weight in data:
                stream.write(str(weight))

class Yaml(DataTemplate):

    default_flow_style = False

    def parse(self, file_location):
        with open(file_location) as stream:
            self.saved = yaml.load(stream)
        return self.saved

    def write(self, file_location, data = None):
        if  type(self.default_flow_style) != bool:
            warnings.warn("Default flow style is not boolean. Defaulting to false.", UserWarning)
            self.default_flow_style = False

        with open(file_location, "w") as stream:
            stream.write( yaml.dump(data, default_flow_style = self.default_flow_style ) )
