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
Required objects to define a plugin.
------------------------------------
Here we have all the objects and interfaces that are necessary to define a
plugin to be used with the configurator plugin.

- Types - Enumeration of the supported plugin types.
  - KERNEL_PROCESSING - A plugin that takes a kernel of code with data
    then distributes that code and data across nodes.
  - OPTIMIZER - Minimizer or Maximizer.
  - DATA_READER - this is a plugin that will iterate over events instead of
    parsing all the data into the memory.
  - DATA_PARSER - this should interact with all data being stored inside the
    memory.
  - SKIP - Shouldn't be loaded, skipped, used for debug.

- Levels - Enumeration of the difficulty and necessity of an option.
  - Required - An option that has to be given to the plugin, and can not be
    calculated in any way from the program.
  - Optional - An option that doesn't require a deep understanding of the
    plugin in order to utilize, but isn't required to be provided if it can
    be calculated otherwise.
  - Advanced - An option that can be calculated or determined internally,
    and required a deep understanding of the plugin.

- Setup - This is the object that would be nested inside your root plugin
  module. This should take a configuration CommandOptions, and use it to
  setup the plugin to be used throughout the program.
  .. see also:
     PyPWA.core.configuration.option_tools.CommandOptions

- Base - This is the base object for all plugins and mains, though you
  shouldn't use this unless you know what you are doing. Instead you should
  use Plugin or Main.

- Plugin - The interface to define the metadata for Plugins.

- Main - The interface to define the metadata for mains, this is essentially
  the beginning of a program.

- FileBuilder - This is the object that needs to be extended and filled out
  if your plugin needs a function to be defined for it to be usable.
"""

from typing import Dict
from typing import Union

import enum

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Types(enum.Enum):
    KERNEL_PROCESSING = 1
    OPTIMIZER = 2
    DATA_READER = 3
    DATA_PARSER = 4
    SKIP = 5


class Levels(enum.Enum):
    REQUIRED = 1
    OPTIONAL = 2
    ADVANCED = 3


class Setup(object):

    def return_interface(self):
        """
        This should return the initialized plugin or main using the
        CommandOptions that would be received via the __init__

        :return: The initialized plugin or main.
        """
        raise NotImplementedError


class Base(object):

    plugin_name = "BASE"  # type: str
    # the options coupled with their default values
    default_options = {}  # type: Dict[str, str]
    # the option and their types. See official documentation.
    option_types = {}  # type: Dict[str, Types]
    module_comment = "BASE"  # type: str
    # A short comment about each option.
    option_comments = {}  # type: Dict[str, str]
    # The options and their Levels.
    option_difficulties = {}  # type: Dict[str,Levels]
    # The defined functions if needed.
    defined_function = None  # type: Union[None, FileBuilder]
    # The setup object
    setup = Setup  # type: Setup


class Plugin(Base):
    provides = Types.SKIP  # type: Types


class Main(Base):
    required_plugins = []  # type: [Types]


class FileBuilder(object):
    imports = set()
    functions = []
