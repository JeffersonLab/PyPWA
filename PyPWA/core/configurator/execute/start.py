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
Where the program really starts.
--------------------------------
This is a progs object to connect the two major halves of execute together,
_settings that loads the settings into something usable, and _plugins that
takes those settings to package together a little runnable program.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator.execute import _plugin_data
from PyPWA.core.configurator.execute import _settings

from typing import Dict

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Execute(object):

    def __init__(self):
        self.__settings = _settings.Setup()
        self.__executor = None  # type: _plugin_data.SetupProgram

    def run(self, function_settings, configuration_location):
        # type: (Dict[str, str], str) -> None
        self.__set_settings(function_settings, configuration_location)
        self.__set_executor()
        self.__execute()

    def __set_settings(self, function_settings, configuration_location):
        # type: (Dict[str, str], str) -> None
        self.__settings.load_settings(
            function_settings, configuration_location
        )

    def __set_executor(self):
        self.__executor = _plugin_data.SetupProgram(self.__settings)

    def __execute(self):
        self.__executor.setup()
        self.__executor.execute()
