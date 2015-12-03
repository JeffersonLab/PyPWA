"""
Holds various tools needed by the Data module.
"""
import os
import numpy
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"


class DataTypeSearch(object):
    """
    Object that searches for the best data wrapper 
    to use for the file in question
    """

    def search(self, file_location):
        """
        Search function, attempts multiple different search patterns to try
        to find a data type

        Args:
            file_location (str): The file that is to be parsed
        Returns:
            str: Type of File
        Raises:
            TypeError: If the file type can't be found
        See Also:
            Supported Data formats
        """

        result = self._extension_test(file_location)
        if result:
            return result

        result = self._line_test(file_location)
        if result:
            return result

        raise TypeError("File Type not known!")

    @staticmethod
    def _extension_test(file_location):
        """Attempts to find type based on file extension.
        Args:
            file_location (str): the file path
        Returns:
            str: Type of file if found.
            bool: False if no type is found
        """

        file_extension = os.path.splitext(file_location)[1].lower()

        if file_extension in ( ".csv", ".tsv"):
            return "sv"
        elif file_extension == ".yml":
            return "yaml"
        elif file_extension == ".pwa":
            return "pwa"
        else:
            return False

    @staticmethod
    def _line_test(file_location):
        """
        Loads the first line and checks it for patterns to
        try to determine the type.

        Args:
            file_location (str): the path to the file
        Returns:
            str: Type of file if found.
            bool: False if no type is found
        """
        with open(file_location, "r") as stream:
            first_line = stream.readline().strip("\n")

        if "=" in first_line or len(first_line) >= 1:
            return "kv"
        else:
            return 0


class DataTypeWrite(object):
    """
    Returns which writer to use based on the data.
    """
    @staticmethod
    def search(file_location):
        """Returns best writer based on data
        Args:
            file_location (str):
        Returns:
            str:
        """
        file_extension = os.path.splitext(file_location)[1].lower()

        if file_extension in (".tsv", ".csv"):
            return "sv"
        elif file_extension == ".yml":
            return "yaml"
        elif file_extension == ".pwa":
            return "pwa"
        else:
            return "kv"


class DataTypes(object):

    def type(self, data):
        if isinstance(data, numpy.ndarray):
            return self._arrays(data)
        elif isinstance(data):
            return self._dicts(data)

    @staticmethod
    def _dicts(data):
        keys = data.keys()
        if isinstance(data[keys[0]], numpy.ndarray):
            return "dictofarrays"
        else:
            return "dictofdicts"

    @staticmethod
    def _arrays(data):
        if isinstance(data[0], numpy.bool):
            return "listofbools"
        else:
            return "listoffloats"

