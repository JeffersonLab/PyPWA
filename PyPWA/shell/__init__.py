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
============
Main Objects
============

This is where the main logic of the programs is defined. Each folder here
represents a core program and contains the main logic required for the 
program to function.

Each of the programs act as a plugin, and their metadata is stored in each 
of their __init__.py files.

- pyfit - the package that dictates how PyFit, PyLikelihood, 
  and PyChiSquared operate

- pysimulate - defines how PySimulate, PyIntensities, and PyWeighting operate.

- pyshell_functions - Defines the output functions for PyShell applications.

There is no actual core logic defined here, data loading, processing, and
optimization is all defined elsewhere, however the algorithms used to 
calculate the final values are found here.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
