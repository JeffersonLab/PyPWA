#!/usr/bin/env python

"""
PyPWA.data.handlers: A collection of file handlers for PyPWA
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import fileinput
from abc import ABCMeta, abstractmethod
import numpy, yaml, PyPWA.data.iterators

class DataTemplate:
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, file_location): pass

    @abstractmethod
    def write(self, file_location, data): pass


class Kv(DataTemplate):
    def parse(self, file_location):


        #This loop both sets the first_line variable, and finds the number of lines in the file
        for file_length, line in enumerate(fileinput.input(file_location)):
            if file_length == 0:
                first_line = line
        fileinput.close()


        parsed = {}

        for x in range(len(first_line.split(","))):
            parsed[first_line.split(",")[x].split("=")[0]] = numpy.zeros(shape=file_length+1, dtype="float64")

        for index, line in enumerate(fileinput.input(file_location)):
            the_line = line.strip("\n")

            for particle_count in range(len(line.split(","))):
                parsed[the_line.split(",")[particle_count].split("=")[0]][index] = numpy.float64(the_line.split(",")[particle_count].split("=")[1])
        fileinput.close()

        return parsed
    
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
        fileinput.close()

        for file_length, line in enumerate(fileinput.input(file_location)):
            pass
        fileinput.close()

        parsed = numpy.zeros(shape=file_length+1, dtype="float64")

        for count, line in enumerate(fileinput.input(file_location)):
            parsed[count] = line.strip("\n")
        fileinput.close()
        return parsed

    def write(self, file_location, data):

        with open(file_location, "w") as stream:
            for event in data:
                stream.write(str(data) + "\n")

class KvCsv(DataTemplate):
    def parse(self, file_location ):
        iterator = PyPWA.data.iterators.LineIterator(file_location)

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


class OldWeights(DataTemplate):
    
    def parse(self, file_location):
        for file_length, line in enumerate(fileinput.input(file_location)):
            pass
        fileinput.close()

        weights = numpy.zeros(shape=file_length, dtype=bool)

        for index, weight in enumerate(fileinput.input(file_location)):
            weights[index] = weight

        return weights

    def write(self, file_location, data ):
        with open(file_location, "w") as stream:
            for weight in data:
                stream.write(str(int(weight))+"\n")



class NewWeights(DataTemplate):

    def parse(self, file_location):
        iterator = PyPWA.data.iterators.SingleIterator(file_location)
        file_length = iterator.iterator_length()

        weights = numpy.zeros(shape=file_length, dtype=bool)

        for index, weight in enumerate(iterator):
            weights[index] = weight

        return weights

    def write(self, file_location, data):
        with open(file_location, "wb") as stream:
            for weight in data:
                stream.write(str(int(weight)))

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
