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
from PyPWA.core.templates import option_templates
from PyPWA.builtin_plugins.nestle import nested

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class NestleOptions(option_templates.PluginsOptionsTemplate):
    def _plugin_name(self):
        return "Nestle"

    def _plugin_interface(self):
        return nested.NestledSampling

    def _plugin_type(self):
        return self._minimization

    def _user_defined_function(self):
        return None

    def _default_options(self):
        return {
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

    def _option_levels(self):
        return {
            "prior location": self._required,
            "prior name": self._required,
            "ndim": self._required,
            "npoints": self._optional,
            "method": self._optional,
            "update interval": self._advanced,
            "npdim": self._advanced,
            "maxiter": self._advanced,
            "maxcall": self._advanced,
            "dlogz": self._advanced,
            "decline_factor": self._advanced
        }

    def _option_types(self):
        return {
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

    def _module_comment(self):
        return "Nestle, a python based multinest implementation."

    def _option_comments(self):
        return {
            "prior location":
                "The path of the file containing the prior.",
            "prior name":
                "The name of the prior function.",
            "ndim":
                "Number of parameters returned by prior and accepted by "
                "loglikelihood.",
            "npoints":
                "Number of active points. Larger numbers result in a more "
                "finely sampled posterior (more accurate evidence), "
                "but also a larger number of iterations required to "
                "converge.",
            "method":
                "Method to select new points. Options are classic, "
                "single-ellipsoidal (single), and multi-ellipsoidal (multi)",
            "update interval":
                "Only update the new point selector every "
                "``update_interval``-th likelihood call. Update intervals "
                "larger than 1 can be more efficient when the likelihood "
                "function is very fast, particularly when using the "
                "multi-ellipsoid method.",
            "npdim":
                "Number of parameters accepted by prior. This might differ "
                "from *ndim* in the case where a parameter of loglikelihood "
                "is dependent upon multiple independently distributed "
                "parameters, some of which may be nuisance parameters.",
            "maxiter":
                "Maximum number of iterations. Iteration may stop earlier "
                "if termination condition is reached.",
            "maxcall":
                "Maximum number of likelihood evaluations. Iteration may "
                "stop earlier if termination condition is reached.",
            "dlogz" :
                "If supplied, iteration will stop when the estimated "
                "contribution of the remaining prior volume to the total "
                "evidence falls below this threshold. Explicitly, "
                "the stopping criterion is "
                "``log(z + z_est) - log(z) < dlogz`` where *z* is the "
                "current evidence from all saved samples, and *z_est* is "
                "the estimated contribution from the remaining volume. This "
                "option and decline_factor are mutually exclusive.",
            "decline_factor":
                "If supplied, iteration will stop when the weight ("
                "likelihood times prior volume) of newly saved samples has "
                "been declining for ``decline_factor * nsamples`` "
                "consecutive samples. A value of 1.0 seems to work pretty "
                "well. This option and dlogz are mutually exclusive."
        }
