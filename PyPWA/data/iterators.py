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
    
    buffersize = 0

    def __init__(self, file_location, buffersize = None):
        self.file_location = file_location
        self.previous = None
        self.current = None
        if type(buffersize) != type(None):
            self.buffersize = buffersize
        self.file = open(file_location, "r", self.buffersize)

    def __iter__(self):
        return self

    def reset(self):
        self.file.seek(0)

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def iterator_length(self):
        pass

    def __next__(self):
        return self.next()

    def close(self):
        self.file.close()

class SingleIterator(FileIterator):
    def next(self):
        self.previous = self.current
        self.current = self.file.read(1)
        if self.current == '':
            raise StopIteration
        return self.current

    def iterator_length(self):
        try:
            line_count = 0
            data = open(self.file_location, "rb", self.buffersize )

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
        self.previous = self.current
        particle_count = self.file.readline()
        if particle_count == '':
            raise StopIteration
        event = []
        for count in range(particle_count):
            event.append(self.file.readline())
        self.current = event
        return self.current

    def iterator_length(self):
        #TODO
        pass