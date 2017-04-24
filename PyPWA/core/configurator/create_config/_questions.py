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

"""

from PyPWA.core.configurator import options
from PyPWA.core.configurator import option_tools
from PyPWA.core.configurator.create_config import _input_loop

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class GetPluginLevel(_input_loop.QuestionLoop):

    _default_answer = "optional"
    _possible_answers = ["required", "optional", "advanced"]
    _question = """
How much control would you like to have over the configuration? 
required
optional (default, recommended)
advanced

[optional]: """

    def ask_for_plugin_level(self):
        self._question_loop()

    def get_plugin_level(self):
        if self._answer is "required":
            return options.Levels.REQUIRED
        elif self._answer is "optional":
            return options.Levels.OPTIONAL
        elif self._answer is "advanced":
            return options.Levels.ADVANCED
        else:
            raise ValueError("Unknown answer '%s'" % self._answer)


class GetPluginDirectory(_input_loop.QuestionLoop):

    _question = """
Would you like to use your own plugins? If so enter the path to your plugins
[None]: """

    _default_answer = "None"

    def ask_for_plugin_directory(self):
        self._question_loop()

    def get_plugin_directory(self):
        if self._answer is "None":
            return None
        else:
            return self._answer


class GetSaveLocation(_input_loop.QuestionLoop):

    _question = """
What would you like to name the configuration file?
File Name?: """

    __override = False

    def ask_for_save_location(self):
        self._question_loop()

    def override_save_location(self, save_location):
        self.__override = save_location

    def get_save_location(self):
        if self.__override:
            return self.__override
        else:
            return self._answer


class GetSpecificPlugin(_input_loop.QuestionLoop):

    __name_conversion = option_tools.PluginNameConversion()

    def ask_for_plugin(self, plugin_list, plugin_type):
        self.__set_possible_answers(plugin_list)
        self.__create_question(plugin_type)
        self._question_loop()

    def __set_possible_answers(self, plugin_list):
        self._possible_answers = []
        for plugin in plugin_list:
            self._possible_answers.append(plugin.plugin_name)

    def __create_question(self, plugin_type):
        self._question = self.__make_base_string(plugin_type)
        self._question += self.__make_name_list_string()
        self._question += "\nPlugin?: "

    def __make_base_string(self, plugin_type):
        clean_type = self.__name_conversion.internal_to_external(plugin_type)
        return "Which plugin would you like to use for '%s'?" % clean_type

    def __make_name_list_string(self):
        name_string = ""
        for name in self._possible_answers:
            name_string += "\n%s" % name
        return name_string

    def get_specific_plugin(self):
        return self._answer
