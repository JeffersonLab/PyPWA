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

from PyPWA import AUTHOR, VERSION
from PyPWA.builtin_plugins.data import iterator
from PyPWA.builtin_plugins.data import memory
from PyPWA.core.configurator import options

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class SetupParser(options.Setup):

    __options_object = None
    __interface = None

    def __init__(self, command_object):
        self.__options_object = command_object
        self.__setup_memory_parser()

    def __setup_memory_parser(self):
        self.__interface = memory.Memory(
            enable_cache=self.__options_object.enable_cache,
            clear_cache=self.__options_object.clear_cache,
            user_plugin_dir=self.__options_object.user_plugin
        )

    def return_interface(self):
        return self.__interface


class SetupIterator(options.Setup):

    __options_object = None
    __interface = None

    def __init__(self, command_object):
        self.__options_object = command_object
        self.__setup_iterator()

    def __setup_iterator(self):
        self.__interface = iterator.Iterator(
            fail=self.__options_object.fail,
            user_plugin=self.__options_object.user_plugin
        )

    def return_interface(self):
        return self.__interface
