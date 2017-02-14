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

import PyPWA
from PyPWA.core.templates import option_templates
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = [
    "Mark Jones",
    "jp. @ Stack Overflow",
    "unutbu @ Stack Overflow"
]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class PluginLoading(object):

    _logger = logging.getLogger(__name__)
    _options_template = None  # type: option_templates._CoreOptionsParsing()

    def __init__(self, template):
        self._logger.addHandler(logging.NullHandler())
        self._options_template = template

    def fetch_plugin(self, plugin_list):
        potential_plugins = []
        for the_file in plugin_list:
            if self._is_str(the_file):
                # Appends the directory containing the
                sys.path.append(
                    os.path.dirname(os.path.abspath(the_file))
                )

                module = importlib.import_module(
                    # Extracts the filename from the path provided
                    os.path.splitext(os.path.basename(the_file))[0]
                )

                potential_plugins.append(self._find_libs(module))
            elif self._is_module(the_file):
                potential_plugins.append(self._find_libs(the_file))

        flattened_potential = []
        for list_of_plugins in potential_plugins:
            for plugin in list_of_plugins:
                flattened_potential.append(plugin)

        plugins = self._extract_options_object(flattened_potential)

        return plugins

    @staticmethod
    def _is_empty(the_file):
        if the_file == "" or isinstance(the_file, type(None)):
            return True
        else:
            return False

    @staticmethod
    def _is_str(the_file):
        if isinstance(the_file, str):
            return True
        else:
            return False

    @staticmethod
    def _is_module(the_file):
        if isinstance(the_file, type(PyPWA)):
            return True
        else:
            return False

    @staticmethod
    def _is_list(var):
        if isinstance(var, list):
            return True
        else:
            return False

    def _find_libs(self, module):
        """
        Takes a package, finds all sub modules, then imports the
        submodules and returns those submodules.

        Args:
            module: The initial module.

        Returns:
            list[module]: The list of submodules.
        """
        libs = []
        for module_name in self._list_of_submodules(module):
            libs.append(
                importlib.import_module(
                    module.__name__ + "." + module_name
                )
            )
        return libs

    @staticmethod
    def _list_of_submodules(module):
        """
        See Also:
            http://stackoverflow.com/a/1310912
            http://stackoverflow.com/a/1708706
        """
        # Should make a list of:
        # [ ImporterInstance, name of module, is a package ]
        names = []
        for loader, name, is_loaded in pkgutil.iter_modules(module.__path__):
            names.append(name)
        # Credit to unutbu and jp. for the discovery of how pkgutil works.
        return names

    def _extract_options_object(self, modules_list):
        plugin_initializer = []

        for plugin in modules_list:

            self._logger.info(
                "Found the following modules: \n{0}".format(repr(plugin))
            )

            for object_name in dir(plugin):
                the_object = getattr(plugin, object_name)
                try:
                    if issubclass(the_object, self._options_template):
                        plugin_initializer.append(the_object)
                except TypeError:
                    pass

        return plugin_initializer
    

class PythonSheetLoader(object):

    _logger = logging.getLogger(__name__)
    _function_file = None  # type: str
    _module = None  # type: type(PyPWA)

    def __init__(self, function_file):
        self._logger.addHandler(logging.NullHandler())
        self._set_function_file(function_file)
        self._load_module()

    def _set_function_file(self, function_file):
        self._function_file = function_file

    def _load_module(self):
        self._append_path()
        self._set_module()

    def _append_path(self):
        sys.path.append(self._get_function_path())

    def _get_function_path(self):
        absolute_path = os.path.abspath(self._function_file)
        path_without_basename = os.path.dirname(absolute_path)
        return path_without_basename

    def _set_module(self):
        module = self._get_module()
        self._check_module(module)
        self._module = module

    def _get_module(self):
        try:
            return importlib.import_module(self._get_function_file_name())
        except Exception as Error:
            self._process_module_error(Error)

    def _get_function_file_name(self):
        basename = os.path.basename(self._function_file)
        filename, extension = os.path.splitext(basename)
        return filename

    def _process_module_error(self, error):
        self._logger.exception(error)
        raise error

    def _check_module(self, module):
        if self._module_is_empty(module):
            self._raise_module_error()

    @staticmethod
    def _module_is_empty(module):
        if isinstance(module, type(None)):
            return True
        else:
            return False

    def _raise_module_error(self):
        error_string = "{0} not found!", self._get_function_file_name()

        self._logger.error(error_string)
        raise ImportError(error_string)

    def fetch_function(self, function_name, fail=False):
        try:
            return self._extract_function(function_name)
        except Exception as Error:
            if fail:
                raise Error
            else:
                return self._empty_function()

    def _extract_function(self, function_name):
        return getattr(self._module, function_name)

    @staticmethod
    def _empty_function():
        def empty():
            pass
        return empty