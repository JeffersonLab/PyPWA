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
The core plugin parser for functions and packages.
--------------------------------------------------
There are 5 objects here, _AppendPath, _Importer, _FilterBySubclass,
_PluginStorage and the main PluginLoader object. If you wish to use the
plugin storage module, you will need to call and use PluginLoader.

.. note::
    This plugin will save all loaded plugins anywhere in the program. The
    benefit to this is that all user plugins can be loaded once, then

- _AppendPath - This object takes the path of modules that exist outside of
  the defined Python Path and imports their root directory into the System
  Path

- _Importer - This object actually imports the module, and all of its
  submodules, then returns those submodules.

- _FilterBySubclass - this object takes all the loaded objects from the
  PluginStorage then searches for all objects that are subclass-ed by the
  provided class.

- _PluginStorage - This object actually stores everything that was imported
  from the provided locations.

- PluginLoader - The main object, returns objects and functions based on the
  provided search conditions.
"""

import importlib
import logging
import os
import pkgutil
import sys

from typing import Any, Callable, List, Union, Set
import types

from PyPWA import AUTHOR, VERSION

__credits__ = [
    "Mark Jones",
    "jp. @ Stack Overflow",
    "unutbu @ Stack Overflow"
]
__author__ = AUTHOR
__version__ = VERSION


class _AppendPath(object):

    __LOGGER = logging.getLogger(__name__ + "._AppendPath")

    def append_path(self, filename):
        # type: (str) -> None
        function_path = self.__get_function_path(filename)
        self.__log_path(function_path)
        sys.path.append(function_path)

    @staticmethod
    def __get_function_path(filename):
        # type: (str) -> str
        absolute_path = os.path.abspath(filename)
        path_without_basename = os.path.dirname(absolute_path)
        return path_without_basename

    def __log_path(self, path):
        # type: (str) -> None
        self.__LOGGER.debug("Adding %s to the path." % path)


class _Importer(object):

    __LOGGER = logging.getLogger(__name__ + "._Importer")

    def __init__(self):
        self.__path_handler = _AppendPath()

    def fetch_modules(self, package):
        # type: (Union[str, types.ModuleType]) -> List[object]
        found_module = self.__load_module(package)
        return self.__process_module(found_module)

    def __load_module(self, package):
        # type: (Union[str, types.ModuleType]) -> object
        if isinstance(package, types.ModuleType):
            return package
        else:
            return self.__import_module(package)

    def __import_module(self, package):
        # type: (str) -> types.ModuleType
        self.__path_handler.append_path(package)
        name = self.__get_module_name(package)
        return self.__get_module(name)

    @staticmethod
    def __get_module_name(package):
        # type: (str) -> str
        file_name = os.path.basename(package)
        module_name = os.path.splitext(file_name)[0]
        return module_name

    def __get_module(self, package):
        # type: (str) -> types.ModuleType
        try:
            return importlib.import_module(package)
        except Exception as Error:
            self.__process_module_error(Error)

    def __process_module_error(self, error):
        # type: (Exception) -> None
        self.__LOGGER.warning(error)

    def __process_module(self, potential_module):
        # type: (types.ModuleType) -> List[types.ModuleType]
        if hasattr(potential_module, "__path__"):
            return self.__load_multiple_modules(potential_module)
        elif isinstance(potential_module, types.ModuleType):
            return [potential_module]
        else:
            self.__raise_module_error()

    def __load_multiple_modules(self, package):
        # type: (types.ModuleType) -> List[types.ModuleType]
        """
        See Also:
            - http://stackoverflow.com/a/1310912
            - http://stackoverflow.com/a/1708706
        """
        modules = []
        for loader, module, ispkg in pkgutil.iter_modules(package.__path__):
            module_name = package.__name__ + "." + module
            found_module = self.__get_module(module_name)
            modules.append(found_module)
        return modules

    @staticmethod
    def __raise_module_error():
        raise ImportError("Failed to find the package!")


class _FilterBySubclass(object):

    __LOGGER = logging.getLogger(__name__ + "._FilterBySubclass")

    def __init__(self, storage):
        # type: (_PluginStorage) -> None
        self.__storage = storage
        self.__found_classes = None
        self.__template = None

    def filter(self, template):
        # type: (type) -> List[type]
        self.__clear_search()
        self.__set_search_template(template)
        plugins = self.__filter_plugins()
        self.__log_plugin_search(plugins)
        return plugins

    def __clear_search(self):
        self.__found_classes = []
        self.__template = None

    def __set_search_template(self, template):
        # type: (type) -> None
        self.__template = template

    def __filter_plugins(self):
        # type: () -> List[type]
        for plugin in self.__storage.PLUGINS:
            self.__process_plugin(plugin)
        return self.__found_classes

    def __process_plugin(self, plugin):
        # type: (type) -> None
        for attribute_name in dir(plugin):
            attribute = getattr(plugin, attribute_name)
            self.__try_to_process_object(attribute)

    def __try_to_process_object(self, attribute):
        # type: (type) -> None
        try:
            self.__process_attribute(attribute)
        except TypeError:
            pass

    def __process_attribute(self, attribute):
        # type: (type) -> None
        if issubclass(attribute, self.__template):
            self.__found_classes.append(attribute())

    def __log_plugin_search(self, plugins):
        # type: (List[type]) -> None
        self.__LOGGER.debug("Using template: '%s'" % self.__template)
        self.__LOGGER.debug("Found: '%s'" % plugins)


class _PluginStorage(object):

    __LOGGER = logging.getLogger(__name__ + "._PluginStorage")
    PLUGINS = []  # type: List[type]
    __LOCATIONS = []  # type: List[str]
    __APPEND_COUNT = 0

    @classmethod
    def add_location(cls, location):
        # type: (str) -> None
        cls.__note_if_index_is_zero()
        cls.__LOCATIONS.append(location)
        cls.__APPEND_COUNT = cls.__APPEND_COUNT + 1

    @classmethod
    def __note_if_index_is_zero(cls):
        if cls.__APPEND_COUNT == 0:
            cls.__LOGGER.debug("Initializing _PluginStorage for first time")

    @classmethod
    def location_already_added(cls, location):
        # type: (str) -> bool
        if location in cls.__LOCATIONS:
            return True
        else:
            return False

    @classmethod
    def plugin_index(cls):
        # type: () -> int
        return cls.__APPEND_COUNT


class PluginLoader(object):

    __LOGGER = logging.getLogger(__name__ + ".PluginStorage")
    __STORAGE = _PluginStorage()

    def __init__(self):
        self.__importer = _Importer()
        self.__filter_subclass = _FilterBySubclass(self.__STORAGE)

    def add_plugin_location(self, location):
        # type: (Any) -> None
        if isinstance(location, list) or isinstance(location, set):
            self.__process_multiple_modules(location)
        else:
            self.__process_single_module(location)

    def __process_multiple_modules(self, locations):
        # type: (Union[List[str], Set[str]]) -> None
        for location in locations:
            self.__process_single_module(location)

    def __process_single_module(self, location):
        # type: (str) -> None
        if location is not None and location is not "":
            if not self.__STORAGE.location_already_added(location):
                modules = self.__importer.fetch_modules(location)
                self.__append_modules(modules)
                self.__STORAGE.add_location(location)
                self.__LOGGER.debug("Adding plugin location: %s" % location)
        else:
            self.__LOGGER.debug(
                "Received blank location! This might be an error."
            )

    def __append_modules(self, modules):
        # type: (List[object]) -> None
        for the_module in modules:
            self.__STORAGE.PLUGINS.append(the_module)

    def get_by_name(self, name):
        # type: (str, bool) -> Callable[Any, Any]
        for plugin in self.__STORAGE.PLUGINS:
            if hasattr(plugin, name):
                possible_answer = getattr(plugin, name)
                if callable(possible_answer):
                    return possible_answer
        raise ImportError("Failed to find %s!" % name)

    def get_by_class(self, template):
        # type: (type) -> List[type]
        return self.__filter_subclass.filter(template)

    @property
    def storage_index(self):
        # type: () -> int
        return self.__STORAGE.plugin_index()
