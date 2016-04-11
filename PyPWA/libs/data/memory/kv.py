
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


class KvInterface(object):

    def parse(self, file_location):
        raise NotImplementedError("Class %s doesn't implement parse()" % self.__class__.__name__)

    @staticmethod
    def write(file_location, data):
        raise NotImplementedError("Object doesn't implement write()")

    @staticmethod
    def file_length(file_location):
        """Determines the number of lines in the file.

        Args:
            file_location (str): The file to check for line count.
        Returns:
            int: The number of lines.
        """
        with io.open(file_location) as stream:
            for file_length, line in enumerate(stream):
                pass
        return file_length + 1


class DictOfArrays(KvInterface):
    """Handles old Kv format"""

    def parse(self, file_location):
        """Loads Kv data into memory
        Args:
            file_location (str): Path of file
        Returns:
            dict: name : numpy array of events
        """

        file_length = self.file_length(file_location)

        with open(file_location) as stream:
            first_line = stream.readline()

        parsed = {}

        for x in range(len(first_line.split(","))):
            parsed[first_line.split(",")[x].split("=")[0]] = numpy.zeros(shape=file_length, dtype="float64")

        with io.open(file_location) as stream:
            for index, line in enumerate(stream):

                for particle_count in range(len(line.split(","))):
                    parsed[line.split(",")[particle_count].split("=")[0]][index] = \
                        numpy.float64(line.strip("\n").split(",")[particle_count].split("=")[1])
        return parsed

    @staticmethod
    def write(file_location, data):
        """Writes Classic Kvs to file
        Args:
            file_location (str): path to file
            data (dict): dict of numpy arrays
        """

        kvars = list(data)

        with open(file_location, "w") as stream:
            for event in range(len(data[kvars[0]])):
                line = ""
                for kvar in range(len(kvars)):
                    if kvar > 0:
                        line += ","
                    line += "{0}={1}".format(kvars[kvar], str(data[kvars[kvar]][event]))
                line += "\n"
                stream.write(line)


class ListOfFloats(KvInterface):
    """Handles QFactor list parsing"""

    def parse(self, file_location):
        """Parses a list of factors
        Args:
            file_location (str): The path to file
        Returns:
            numpy.ndarray: Array of factors
        """

        file_length = self.file_length(file_location)

        parsed = numpy.zeros(shape=file_length, dtype="float64")

        with io.open(file_location) as stream:
            for count, line in enumerate(stream):
                parsed[count] = line.strip("\n")
        return parsed

    @staticmethod
    def write(file_location, data):
        """Writes Arrays to disk as floats
        Args:
            file_location (str): Path to file
            data (numpy.ndarray): Data to be written to disk
        """
        with open(file_location, "w") as stream:
            for event in data:
                stream.write(str(event) + "\n")


class ListOfBooleans(KvInterface):
    """Classic boolean per line data type"""

    def parse(self, file_location):
        """Parses list of booleans into numpy array.
        Args:
            file_location (str): Path to file
        Returns:
            numpy.ndarray: Bool array of weights
        """

        file_length = self.file_length(file_location)

        weights = numpy.zeros(shape=file_length, dtype=bool)

        with io.open(file_location) as stream:
            for index, weight in enumerate(stream):
                weights[index] = int(weight)

        return weights

    @staticmethod
    def write(file_location, data):
        """Writes booleans to text file with each weight on a new line
        Args:
            file_location (str): Path to file
            data (numpy.ndarray): Array of booleans
        """
        with open(file_location, "w") as stream:
            for weight in data:
                stream.write(str(int(weight)) + "\n")
