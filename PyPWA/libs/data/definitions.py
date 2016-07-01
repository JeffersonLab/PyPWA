#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Holds Data Exceptions

These exceptions are written to help aid the Data module and improve
readability of the traceback errors without obscuring more complex errors.
"""

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class TemplateValidator(object):

    def __init__(self, file_location, full=False):
        self._file_location = file_location
        self._full = full

    def test(self):
        raise NotImplementedError(
            "%s does not overwrite method test. This is the method that "
            "you should use to overwrite to nest your individual tests "
            "into." % self.__class__.__name__
        )


class TemplateMemory(object):

    def parse(self, file_location):
        raise NotImplementedError(
            "%s does not overwrite method parse. This is the method that "
            "you should overwrite to have the object read data into "
            "memory from disk." % self.__class__.__name__
        )

    def write(self, file_location, data):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object write your data to "
            "disk from memory" % self.__class__.__name__
        )


class TemplateReader(object):

    def __init__(self, file_location):
        self._the_file = file_location

    def reset(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object reset properly when "
            "this method is called." % self.__class__.__name__
        )

    @property
    def next_event(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object read in the next "
            "event properly when its called." % self.__class__.__name__
        )

    def __next__(self):
        return self.next_event

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @property
    def previous_event(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object return the last "
            "value that was parsed." % self.__class__.__name__
        )

    def close(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object return the last "
            "value that was parsed." % self.__class__.__name__
        )


class TemplateWriter(object):

    def __init__(self, file_location):
        self._the_file = file_location

    def write(self, data):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object write the data out "
            "to the disk correctly." % self.__class__.__name__
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object properly operated "
            "properly when its called" % self.__class__.__name__
        )


class IncompatibleData(Exception):
    pass


class UnknownData(Exception):
    pass
