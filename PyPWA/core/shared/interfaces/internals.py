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

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class Reader(object):

    def next(self):
        raise NotImplementedError()

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        raise NotImplementedError()


class Writer(object):

    def write(self, data):
        raise NotImplementedError()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        raise NotImplementedError()


class ProcessInterface(object):

    def run(self, *args):
        raise NotImplementedError

    @property
    def previous_value(self):
        raise NotImplementedError

    def stop(self, force=False):
        raise NotImplementedError

    @property
    def is_alive(self):
        raise NotImplementedError


class Kernel(object):

    processor_id = None

    def setup(self):
        raise NotImplementedError()

    def process(self, data=False):
        raise NotImplementedError()


class KernelInterface(object):

    is_duplex = False

    def run(self, communicator, args):
        raise NotImplementedError("The run method must be extended!")


class MinimizerOptionParser(object):

    def convert(self, passed_value):
        raise NotImplementedError
