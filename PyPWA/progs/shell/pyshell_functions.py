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
Simply defines the user's functions that are shared between PyFit, PySimulate,
and their derivative programs.
"""

from PyPWA.initializers.configurator import options
from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class ShellFunctionFile(options.FileBuilder):
    imports = {"numpy"}
    functions = [
        """
def processing_function(the_array, the_params):
    # The Params is passed by your optimizer, each optimizer passes something
    # different to check with the documentation if you are unsure how to use
    # it.
    
    final_value = the_array["x"] * the_params["A1"]
    return final_value
        """,
        """
def setup_function():
    # If you have an amplitude that needs a method are function called before
    # you can begin processing, call it here.
    pass
        """
    ]
