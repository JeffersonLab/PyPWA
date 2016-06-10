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
This file imports the uses python files and plugins from their specified
location. This is an internal file only, and should be only be used by the
configuratr.
"""

from __future__ import absolute_import

import sys
import logging
import os

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ImportTools(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def import_package(self, folder):
        self._append_path(folder)
        return __import__(os.path.basename(folder))

    def import_object(self, file, object_name):
        self._append_path(file)
        imported = self._import_script(file)
        return self._extract_object(imported, object_name)

    def _import_script(self, file):
        self._append_path(file)
        return __import__(os.path.basename(file).strip(".py"))

    @staticmethod
    def _extract_object(imported, object_name):
        return getattr(imported, object_name)

    @staticmethod
    def _append_path(file):
        sys.path.append(os.path.dirname(file))
