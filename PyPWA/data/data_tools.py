"""
Holds various tools needed by the Data module.
"""
__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

import os, numpy

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

        result = self._character_test(file_location)
        if result:
            return result

        result = self._line_test(file_location)
        if result:
            return result

        raise TypeError("File Type not known!")


    def _extension_test(self,file_location):
        """Attempts to find type based on file extension.
        Args:
            file_location (str): the file path
        Returns:
            str: Type of file if found.
            bool: False if no type is found
        """

        file_extenstion = os.path.splitext(file_location)[1].lower()

        if file_extenstion == ".csv":
            return "KvCsv"
        elif file_extenstion == ".tsv":
            return "KvTsv"
        elif file_extenstion == ".yml":
            return "Yaml"
        else:
            return False


    def _character_test(self, file_location):
        """Checks for single line boolean data type.
        Args:
            file_location (str): the path to the file
        Returns:
            str: Type of file if found.
            bool: False if no type is found
        """

        characters = []

        with open(file_location, "r") as stream:
            for x in range(25):
                characters.append(stream.read(1))

        try:
            for character in characters:
                if not int(character) < 2:
                    return 0
                else:
                    pass
            return "NewWeights"
        except:
            return 0


    def _line_test(self, file_location):
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

        if "=" in first_line:
            return "Kv"
        elif len(first_line) > 1:
            return "Qf"
        elif len(first_line) == 1:
            return "OldWeights"
        else:
            return 0


class DataTypeWrite(object):
    """
    Returns which writer to use based on the data.
    """

    def search(self, data, new = False):
        """Returns best writter based on data
        Args:
            data (object): The data that needs to be written
            new (optional[bool]): Default is False, choose to write data new format.
        """
        if type(data) == dict:
            data_type = "Kv"
        elif type(data) == numpy.ndarray:
            if data.dtype == bool:
                data_type = "OldWeights"
            else:
                data_type = "Qfactor"

        if new:
            if data_type == "Kv":
                data_type == "KvTsv"
            elif data_type == "OldWeights":
                data_type == "NewWeights"
        return data_type
