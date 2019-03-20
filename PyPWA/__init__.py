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
General Docs
============

PyPWA is statistical analysis toolkit that was built with Partial Wave
Analysis in mind, however you should be able to use the tools included for
anything statistical analysis.

Currently there are 4 different applications defined inside this package:

- PyFit - Fitting with any likelihood.

- PyLikelihood - Fitting with the log-likelihood.

- PyChiSquared - Fitting with the ChiSquared likelihood.

- PySimulate - Simulation of an amplitude.

- PyIntensities - Just the calculation half of PySimulate.

- PyRejection - Just the rejection-method half of PySimulate.

For information about how to use each of the programs, look in the docs folder
included with the source code, or check the user docs at ReadTheDocs.io.

Developer Docs
==============

To attempt to achieve a flexible fitter that could be quickly adapted to
changing needs, we actually built the entire package around a generalized
plugin loader. The "main" objects ore defined as plugins, along with each
task that needed to be solved. This means that fitting, data loading,
the processing module, simulation, optimizers, etc are all defined as
plugins internally.

Package purposes
----------------

- builtin_plugins - This is where each included plugins are defined, the
  optimizers, the processing module, the builtin parser, and iterators are
  all defined here.

- entries - The various entry points for each program contained in this
  package are here, each function defined here is a starting point for
  setuptools.

- initializers - This is where the loaders for the programs are defined, this
  either processes and setups the arguments or a configuration file to load
  and send the needed plugins to the main objects.

- libs - The main libraries for the program. Core file libs, interfaces,
  and mathematics are defined here.

- progs - This is where the various programs are defined that are provided by
  PyPWA.

For more information on how each module works, view their documentation
respectively.
"""


__author__ = "PyPWA Team and Contributors"
__credits__ = ["Mark Jones"]
__version__ = "3.0.0.dev"


LICENSE = "GPLv3"
STATUS = "development"
MAINTAINER = "Mark Jones"
AUTHOR = __author__
VERSION = __version__

import sys

if sys.version_info[0:2] < (3, 5):
    from pathlib2 import Path, PurePath
else:
    from pathlib import Path, PurePath

if sys.version_info.major == 2:
    import Queue as queue
else:
    import queue

