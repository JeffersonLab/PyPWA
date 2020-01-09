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
******************
How to get started
******************

To make using PyPWA easier from IPython or Jupyter, useful modules have
been imported directly into this package so that you can get up and
running as quickly as possible. To know more about the following modules,
use help.

Working with data:
 - get_reader, get_writer: Returns an object that can read/write data
    one event at a time.
 - read, write: Reads/Writes data to and from memory
 - ProjectDatabase: Handles operating with HD5 tables. This is the
    method used inside PyPWA to bin data, or operate on larger-than-memory
    data.

Programs:
 - monte_carlo_simulation: Simulates data using the Monte Carlo Rejection
    method.

Complex Data Types:
 - FourVector ThreeVector Particle ParticlePool: Handles working
    with particle data.

General Docs
============

PyPWA is statistical analysis toolkit that was built with Partial Wave
Analysis in mind, however you should be able to use the tools included for
anything statistical analysis.

Currently there are 4 different applications defined inside this package:

- pyfit - Fitting with any likelihood.
- pysimulate - Monte-Carlo something or the other.
- pymask  - Simple masking and conversion of data
- pybin - Multi-Variable binning utility utilizing PyTables

For information about how to use each of the programs, look in the docs
folder included with the source code, or check the user docs at
ReadTheDocs.io.

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

- plugins - Plug and play functionality for PyPWA. These are modular
    metadata based plugins that can be user defined to add support for
    new data types and likelihoods for pypwa.

- libs - The main libraries for the program. Core file libs, interfaces,
    and mathematics are defined here. If you're writing a script to
    interface with PyPWA, this will be the package you'll want to use.

- progs - This is where the various shell programs that PyPWA provides
    are defined. These programs can also be used as an example on how
    their respective lib component is used.

For more information on how each package works, view their documentation.
"""

from PyPWA import info as _info
from PyPWA.libs.binning import bin_by_range
from PyPWA.libs.file import (
    get_reader, get_writer, read, write, ProjectDatabase
)
from PyPWA.libs.fit import (
    minuit, ChiSquared, LogLikelihood, EmptyLikelihood, AbstractAmplitude,
    FunctionAmplitude
)
from PyPWA.libs.plotting import make_lego
from PyPWA.libs.resonance import ResonanceData
from PyPWA.libs.simulate import monte_carlo_simulation
from PyPWA.libs.vectors import FourVector, ThreeVector, ParticlePool, Particle

__all__ = [
    "FourVector", "ThreeVector", "Particle", "ParticlePool",
    "get_writer", "get_reader", "read", "write", "ProjectDatabase",
    "monte_carlo_simulation", "minuit", "ChiSquared", "LogLikelihood",
    "EmptyLikelihood", "AbstractAmplitude", "FunctionAmplitude",
    "ResonanceData", "bin_by_range", "make_lego"
]

__author__ = _info.AUTHOR
__credits__ = ["Mark Jones"]
__version__ = _info.VERSION
__release__ = _info.RELEASE
__license__ = _info.LICENSE
