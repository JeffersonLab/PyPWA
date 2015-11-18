"""
Reader.py: Reads formats from 
"""
from abc import ABCMeta, abstractmethod

class FileIterator(object):
    __metaclass__ = ABCMeta
    
    __buffersize = 0

    def __init__(self, file_location, buffersize = None):
        self.__file_location = file_location
        self.__previous = None
        self.__current = None
        if type(buffersize) != type(None):
            self.__buffersize = buffersize
        self.__file = open(file_location, "r", self.__buffersize)

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
        self.__file.close()

class SingleIterator(FileIterator):
    def next(self):
        self.__previous = self.__current
        self.__current = self.__file.read(1)
        if self.__current == '':
            raise StopIteration
        return self.__current

    def iterator_length(self):
        try:
            line_count = 0
            data = open(self.__file_location, "rb", self.__buffersize )

            while True:
                returned = data.read(1)
                if returned == '':
                    break
                count += 1
        except:
            raise
        return line_count


class LineIterator(FileIterator):
    def next(self):
        self.__previous = self.__current
        self.__current = self.__file.readline()
        if self.__current == '':
            raise StopIteration
        return self.__current

    def iterator_length(self):
        """
        Methods determines how many lines are in a file.
        params: file_name = the path to the file
        """
        try:
            with open(self.__file_location, "r", __buffersize) as the_file:
                for length, l in enumerate(the_file):
                    pass
            return length + 1
        except IOError:
            raise AttributeError(self.__file_location + " doesn't exsist. Please check your configuration and try again.")


class GampIterator(FileIterator):
    def next(self):
        self.__previous = self.__current
        particle_count = self.__file.readline()
        if particle_count == '':
            raise StopIteration
        event = []
        for count in range(particle_count):
            event.append(self.file.readline())
        self.__current = event
        return self.__current

    def iterator_length(self):
        #TODO
        pass