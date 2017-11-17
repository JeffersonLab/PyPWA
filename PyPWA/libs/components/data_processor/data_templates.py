#  coding=utf-8
#
#  PyPWA, a scientific analysis toolkit.
#  Copyright (C) 2016 JLab
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Holds the different implementation interfaces that are needed to interface
data module.
"""

from typing import List

import numpy

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class DataPlugin(object):

    @property
    def plugin_name(self):
        # type: () -> str
        raise NotImplementedError()

    def get_plugin_memory_parser(self):
        # type: () -> Memory
        raise NotImplementedError()

    def get_plugin_reader(self, file_location):
        # type: (str) -> Reader
        raise NotImplementedError()

    def get_plugin_writer(self, file_location):
        # type: (str) -> Writer
        raise NotImplementedError()

    def get_plugin_read_test(self):
        # type: () -> ReadTest
        raise NotImplementedError()

    @property
    def plugin_supported_extensions(self):
        # type: () -> List[str]
        raise NotImplementedError()

    @property
    def plugin_supports_columned_data(self):
        # type: () -> bool
        raise NotImplementedError()

    @property
    def plugin_supports_single_array(self):
        # type: () -> bool
        raise NotImplementedError

    @property
    def plugin_supports_tree_data(self):
        # type: () -> bool
        raise NotImplementedError()


class Memory(object):

    def parse(self, file_location):
        # type: (str) -> numpy.ndarray
        raise NotImplementedError()

    def write(self, file_location, data):
        # type: (str, numpy.ndarray) -> None
        raise NotImplementedError()


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


class ReadTest(object):

    def test(self, file_location):
        # type: (str) -> None
        """
        Raises:
            PyPWA.builtin_plugins.data.exceptions.IncompatibleData: Raised
                when data  failed to test properly for the file.
        """
        raise NotImplementedError()
