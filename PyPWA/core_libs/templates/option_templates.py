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

"""

"""

import copy

import ruamel.yaml.comments

from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class _CoreOptionsParsing(object):

    _required = "required"
    _optional = "optional"
    _advanced = "advanced"
    _kernel_processing = "kernel processing"
    _minimization = "minimization"
    _data_reader = "data reader"
    _data_parser = "data parser"

    def __init__(self):
        if self._default_options():
            self.__processed = self.__build_options_dictionary()
            self.__req_func, self.__opt_func, \
            self.__adv_func = self.__build_leveled_dictionaries()
        else:
            self.__req_func = {}
            self.__opt_func = {}
            self.__adv_func = {}

    def _id(self):
        raise NotImplementedError

    def _default_options(self):
        raise NotImplementedError

    def _option_levels(self):
        raise NotImplementedError

    def _option_types(self):
        raise NotImplementedError

    def _main_comment(self):
        raise NotImplementedError

    def _option_comments(self):
        raise NotImplementedError

    def __build_options_dictionary(self):
        """
        Builds the dictionary with the default options and the comments
        connected to to each key.

        Returns:
            dict: The dictionary with all
                the comments and the default options.
        """
        defaults = self._default_options()

        header = ruamel.yaml.comments.CommentedMap()
        header.yaml_add_eol_comment(
            self._main_comment(), self._id()
        )

        content = ruamel.yaml.comments.CommentedMap()
        header[self._id()] = content

        for key in list(self._option_comments().keys()):
            header.yaml_add_eol_comment(
                self._option_comments()[key], key
            )

            header[self._id()][key] = defaults[key]

        return header

    def __build_leveled_dictionaries(self):
        """
        Parses the dictionary out to 3 different dictionaries. Each being
        a level of potential user requests.

        Returns:
            list[dict]: The 3 dictionaries
                that hold the data that
        """
        levels = self._option_levels()

        required = copy.deepcopy(self.__processed)
        optional = copy.deepcopy(self.__processed)
        advanced = copy.deepcopy(self.__processed)

        for key in list(levels.keys()):
            if levels[key] == self._required:
                pass
            elif levels[key] == self._optional:
                required[self._id()].pop(key)
            elif levels[key] == self._advanced:
                required[self._id()].pop(key)
                optional[self._id()].pop(key)

        return [required, optional, advanced]

    @staticmethod
    def _build_function(imports, function):
        return {"function": function, "imports": set(imports)}

    def request_options(self, level):
        return {
            "required": self.__req_func,
            "optional": self.__opt_func,
            "advanced": self.__adv_func
        }[level]

    def request_metadata(self, data):
        raise NotImplementedError


class PluginsOptionsTemplate(_CoreOptionsParsing):

    def __init__(self):
        super(PluginsOptionsTemplate, self).__init__()

    def _id(self):
        return self._plugin_name()

    def _plugin_name(self):
        raise NotImplementedError

    def _default_options(self):
        raise NotImplementedError

    def _option_levels(self):
        raise NotImplementedError

    def _option_types(self):
        raise NotImplementedError

    def _main_comment(self):
        raise NotImplementedError

    def _option_comments(self):
        raise NotImplementedError

    def _plugin_interface(self):
        raise NotImplementedError

    def _plugin_type(self):
        raise NotImplementedError

    def _user_defined_function(self):
        raise NotImplementedError

    def request_metadata(self, data):
        """

        Args:
            data (str):

        Returns:

        """
        return {
            "name": self._plugin_name(),
            "interface": self._plugin_interface(),
            "provides": self._plugin_type(),
            "user functions": self._user_defined_function()
        }[data]


class MainOptionsTemplate(_CoreOptionsParsing):

    _shell_main = "main shell"
    _gui_main = "main gui"

    def __init__(self):
        super(MainOptionsTemplate, self).__init__()

    def _id(self):
        return self._shell_id()

    def _shell_id(self):
        raise NotImplementedError

    def _default_options(self):
        raise NotImplementedError

    def _option_levels(self):
        raise NotImplementedError

    def _option_types(self):
        raise NotImplementedError

    def _main_comment(self):
        raise NotImplementedError

    def _option_comments(self):
        raise NotImplementedError

    def _main_type(self):
        raise NotImplementedError

    def _user_defined_function(self):
        raise NotImplementedError

    def request_metadata(self, data):
        """

        Args:
            data (str):

        Returns:

        """
        return {
            "id": self._shell_id(),
            "ui": self._main_type(),
            "user functions": self._user_defined_function()
        }[data]
