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

import logging
import re

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
        """

        Args:
            options:
        """
        local_logger = logging.getLogger(__name__)
        local_logger.addHandler(logging.NullHandler())

        for key in list(options.keys()):
            underscores = "_" + key.replace(" ", "_")
            lowercase = underscores.lower()
            final = re.sub(r'[^a-z0-9_]', '', lowercase)
            local_logger.debug("Converted {0} to {1}".format(key, final))
            setattr(self, final, options[key])


class MinimizerTemplate(_InitialOptions):
    """
    Template for minimization plugins.
    """
    def __init__(self, options):
        """

        Args:
            options:
        """
        super(MinimizerTemplate, self).__init__(options)

    def main_options(self, calc_function, fitting_type=False):
        """

        Args:
            calc_function:
            fitting_type:

        Returns:

        """
        raise NotImplementedError

    def start(self):
        """

        Returns:

        """
        raise NotImplementedError

    def return_parser(self):
        """

        Returns:

        """
        raise NotImplementedError

    def save_extra(self, save_name):
        """

        Args:
            save_name:

        Returns:

        """
        raise NotImplementedError


class KernelProcessingTemplate(_InitialOptions):
    """
    Template for kernel processing plugins.
    """
    def __init__(self, options):
        """

        Args:
            options:
        """
        super(KernelProcessingTemplate, self).__init__(options)

    def main_options(self, data, process_template, interface_template):
        """

        Args:
            data:
            process_template:
            interface_template:

        Returns:

        """
        raise NotImplementedError

    def fetch_interface(self):
        """

        Returns:

        """
        raise NotImplementedError


class DataParserTemplate(_InitialOptions):
    """
    Template for data parser and writing plugins
    """

    def __init__(self, options):
        """

        Args:
            options:
        """
        super(DataParserTemplate, self).__init__(options)

    def parse(self, text_file):
        """

        Args:
            text_file:

        Returns:

        """
        raise NotImplementedError

    def write(self, data, text_file):
        """

        Args:
            data:
            text_file:

        Returns:

        """
        raise NotImplementedError


class DataReaderTemplate(_InitialOptions):
    """
    Template for data reader and writers plugins.
    """

    def __init__(self, options):
        """

        Args:
            options:
        """
        super(DataReaderTemplate, self).__init__(options)

    def return_reader(self, text_file):
        """

        Args:
            text_file:

        Returns:

        """
        raise NotImplementedError

    def return_writer(self, text_file, data_shape):
        """

        Args:
            text_file:
            data_shape:

        Returns:

        """
        raise NotImplementedError


class ShellMain(_InitialOptions):

    def __init__(self, options):
        """

        Args:
            options:
        """
        super(ShellMain, self).__init__(options)

    def start(self):
        """

        Returns:

        """
        raise NotImplementedError
