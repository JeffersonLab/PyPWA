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

import importlib
import logging
import os
import pkgutil
import sys

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

    __logger = logging.getLogger(__name__ + "._AppendPath")

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())

    def append_path(self, filename):
        function_path = self.__get_function_path(filename)
        self.__log_path(function_path)
        sys.path.append(function_path)

    @staticmethod
    def __get_function_path(filename):
        absolute_path = os.path.abspath(filename)
        path_without_basename = os.path.dirname(absolute_path)
        return path_without_basename

    def __log_path(self, path):
        self.__logger.info("Adding %s to the path." % path)

        
class _Importer(object):

    __logger = logging.getLogger(__name__ + "._Importer")
    __path_handler = _AppendPath()

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())

    def fetch_modules(self, package):
        found_module = self.__load_module(package)
        return self.__process_module(found_module)

    def __load_module(self, package):
        if isinstance(package, types.ModuleType):
            return package
        else:
            return self.__import_module(package)

    def __import_module(self, package):
        self.__path_handler.append_path(package)
        name = self.__get_module_name(package)
        return self.__get_module(name)

    @staticmethod
    def __get_module_name(package):
        file_name = os.path.basename(package)
        module_name = os.path.splitext(file_name)[0]
        return module_name
        
    def __get_module(self, package):
        try:
            return importlib.import_module(package)
        except Exception as Error:
            self.__process_module_error(Error)

    def __process_module_error(self, error):
        self.__logger.exception(error)

    def __process_module(self, module):
        if hasattr(module, "__path__"):
            return self.__load_multiple_modules(module)
        elif isinstance(module, types.ModuleType):
            return [module]
        else:
            self.__raise_module_error()

    def __load_multiple_modules(self, package):
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

    __logger = logging.getLogger(__name__ + "._FilterBySubclass")

    __plugins = None
    __classes = None
    __template = None

    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())

    def filter(self, plugins, template):
        self.__classes = []
        self.__plugins = plugins
        self.__template = template
        plugins = self.__filter_plugins()
        self.__log_plugin_search(plugins)
        return plugins
        
    def __filter_plugins(self):
        for plugin in self.__plugins:
            self.__process_plugin(plugin)
        return self.__classes

    def __process_plugin(self, plugin):
        for attribute_name in dir(plugin):
            attribute = getattr(plugin, attribute_name)
            self.__try_to_process_object(attribute)

    def __try_to_process_object(self, attribute):
        try:
            self.__process_attribute(attribute)
        except TypeError:
            pass

    def __process_attribute(self, attribute):
        if issubclass(attribute, self.__template):
            self.__classes.append(attribute)

    def __log_plugin_search(self, plugins):
        self.__logger.debug("Using template: %s" % self.__template)
        self.__logger.debug("Found: %s" % plugins)


class PluginStorage(object):

    __importer = _Importer()
    __logger = logging.getLogger(__name__ + ".PluginStorage")
    __filter_subclass = _FilterBySubclass()

    __plugins = None  # type: [types.ModuleType]
    
    def __init__(self):
        self.__logger.addHandler(logging.NullHandler())
        self.__plugins = []

    def add_plugin_location(self, location):
        if isinstance(location, list) or isinstance(location, set):
            self.__process_multiple_modules(location)
        else:
            self.__process_single_module(location)

    def __process_multiple_modules(self, locations):
        for location in locations:
            self.__process_single_module(location)

    def __process_single_module(self, location):
        if location is not None and location is not "":
            modules = self.__importer.fetch_modules(location)
            self.__append_modules(modules)
        
    def __append_modules(self, modules):
        for the_module in modules:
            self.__plugins.append(the_module)

    def get_by_name(self, name, fail=True):
        for plugin in self.__plugins:
            if hasattr(plugin, name):
                return getattr(plugin, name)
        if fail:
            raise ImportError
        else:
            return self.__empty_function

    @staticmethod
    def __empty_function(*args, **kwargs):
        pass

    def get_by_class(self, template):
        return self.__filter_subclass.filter(self.__plugins, template)
