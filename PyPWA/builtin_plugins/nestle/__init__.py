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
from PyPWA.builtin_plugins.nestle import nested
from PyPWA.core.configurator import options

__author__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class NestleOptions(options.PluginsOptions):
    plugin_name = "Nestle"
    setup = nested.NestleSetup
    provides = options.PluginTypes.MINIMIZATION
    defined_function = None
    module_comment = "Nestle, a python based multinest implementation."

    default_options = {
        "prior location": "/location/to/prior.py",
        "prior name": "prior_function",
        "ndim": 1,
        "npoints": 100,
        "method": "single",
        "update interval": None,
        "npdim": None,
        "maxiter": None,
        "maxcall": None,
        "dlogz": None,
        "decline_factor": None
    }
    option_difficulties = {
        "prior location": options.OptionLevels.REQUIRED,
        "prior name": options.OptionLevels.REQUIRED,
        "ndim": options.OptionLevels.REQUIRED,
        "npoints": options.OptionLevels.OPTIONAL,
        "method": options.OptionLevels.OPTIONAL,
        "update interval": options.OptionLevels.ADVANCED,
        "npdim": options.OptionLevels.ADVANCED,
        "maxiter": options.OptionLevels.ADVANCED,
        "maxcall": options.OptionLevels.ADVANCED,
        "dlogz": options.OptionLevels.ADVANCED,
        "decline_factor": options.OptionLevels.ADVANCED
    }

    option_types = {
        "prior location": str,
        "prior name": str,
        "ndim": int,
        "npoints": int,
        "method": ["classic", "single", "multi"],
        "update interval": int,
        "npdim": int,
        "maxiter": int,
        "maxcall": int,
        "dlogz": float,
        "decline_factor": float
    }

    option_comments = {
        "prior location":
            "The path of the file containing the prior.",
        "prior name":
            "The name of the prior function.",
        "ndim":
            "Number of parameters returned by prior.",
        "npoints":
            "Number of active points.",
        "method":
            "Method to select new points.",
        "update interval":
            "Only update the new point selector every "
            "``update_interval``-th likelihood call.",
        "npdim":
            "Number of parameters accepted by prior.",
        "maxiter":
            "Maximum number of iterations.",
        "maxcall":
            "Maximum number of likelihood evaluations.",
        "dlogz":
            "If supplied, iteration will stop when the estimated "
            "contribution of the remaining prior volume to the total "
            "evidence falls below this threshold.",
        "decline_factor":
            "If supplied, iteration will stop when the weight of newly "
            "saved samples has been declining for x consecutive samples."
    }
