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
Main object for Parsing Data
"""

from typing import Optional

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.libs.components.data_processor import file_processor, settings

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ShellDataProcessor(file_processor.DataProcessor):

    def __init__(self, enable_cache=True, clear_cache=False):
        # type: (Optional[bool], Optional[bool]) -> None
        self.settings = settings.DataSettings()
        self.settings.clear_cache(clear_cache)
        self.settings.use_cache(enable_cache)

        super(ShellDataProcessor, self).__init__()

    def parse(self, file_location):
        return super(ShellDataProcessor, self).parse(Path(file_location))

    def get_reader(self, file_location):
        return super(ShellDataProcessor, self).get_reader(Path(file_location))

    def write(self, file_location, data):
        return super(ShellDataProcessor, self).write(
            Path(file_location), data
        )

    def get_writer(
            self, file_location, is_particle_pool=False, is_basic_type=False
    ):
        return super(ShellDataProcessor, self).get_writer(
            Path(file_location), is_particle_pool, is_basic_type
        )
