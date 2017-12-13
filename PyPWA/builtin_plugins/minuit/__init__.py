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
Python Minimization with with Iminuit
-------------------------------------
This optimizer will try to find the nearest local minima in the function
provided using the settings that it was configured with.

To understand how to use the minimzer, read iminuit's documentation online.
"""


from PyPWA import AUTHOR, VERSION
from PyPWA.libs.components.optimizers import opt_plugins
from PyPWA.builtin_plugins.minuit import minimization

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class MinuitOptimizer(opt_plugins.OptimizerConf):

    def __init__(self):
        self.name = "minuit"
        self.optimizer_summary = "Minuit is the tried and tested minimizer."

    def get_optimizer_type(self):
        return opt_plugins.Type.MINIMIZER

    def get_optimizer_parser(self):
        return minimization.ParserObject()

    def get_optimizer(self):
        return minimization.Minuit()

    def get_defaults(self):
        return {
            "settings": {"A1": 1, "fix_A1": True},
            "strategy": 1,
            "number of calls": 10000
        }

    def get_difficulties(self):
        return {
            "settings": opt_plugins.Levels.REQUIRED,
            "strategy": opt_plugins.Levels.OPTIONAL,
            "number of calls": opt_plugins.Levels.ADVANCED
        }

    def get_types(self):
        return {
            "settings": dict,
            "strategy": int,
            "number of calls": int
        }

    def get_option_comments(self):
        return {
            "parameters":
                "The parameters used inside your settings and your function",
            "settings":
                "The settings for iMinuit's fit. See iMinuit documentation",
            "strategy":
                "The strategy of Minuit. 0 for fast, 1 default, 2 for "
                "accurate",
            "number of calls":
                "The suggested max number of calls for the fit."
        }
