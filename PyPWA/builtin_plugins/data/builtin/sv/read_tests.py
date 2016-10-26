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

import csv
import io

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data import exceptions
from PyPWA.builtin_plugins.data.builtin.sv import HEADER_SEARCH_BITS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class SvDataTest(data_templates.ReadTest):

    def quick_test(self, file_location):
        self._check_header(file_location)

    def full_test(self, file_location):
        self._check_header(file_location)

    @staticmethod
    def _check_header(text_file):

        the_file = io.open(text_file)

        if not csv.Sniffer().has_header(
                the_file.read(HEADER_SEARCH_BITS),
        ):
            raise exceptions.IncompatibleData(
                "CSV Module failed to find the files header in " +
                str(HEADER_SEARCH_BITS) + " characters!"
            )
