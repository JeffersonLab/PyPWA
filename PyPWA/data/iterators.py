"""
Data Iterators.
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
    """Abstrat Class for Iterators
    Args:
        file_location (str): the path to the file
        buffersize (optional[int]): Defaults to 0.
            The size of the buffer to use.
    """
    __metaclass__ = ABCMeta


    def __init__(self, file_location, buffersize = 0):
        self._file_location = file_location
        self._previous = None
        self._current = None
        self._buffersize = buffersize
        self._file = open(file_location, "r", self._buffersize)


    def __iter__(self):
        """Defines object as iterator
        Returns:
            self
        """
        return self


    def reset(self):
        """Resets the iteration."""
        self._file.seek(0)


    @abstractmethod
    def next(self):
        """Moves to next iteration"""
        pass


    @abstractmethod
    def iterator_length(self):
        """Returns number of iterations in file"""
        pass


    def __next__(self):
        """Python 3 wrapper for next()"""
        return self.next()


    def close(self):
        """closes the file"""
        self._file.close()


class SingleIterator(FileIterator):
    """Iterators every character in file"""

    def next(self):
        """Returns single character from file.
        Returns:
            str: Single character
        Raises:
            StopIteration: No characters left in file.
        """
        self._previous = self._current
        self._current = self._file.read(1)
        if self._current == '':
            raise StopIteration
        return self._current


    def iterator_length(self):
        """Retuns max iteration
        Retuns:
            int: Number of characters.
        """
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
    """Iterates over entire Gamp event"""
    def next(self):
        """Returns event in string from
        Returns:
            list of str: Each particle as string in list
        Raises:
            StopIteration: No events left to parse
        """
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
        """Nothing yet"""
        pass
