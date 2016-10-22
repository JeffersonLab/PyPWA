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
from PyPWA.core_libs.templates import option_templates

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

MULTINEST_FAIL = False

try:
    import pymultinest
    from PyPWA.builtin_plugins.multinest_minimization import minimization
except (ImportError, AttributeError):
    MULTINEST_FAIL = True

if not MULTINEST_FAIL:
    class MultiNestOptions(option_templates.PluginsOptionsTemplate):

        def _plugin_name(self):
            return "MultiNest"

        def _plugin_interface(self):
            return minimization.MultiNest

        def _plugin_type(self):
            return self._minimization

        def _user_defined_function(self):
            function = """\
def the_prior(cube, ndim, nparams):
    for index in range(ndim):
        cube[index] = numpy.cos(cube[index] / 2.)
            """
            return self._build_function("numpy", function)

        def _default_options(self):
            return {
                "prior location": "/path/to/function.py",
                "prior name": "the_prior",
                "number of parameters": ""
            }

        def _option_levels(self):
            return {
                "prior location": self._required,
                "prior name": self._required,
                "number of parameters": self._required
            }

        def _option_types(self):
            return {
                "prior location": str,
                "prior name": str,
                "number of parameters": int
            }

        def _main_comment(self):
            return "A full parameter space minimizer."

        def _option_comments(self):
            return {
                "prior location": "The location of the prior function "
                                  "file.",
                "prior name": "The name of the prior function.",
                "number of parameters": "The number of parameters."
            }
