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

import enum
import ruamel.yaml.comments
import copy

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


class PluginsOptions(object):
    plugin_name = NotImplemented
    default_options = NotImplemented
    option_levels = NotImplemented
    option_types = NotImplemented
    module_comment = NotImplemented
    option_comments = NotImplemented
    interface = NotImplemented
    defined_function = NotImplemented
    provides = NotImplemented


class MainOptions(object):

    name = ""
    default_options = {}
    option_levels = {}
    option_types = {}
    module_comment = ""
    option_comments = {}
    user_defined_function = False
    interface_object = None
    requires_data_parser = False
    requires_kernel_processing = False
    requires_minimization = False
    requires_data_reader = False


class ProcessOptions(object):

    _module_name = None
    _module_comment = None
    _option_comments = None
    _option_types = None
    _option_defaults = None
    _option_difficulties = None

    _built_options = None
    _required = None
    _optional = None
    _advanced = None

    def __init__(
            self, module, module_comment, options_comment,
            option_types, option_defaults, option_difficulty
    ):
        self._module_name = module
        self._module_comment = module_comment
        self._option_comments = options_comment
        self._option_types = option_types
        self._option_defaults = option_defaults
        self._option_difficulties = option_difficulty

        self._set_header_into_built_options()
        self._set_content_into_built_options()
        self._set_difficulties()

    def _set_header_into_built_options(self):
        header = ruamel.yaml.comments.CommentedMap()
        header.yaml_add_eol_comment(
            self._module_comment, self._module_name
        )
        self._built_options = header

    def _set_content_into_built_options(self):
        content = ruamel.yaml.comments.CommentedMap()
        populated_content = self._add_options_defaults(content)
        commented_content = self._add_option_comments(populated_content)
        self._built_options[self._module_name] = commented_content

    def _add_options_defaults(self, content):
        for option, value in self._option_defaults.items():
            content[option] = value
        return content

    def _add_option_comments(self, content):
        for option, comment in self._option_comments.items():
            content.yaml_add_eol_comment(comment, option)
        return content

    def _set_difficulties(self):
        self._make_separate_difficulties()
        self._process_separate_difficulties()

    def _make_separate_difficulties(self):
        required = copy.deepcopy(self._built_options)
        optional = copy.deepcopy(self._built_options)
        advanced = copy.deepcopy(self._built_options)

        self._required = required
        self._optional = optional
        self._advanced = advanced

    def _process_separate_difficulties(self):
        for option, difficulty in self._option_difficulties.items():
            if difficulty == "optional":
                self._required[self._module_name].pop(option)
            elif difficulty == "advanced":
                self._required[self._module_name].pop(option)
                self._optional[self._module_name].pop(option)

    @property
    def required(self):
        return self._required

    @property
    def optional(self):
        return self._optional

    @property
    def advanced(self):
        return self._advanced
