"""
A collection of file handlers for PyPWA
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones", "Josh Pond"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import os
import yaml

import PyPWA.libs.data.data_tools as data_tools
from PyPWA.libs.data.memory import sv, kv


class DataInterface(object):
    """Interface for Data Objects"""

    @staticmethod
    def parse(file_location):
        raise NotImplementedError("Object doesn't implement parse()")

    @staticmethod
    def write(file_location, data):
        raise NotImplementedError("Object doesn't implement write()")


class Kv(DataInterface):

    @staticmethod
    def parse(file_location):
        with open(file_location) as stream:
            first_line = stream.readline()

        if "=" in first_line:
            reader = kv.DictOfArrays()
        elif len(first_line.strip("\n")) == 1:
            reader = kv.ListOfBooleans()
        elif len(first_line.strip("\n")) > 1:
            reader = kv.ListOfFloats()
        else:
            raise TypeError("Unknown data type for {0} !".format(file_location))

        return reader.parse(file_location)

    @staticmethod
    def write(file_location, data):
        data_check = data_tools.DataTypes()
        the_type = data_check.type(data)

        if the_type == "dictofarrays":
            writer = kv.DictOfArrays()
        elif the_type == "listofbools":
            writer = kv.ListOfBooleans()
        elif the_type == "listoffloats":
            writer = kv.ListOfFloats()
        else:
            raise TypeError("Unknown type {0} !".format(the_type))

        writer.write(file_location, data)


class Sv(DataInterface):

    @staticmethod
    def parse(file_location):
        file_ext = os.path.splitext(file_location)[1]

        if file_ext == ".tsv":
            parser = sv.SvParser("\t")
        elif file_ext == ".csv":
            parser = sv.SvParser(",")
        else:
            raise TypeError("Variable separated files must end in .tsv or .csv!")

        return parser.reader(file_location)

    @staticmethod
    def write(file_location, data):
        raise NotImplementedError("Writing of Variable Separated files is not yet supported")


class Binary(DataInterface):
    def __init__(self):
        raise NotImplementedError("There isn't any defined standard yet")


class Yaml(DataInterface):
    """YAML Parsing Object"""

    @staticmethod
    def parse(file_location):
        """Parses Yaml configuration files from disk
        Args:
            file_location (str): Path to the file
        Returns:
            dict: The values stored in a multidimensional dictionary
        """
        with open(file_location) as stream:
            saved = yaml.load(stream)
        return saved

    @staticmethod
    def write(file_location, data):
        """Writes YAML Configs to disk
        Args:
            file_location (str): Path to the file
            data (dict): Dictionary to write.
        """

        with open(file_location, "w") as stream:
            stream.write(yaml.dump(data))
