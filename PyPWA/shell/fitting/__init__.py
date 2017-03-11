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
This line is green in PyCharm, however in Github its blue.
"""

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core.configurator import options
from PyPWA.shell.fitting import main

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ShellFitting(options.Main):

    def _user_defined_function(self):
        return self._build_function("numpy", """\

def processing_function(the_array, the params):
    pass

def setup_function():
    pass

        """)

    def _shell_id(self):
        return "shell fitting method"

    def _default_options(self):
        return {
            "likelihood type": "likelihood",
            "generated length": 10000,
            "function's location": "/path/to/the/function.py",
            "processing name": "processing_function",
            "setup name": "setup_function",
            "qfactor location": "/path/to/the/data.csv",
            "data location": "/path/to/the/data.csv",
            "accepted monte carlo location": "/path/to/monte/carlo.csv",
            "save name": "output"
        }

    def _option_levels(self):
        return {
            "likelihood type": self._required,
            "generated length": self._optional,
            "function's location": self._required,
            "processing name": self._required,
            "setup name": self._required,
            "qfactor location": self._optional,
            "data location": self._required,
            "accepted monte carlo location": self._optional,
            "save name": self._required
        }

    def _option_types(self):
        return {
            "likelihood type": ["likelihood", "chi-squared"],
            "generated length": int,
            "function's location": str,
            "processing name": str,
            "setup name": str,
            "qfactor location": str,
            "data location": str,
            "accepted monte carlo location": str,
            "save name": str
        }

    def _module_comment(self):
        return "The General Shell, a simple multiprocessing enabled " \
               "data analysis tool."

    def _option_comments(self):
        return {
            "likelihood type":
                "The type of likelihood to calculate with, possible "
                "values are 'likelihood' and 'chi-squared'",
            "generated length": "The length of the generated data.",
            "function's location":
                "The location of the file that holds your defined "
                "functions.",
            "processing name": "The name of your main function.",
            "setup name": "The name of your setup function",
            "qfactor location": "The location of the qfactors.",
            "data location": "The location of your data.",
            "accepted monte carlo location":
                "The location to your accepted monte carlo",
            "save name": "The name out the output files."
        }

    def _main_type(self):
        return self._shell_main

    def _requires_data_parser(self):
        return True

    def _requires_data_reader(self):
        return False

    def _requires_kernel_processing(self):
        return True

    def _requires_minimization(self):
        return True

    def _interface_object(self):
        return main.Fitting
