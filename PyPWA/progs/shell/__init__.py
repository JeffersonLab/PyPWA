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
PyFit, PySimulate, and shared libraries
---------------------------------------
- fit - The package that contains PyFit
- simulate - The package that contains PySimulate
- loaders - Package that loads the data and functions for both programs
- pyshell_functions - Contains the example functions for PyFit and PySimulate
- shell types - The static typing information for the expected user's
  functions.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.progs.shell.fit import ShellFitting
from PyPWA.progs.shell.simulate import ShellSimulation

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
