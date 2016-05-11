"""
Tools needed for the various Amplitude analysing utilities.
"""

import numpy

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"


class AbstractInterface(object):
    pass


class AbstractProcess(object):
    pass


class DictionarySplitter(object):
    """Splits data up depending on time into defined number of chunks"""

    def split(self, data, num_chunks):
        """Entry point for object.
        Args:
            data (dict/float): Data to be split up
            num_chunks (int): Number of chunks to return
        Returns:
            list: Each index is a chunk of the returned data in order
        """
        if num_chunks == 1:
            return [data]

        if type(data) == dict:
            return self._dictionary_split(data, num_chunks)

    @staticmethod
    def _dictionary_split(dictionary, num_chunks):
        """Splits dictionary into user defined number of chunks
        Args:
            dictionary (dict): Dictionary of arrays that needs to be split
            num_chunks (int): Number of chunks
        Returns:
            list: Each index is a chunk of the returned data in order
        """
        split_dictionary = []

        for x in range(num_chunks):
            split_dictionary.append({})

        for data in dictionary:
            if isinstance(dictionary[data], numpy.ndarray):
                for index in range(num_chunks):
                    split_dictionary[index][data] = numpy.array_split(dictionary[data], num_chunks)[index]
            elif isinstance(dictionary[data], dict):
                for index in range(num_chunks):
                    split_dictionary[index][data] = {}
                for key in dictionary[data]:
                    for index in range(num_chunks):
                        split_dictionary[index][data][key] = numpy.array_split(dictionary[data][key], num_chunks)[index]
        return split_dictionary
