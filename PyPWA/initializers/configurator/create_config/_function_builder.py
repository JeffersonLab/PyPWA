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
Writer for Example Functions
----------------------------

- _GetFunctionLocation - Takes the configuration file location then derives
  a function file location using the same name.

- _FunctionStorage - a simple object used for passing around data about the
  imports and functions.

- _BuildStorage - Takes the plugin list and uses it to populate the
  _FunctionStorage object.

- _FileBuilder - takes all the storage object and uses it to build the actual
  text file that is to be written to disk.

- _FileWriter - A simple object that takes the file and function location and
  writes the rendered functions to disk.

- FunctionHandler - The main object to interact with to generate a functions
  file.
"""

from typing import List

from PyPWA import Path, AUTHOR, VERSION
from PyPWA.initializers.configurator import options
from PyPWA.initializers.configurator.create_config import _metadata

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _GetFunctionLocation(object):

    def __init__(self):
        self.__function_location = None  # type: Path

    def process_location(self, configuration_location):
        # type: (Path) -> None
        self.__function_location = Path(configuration_location.stem + ".py")

    @property
    def function_location(self):
        # type: () -> Path
        return self.__function_location


class _FunctionStorage(object):

    def __init__(self):
        self.imports = set()
        self.functions = []


class _BuildStorage(object):

    def __init__(self):
        self.__storage = _FunctionStorage()
        self.__plugin_list = None

    def process_plugin_list(self, plugin_list):
        # type: (_metadata.GetPluginList) -> None
        self.__plugin_list = plugin_list
        self.__process_program()
        self.__process_components()

    def __process_program(self):
        if isinstance(self.__plugin_list.program, options.HasUserFunction):
            self.__process_function(self.__plugin_list.program)

    def __process_components(self):
        for component in self.__plugin_list.components:
            if isinstance(component, options.HasUserFunction):
                self.__process_function(component)

    def __process_function(self, component):
        # type: (options.HasUserFunction) -> None
        self.__add_imports(component.get_predefined_function().imports)
        self.__add_function(component.get_predefined_function().functions)

    def __add_imports(self, imports):
        # type: (List[str]) -> None
        for the_import in imports:
            self.__storage.imports.add(the_import)

    def __add_function(self, functions):
        # type: (List[str]) -> None
        for the_function in functions:
            self.__storage.functions.append(the_function)

    @property
    def storage(self):
        # type: () -> _FunctionStorage
        return self.__storage


class _FileBuilder(object):

    def __init__(self):
        self.__imports = None  # type: List[str]
        self.__functions = None  # type: List[str]
        self.__file = None  # type: str

    def build(self, storage):
        # type: (_FunctionStorage) -> None
        self.__file = ""
        self.__process_imports(storage)
        self.__process_functions(storage)
        self.__render_imports()
        self.__render_functions()

    def __process_imports(self, storage):
        # type: (_FunctionStorage) -> None
        self.__imports = sorted(storage.imports)

    def __process_functions(self, storage):
        # type: (_FunctionStorage) -> None
        self.__functions = sorted(storage.functions)

    def __render_imports(self):
        for the_import in self.__imports:
            self.__file += "import %s\n" % the_import

    def __render_functions(self):
        for the_function in self.__functions:
            self.__file += "\n" + the_function
        self.__file += "\n"

    @property
    def functions_file(self):
        # type: () -> str
        return self.__file


class _FileWriter(object):

    @staticmethod
    def write_file(file_location, file_data):
        # type: (Path, str) -> None
        with open(str(file_location), "w") as stream:
            stream.write(file_data)


class FunctionHandler(object):

    def __init__(self):
        self.__file_location = _GetFunctionLocation()
        self.__builder = _FileBuilder()
        self.__writer = _FileWriter()
        self.__storage = _BuildStorage()

    def output_functions(self, plugin_list, configuration_location):
        # type: (_metadata.GetPluginList, Path) -> None
        self.__file_location.process_location(configuration_location)
        self.__storage.process_plugin_list(plugin_list)
        self.__builder.build(self.__storage.storage)
        self.__writer.write_file(
            self.__file_location.function_location,
            self.__builder.functions_file
        )
