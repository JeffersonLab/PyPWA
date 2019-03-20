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
PyFit, LikelihoodFitting, and ChiSquaredFitting
-----------------------------------------------
PyFit is a simple fitting tool that can use multiple processes depending on
the processing module that is picked.

- likelihoods - the various builtin likelihoods the PyFit supports.

- _processing_interface - PyFits interface with the processing package, also
  handles the output mechanism in a second thread.

- interfaces - the interfaces that need to be extended to define a new
  likelihood function.

- initial_setup - how the configurator package interfaces the PyFit
  Main object.

- pyfit - the main object and the likelihood loading object are contained.
"""

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION
