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
Handles direct interaction with plugins
---------------------------------------

- MetadataStorage - Interacts directly with the plugins.
- GetPluginList - Stores the dependency plugins for the configuration.
"""

import logging

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator import options
from PyPWA.initializers.configurator import storage
from PyPWA.initializers.configurator.create_config import _questions
from typing import Any, Dict, Union, List

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION

__STORAGE_TYPE = Dict[Union[str, options.Levels], Any]


class MetadataStorage(storage.Storage):

    __LOGGER = logging.getLogger(__name__)

    def __init__(self):
        super(MetadataStorage, self).__init__()
        self.__actual_storage = None  # type: __STORAGE_TYPE
        self._update_extra()

    def request_program_by_name(self, name):
        # type: (str) -> options.Program
        for plugin in self._get_programs():
            print(plugin.name)
            if plugin.name == name:
                return plugin
        raise ValueError("Unknown program name '%s'" % name)


class GetPluginList(object):

    __LOGGER = logging.getLogger(__name__)

    def __init__(self):
        self.__ask_for_plugin = _questions.GetSpecificPlugin()
        self.__storage = MetadataStorage()
        self.__components = []  # type: List[options.Component]
        self.__main_plugin = None  # type: options.Program

    def parse_plugins(self, main_plugin):
        # type: (options.Program) -> None
        self.__main_plugin = main_plugin
        self.__components = main_plugin.get_required_components()
        self.__check_for_choices()

    def __check_for_choices(self):
        for component in self.__components:
            if isinstance(component, options.HasChoices):
                self.__process_choice(component)

    def __process_choice(self, component):
        if len(component.choices) > 1:
            self.__ask_for_plugin.ask_for_plugin(
                component.choices, component.choice_type
            )
            component.set_choice(self.__ask_for_plugin.get_specific_plugin())
        elif len(component.choices) == 1:
            component.set_choice(component.choices[0])
        else:
            component.set_choice(None)

    @property
    def components(self):
        # type: () -> List[options.Component]
        return self.__components

    @property
    def program(self):  # needed so that BuildConfig can know the program plugin
        # type: () -> options.Program
        return self.__main_plugin
