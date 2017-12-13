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


from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator import options
from PyPWA.libs.components.optimizers import (
    _plugin_fetcher, opt_plugins
)

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class OptimizerConf(
    options.Component, options.HasUserFunction, options.HasChoices
):

    def __init__(self):
        self.name = "Optimizer"
        self.choice_type = "Optimizers"
        self.module_comment = "Handles function optimizer interaction with " \
                              "the package"

        self.__optimizer_fetcher = _plugin_fetcher.OptimizerFetcher()

        self.choices = self.__optimizer_fetcher.get_list_of_plugins()
        self.__choice = _plugin_fetcher.AllOptions()


    def set_choice(self, optimizer_selected):
        # type: (str) -> None
        self.__choice = self.__optimizer_fetcher.get_optimizer_by_name(
            optimizer_selected
        )

    def get_default_options(self):
        return {
            "parameters": ["A1", "A2", "A3"],
            "selected optimizer": self.__choice.name,
            "configuration": self.__choice.get_defaults()
        }

    def get_option_difficulties(self):
        return {
            "parameters": options.Levels.REQUIRED,
            "selected optimizer": options.Levels.REQUIRED,
            "configuration": self.__choice.get_difficulties()
        }

    def get_option_types(self):
        return {
            "parameters": list,
            "selected optimizer": str,
            "configuration": self.__optimizer_fetcher.get_plugin_types()
        }

    def get_option_comments(self):
        return {
            "parameters":
                "The parameters used inside your settings and your function",
            "selected optimizers": "Your choice of optimizer",
            "configuration": "Configuration for the optimizer"
        }

    def get_predefined_function(self):
        if isinstance(self.__choice, opt_plugins.HasPrior):
            return self.__choice.get_prior_function_template()
        else:
            return options.FileBuilder()
