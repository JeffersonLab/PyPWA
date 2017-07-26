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
Data and Function Loading for the PyShell
-----------------------------------------
- data_loader - Loads in all data for PyShell
- function_loading - loads in the users functions.
"""

from PyPWA import AUTHOR, VERSION
from PyPWA.progs.shell.loaders.data_loader.load import DataLoading
from PyPWA.progs.shell.loaders._function_loading import FunctionLoader

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
