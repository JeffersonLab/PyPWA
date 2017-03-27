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
import logging
import re

from ruamel.yaml import comments

from PyPWA import AUTHOR, VERSION
from PyPWA.core.configurator import options

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class CommandOptions(object):

    __logger = logging.getLogger("CommandOptions." + __name__)

    def __init__(self, plugin_options):
        self.__logger.addHandler(logging.NullHandler())
        self.__set_variables(plugin_options)

    def __set_variables(self, plugin_options):
        for key in list(plugin_options.keys()):
            name = self.__find_variable_name(key)
            setattr(self, name, plugin_options[key])

    def __find_variable_name(self, key):
        underscored_name = key.replace(" ", "_")
        lowercase_name = underscored_name.lower()
        filtered_name = re.sub(r'[^a-z0-9_]', '', lowercase_name)
        self.__logger.debug("Converted {0} to {1}".format(key, filtered_name))
        return filtered_name


class ProcessOptions(object):

    __options = None  # type: options.Base()
    __built_options = None  # type: comments.CommentedMap
    __required = None  # type: dict
    __optional = None  # type: dict
    __advanced = None  # type: dict

    def __init__(self, option_object):
        self.__options = option_object
        self.__set_header_into_built_options()
        self.__set_content_into_built_options()
        self.__set_difficulties()

    def __set_header_into_built_options(self):
        header = comments.CommentedMap()
        header.yaml_add_eol_comment(
            self.__options.module_comment, self.__options.plugin_name
        )
        self.__built_options = header

    def __set_content_into_built_options(self):
        content = comments.CommentedMap()
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


class PluginNameConversion(object):
    __NAMES = [
        # Internal name, External Name
        [options.Types.DATA_PARSER, "Data Parsing"],
        [options.Types.DATA_READER, "Data Iterator"],
        [options.Types.KERNEL_PROCESSING, "Kernel Processor"],
        [options.Types.OPTIMIZER, "Optimizer"]
    ]

    def internal_to_external(self, plugin_type):
        for internal_name, external_name in self.__NAMES:
            if internal_name == plugin_type:
                return external_name

    def external_to_internal(self, plugin_type):
        for internal_name, external_name in self.__NAMES:
            if external_name == plugin_type:
                return internal_name
