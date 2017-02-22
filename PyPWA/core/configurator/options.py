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

import copy
import enum
import logging
import re

import ruamel.yaml.comments

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class PluginTypes(enum.Enum):
    KERNEL_PROCESSING = 1
    MINIMIZATION = 2
    DATA_READER = 3
    DATA_PARSER = 4


class OptionLevels(enum.Enum):
    REQUIRED = 1
    OPTIONAL = 2
    ADVANCED = 3


class Options(object):
    plugin_name = ""
    default_options = {}
    option_difficulties = {}
    option_types = {}
    module_comment = ""
    option_comments = {}
    defined_function = None


class PluginsOptions(Options):
    setup = None  # type: PyPWA.core.shared.interface.plugins
    provides = None  # type: PluginTypes


class MainOptions(Options):
    required_plugins = []  # type: [PluginTypes]


class Setup(object):

    def return_interface(self):
        raise NotImplementedError


class CommandOptions(object):

    __logger = logging.getLogger("CommandOptions." + __name__)

    def __init__(self, options):
        self.__logger.addHandler(logging.NullHandler())
        self.__set_variables(options)

    def __set_variables(self, options):
        for key in list(options.keys()):
            name = self.__find_variable_name(key)
            setattr(self, name, options[key])

    def __find_variable_name(self, key):
        underscored_name = key.replace(" ", "_")
        lowercase_name = underscored_name.lower()
        filtered_name = re.sub(r'[^a-z0-9_]', '', lowercase_name)
        self.__logger.debug("Converted {0} to {1}".format(key, filtered_name))
        return filtered_name


class ProcessOptions(object):

    __options = None  # type: Options()
    __built_options = None  # type: ruamel.yaml.comments.CommentedMap
    __required = None  # type: dict
    __optional = None  # type: dict
    __advanced = None  # type: dict

    def __init__(self, option_object):
        self.__options = option_object
        self.__set_header_into_built_options()
        self.__set_content_into_built_options()
        self.__set_difficulties()

    def __set_header_into_built_options(self):
        header = ruamel.yaml.comments.CommentedMap()
        header.yaml_add_eol_comment(
            self.__options.module_comment, self.__options.plugin_name
        )
        self.__built_options = header

    def __set_content_into_built_options(self):
        content = ruamel.yaml.comments.CommentedMap()
        populated_content = self.__add_options_defaults(content)
        commented_content = self.__add_option_comments(populated_content)
        self.__built_options[self.__options.plugin_name] = commented_content

    def __add_options_defaults(self, content):
        for option, value in self.__options.options_defaults.items():
            content[option] = value
        return content

    def __add_option_comments(self, content):
        for option, comment in self.__options.option_comments.items():
            content.yaml_add_eol_comment(comment, option)
        return content

    def __set_difficulties(self):
        self.__make_separate_difficulties()
        self.__process_separate_difficulties()

    def __make_separate_difficulties(self):
        required = copy.deepcopy(self.__built_options)
        optional = copy.deepcopy(self.__built_options)
        advanced = copy.deepcopy(self.__built_options)

        self.__required = required
        self.__optional = optional
        self.__advanced = advanced

    def __process_separate_difficulties(self):
        for option, difficulty in self.__options.options_difficulties.items():
            if difficulty == "optional":
                self.__required[self.__options.plugin_name].pop(option)
            elif difficulty == "advanced":
                self.__required[self.__options.plugin_name].pop(option)
                self.__optional[self.__options.plugin_name].pop(option)

    @property
    def required(self):
        return self.__required

    @property
    def optional(self):
        return self.__optional

    @property
    def advanced(self):
        return self.__advanced
