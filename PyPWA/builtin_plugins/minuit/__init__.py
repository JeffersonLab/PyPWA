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

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.configurator import options
from PyPWA.builtin_plugins.minuit import minimization
from PyPWA.builtin_plugins.minuit import _setup

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class MinuitOptions(options.Plugin):
    plugin_name = "Minuit"
    setup = _setup.MinuitSetup
    provides = options.Types.MINIMIZATION
    defined_function = None
    module_comment = "Minuit is the tried and tested minimizer."

    default_options = {
        "parameters": ["A1", "A2", "A3"],
        "settings": {"A1": 1, "fix_A1": True},
        "strategy": 1,
        "number of calls": 10000
    }

    option_difficulties = {
        "parameters": options.Levels.REQUIRED,
        "settings": options.Levels.REQUIRED,
        "strategy": options.Levels.OPTIONAL,
        "number of calls": options.Levels.ADVANCED
    }

    option_types = {
        "parameters": list,
        "settings": dict,
        "strategy": int,
        "number of calls": int
    }

    option_comments = {
        "parameters":
            "The parameters used inside your settings and your function",
        "settings":
            "The settings for iMinuit's fitting. See iMinuit documentation",
        "strategy":
            "The strategy of Minuit. 0 for fast, 1 default, 2 for accurate",
        "number of calls":
            "The suggested max number of calls for the fit."
    }
