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

"""

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _InitialOptions(object):
    def __init__(self, options):
        for key in list(options.keys()):
            setattr(self, "_" + key.replace(" ", "_"), options[key])


class MinimizerTemplate(_InitialOptions):
    """
    Template for minimization plugins.
    """
    def __init__(self, options):
        super(MinimizerTemplate, self).__init__(options)

    def main_options(self, calc_function, fitting_type=False):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def return_parser(self):
        raise NotImplementedError


class KernelProcessingTemplate(_InitialOptions):
    """
    Template for kernel processing plugins.
    """
    def __init__(self, options):
        super(KernelProcessingTemplate, self).__init__(options)

    def main_options(self, data, process_template, interface_template):
        raise NotImplementedError

    def fetch_interface(self):
        raise NotImplementedError


class DataParserTemplate(_InitialOptions):
    """
    Template for data parser and writing plugins
    """

    def __init__(self, options):
        super(DataParserTemplate, self).__init__(options)

    def parse(self, text_file):
        raise NotImplementedError

    def write(self, data, text_file):
        raise NotImplementedError


class DataReaderTemplate(_InitialOptions):
    """
    Template for data reader and writers plugins.
    """

    def __init__(self, options):
        super(DataReaderTemplate, self).__init__(options)

    def return_reader(self, text_file):
        raise NotImplementedError

    def return_writer(self, text_file, data_shape):
        raise NotImplementedError


class ShellMain(_InitialOptions):

    def __init__(self, options):
        super(ShellMain, self).__init__(options)

    def start(self):
        raise NotImplementedError
