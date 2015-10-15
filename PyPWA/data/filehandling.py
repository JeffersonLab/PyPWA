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

import fileinput, numpy, click
from abc import ABCMeta, abstractmethod

class DataTemplate:
    __metaclass__ = ABCMeta

    parsed = None

    data = None

    @abstractmethod
    def parse(self, file_location):
        pass

    @abstractmethod
    def write(self, file_location, data= None):
        pass

    def file_length(self, file_name ):
        """
        Methods determines how many lines are in a file.
        params: file_name = the path to the file
        """
        try:
            with open(file_name) as the_file:
                for length, l in enumerate(the_file):
                    pass
            return length + 1
        except IOError:
            raise AttributeError(file_name + " doesn't exsist. Please check your configuration and try again.")


class Kv(DataTemplate):
    """
    This class reads and writes data from and to a Numpy Array.
    Data is accessible threw event_one and event_two
    """

    data_type = None

    def parse(self, file_location):
        """
        Loads Kvs into self.parsed and returns the values
        
        params: file_location- Location of the file to loads
        return: dict = { "kvar": numpy.array() }
        """

        file_length = self.file_length(file_location)

        with open(file_location, 'r') as the_file:
            first_line = the_file.readline().strip("\n")

        try:
            numpy.float64(first_line)
            self.data_type = "QFactor"
        except ValueError:
            self.data_type = "kVar"

        if self.data_type == "kVar":
            self.parsed = {}
            for x in range(len(first_line.split(","))):
                self.parsed[first_line.split(",")[x].split("=")[0]] = numpy.zeros(shape=file_length, dtype="float64")

            with click.progressbar(length=file_length, label="Loading kinematic variables:") as progress:
                for line in fileinput.input([file_location]):
                    the_line = line.strip("\n")

                    for x in range(len(line.split(","))):
                        self.parsed[the_line.split(",")[x].split("=")[0]][count] = numpy.float64(the_line.split(",")[x].split("=")[1])
                    count += 1
                    progress.update(1)
            
            return self.parsed

        elif self.data_type == "QFactor":
            self.parsed = numpy.zeros(shape=file_length, dtype="float64")

            count = 0
            with click.progressbar(length = file_length, label="Loading Qfactor:") as progress:
                for line in fileinput.input([file_location]):
                    self.parsed[count] = line.strip("\n")
                    count += 1
                    progress.update(1)

    def write(self, file_location, data = None):
        if type(data) != None:
            self.data = data
        if type(self.data) != dict:
            if type(self.data) != numpy.ndarray:
                pass #Add Error
            else:
                self.data_type = "QFactor"
        else:
            self.data_type = "kVar"

        if self.data_type == "kVar":
            if self.data[self.data.keys()[0]] != numpy.ndarray:
                pass
            else:
                pass

            kvars = self.data.keys()

            file_length = len(self.data[kvars[0]])
            
            try:
                with open(file_location, "w") as stream:
                    with click.progressbar(length=file_length, label="Writing kinematic variables:") as progress:
                        for event in progess:
                            line = ""
                            for kvar in range(len(kvars)):
                                if kvar > 0:
                                    line += ","
                                line += "{0}={1}".format(kvars[kvar],str(self.data[kvars[kvar]][event]))
                            line +="\n"
                            stream.write(line)
            except:
                raise

        elif self.data_type == "QFactor":
            file_length = len(self.data)

            try:
                with open(file_location, "w") as stream:
                    with click.progressbar(length=file_length, label="Writing QFactors:") as progress:
                        for event in progress:
                            stream.write(str(self.data[event]))
            except:
                raise
