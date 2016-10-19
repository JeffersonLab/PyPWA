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
from PyPWA.core_libs.templates import option_templates
from PyPWA.shell.simulation import main

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class ShellSimulation(option_templates.MainOptionsTemplate):

    def _user_defined_function(self):
        return self._build_function("numpy", """\

def processing_function(the_array, the params):
    pass

def setup_function():
    pass

        """)

    def _shell_id(self):
        return "shell simulation"

    def _default_options(self):
        return {
            "the type": "full",
            "function's location": "/path/to/the/function.py",
            "processing name": "processing_function",
            "setup name": "setup_function",
            "data location": "/path/to/the/data.csv",
            "parameters": {"A1": 1, "A2": 2, "A3": 0.1, "A4": -10.0001},
            "max intensity": "2.123123",
            "save name": "output"
        }

    def _option_levels(self):
        return {
            "the type": self._required,
            "function's location": self._required,
            "processing name": self._required,
            "setup name": self._required,
            "data location": self._required,
            "parameters": self._required,
            "max intensity": self._required,
            "save name": self._required
        }

    def _option_types(self):
        return {
            "the type": ["full", "intensities", "weighting"],
            "function's location": str,
            "processing name": str,
            "setup name": str,
            "data location": str,
            "parameters": dict,
            "max intensity": float,
            "save name": str
        }

    def _main_comment(self):
        return "The General Shell, a simple multiprocessing enabled " \
               "data analysis tool."

    def _option_comments(self):
        return {
            "the type":
                "If you are seeing this, something went very wrong.",
            "function's location":
                "The location to the intensity function.",
            "processing name": "The name of the intensity function.",
            "setup name": "The name of the setup function.",
            "data location": "The path to your data.",
            "parameters": "The parameters to simulate against.",
            "max intensity":
                "The largest intensity in your entire data set",
            "save name": "The name to use for saving data."
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
        return False

    def _interface_object(self):
        return main.Simulator
