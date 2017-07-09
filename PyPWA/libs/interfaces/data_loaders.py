import numpy

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.interfaces import common

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ParserPlugin(common.BasePlugin):

    def parse(self, text_file):
        # type: (str) -> numpy.ndarray
        """
        Called to read in the data from a file.

        :param str text_file: The path to the file to read.
        :return: All the data from the file.
        :rtype: numpy.ndarray
        """
        raise NotImplementedError

    def write(self, text_file, data):
        # type: (str, numpy.ndarray) -> None
        """
        Called to write a numpy array out to file.

        :param str text_file: The file to write the data out to.
        :param numpy.ndarray data: The array data to write.
        """
        raise NotImplementedError


class IteratorPlugin(common.BasePlugin):

    def return_reader(self, text_file):
        # type: (str) -> Reader
        """
        Returns an initialized reader for that text file.

        :param str text_file: The file to be read over.
        :return: An initialized reader.
        :rtype: internals.Reader
        """
        raise NotImplementedError

    def return_writer(self, text_file, data):
        # type: (str, numpy.ndarray) -> Writer
        """
        Returns an initialized writer that will work with the data type.

        :param str text_file: Where to write the data.
        :param numpy.ndarray data: The array or event you want to write.
        :return: An initialized writer.
        :rtype: internals.Writer
        """
        raise NotImplementedError


class Reader(object):

    def next(self):
        # type: () -> numpy.ndarray
        """
        Called to get the next event from the reader.

        :return: A single event.
        :rtype: numpy.ndarray
        """
        raise NotImplementedError()

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __len__(self):
        return self.get_event_count()

    def __exit__(self, *args):
        self.close()


    def get_event_count(self):
        # type: () -> int
        """
        Called to get the total number of events in the file.

        :return: Count of the events
        :rtype: int
        """
        raise NotImplementedError()

    def close(self):
        # type: () -> None
        """
        Should close any open objects or streams.
        """
        raise NotImplementedError()


class Writer(object):

    def write(self, data):
        # type: (numpy.ndarray) -> None
        """
        Should write the received event to the stream.

        :param numpy.ndarray data: The event data stored in a numpy array.
        """
        raise NotImplementedError()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        # type: () -> None
        """
        Should close the stream and any open streams or objects.
        """
        raise NotImplementedError()
