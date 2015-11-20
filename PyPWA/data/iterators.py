"""
PyPWA/data/iterators.py: Different iterators to pull a single
"""

__author__ = "Mark Jones"
__credits__ = ["Mark Jones"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Mark Jones"
__email__ = "maj@jlab.org"
__status__ = "Beta0"

from abc import ABCMeta, abstractmethod

class FileIterator(object):
    """
    Abstract Class for iterators inside PyPWA.data, __init__ funciton is predefined.
    """
    __metaclass__ = ABCMeta

    def __init__(self, file_location, buffersize = 0):
        self._file_location = file_location
        self._previous = None
        self._current = None
        self._buffersize = buffersize
        self._file = open(file_location, "r", self._buffersize)

    def __iter__(self):
        return self

    def reset(self):
        self._file.seek(0)

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def iterator_length(self):
        pass

    def __next__(self):
        return self.next()

    def close(self):
        self._file.close()

class SingleIterator(FileIterator):
    def next(self):
        self._previous = self._current
        self._current = self._file.read(1)
        if self._current == '':
            raise StopIteration
        return self._current

    def iterator_length(self):
        try:
            line_count = 0
            data = open(self._file_location, "rb", self._buffersize )

            while True:
                returned = data.read(1)
                if returned == '':
                    break
                line_count += 1
        except:
            raise
        return line_count


class GampIterator(FileIterator):
    def next(self):
        self._previous = self._current
        particle_count = self._file.readline()
        if particle_count == '':
            raise StopIteration
        event = []
        for count in range(particle_count):
            event.append(self._file.readline())
        self._current = event
        return self._current

    def iterator_length(self):
        #TODO
        pass