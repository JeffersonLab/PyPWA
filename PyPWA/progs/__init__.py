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
Shell Modules
-------------
Here is where PyFit and PySimulate are defined for PyPWA, along with any
programs that build off of those two modules.

- fit - the package that dictates how PyFit, PyLikelihood,
  and PyChiSquared operate
- simulate - defines how PySimulate, PyIntensities, and PyWeighting operate.
- pyshell_functions - Defines the output functions for PyShell applications.
- loaders - Loads the data and functions for PyShell programs in a way that
  should work with either program.
- shell_types - Defines some static typing information for more complicated
  data types inside the shell programs.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
