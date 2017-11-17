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

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.components.data_processor import file_processor
from PyPWA.libs.components.data_processor import settings

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
