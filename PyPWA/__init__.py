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
Welcome to PyPWA!
=================
To make using PyPWA easier from IPython or Jupyter, useful modules have
been imported directly into this package so that you can get up and
running as quickly as possible. To know more about the following modules,
use help. i.e. ? read or help(read)

Fitting and Simulation:
-----------------------
- NestedFunction: Abstract object that should be used to define whatever
    function you want to simulate or fit.
- FunctionAmplitude: Fallback for old functions for PyPWA 2.0, don't
    use unless you need.
- monte_carlo_simulation: Function used for rejection sampling.
- simulate.process_user_function: Processes the user function and returns
    the functions final values and max value.
- simulate.make_rejection_list: Takes the final values and max values to
    produce a rejection list that can be used to mask the source data.
- LogLikelihood: Sets up the log likelihood. Supports both the extended,
    binned, and standard likelihood.
- ChiSquared: Sets up the ChiSquared likelihood, supports using working
    with expected values or binned
- EmptyLikelihood: Sets up an empty likelihood. For use when you want
    to use the multiprocessing without a likelihood, or have included
    a likelihood directly into your NestedFunction.
- minuit: A wrapper around iminuit to make it easier to use with our
    likelihoods.

Reading and Writing data:
-------------------------
Note: Data can be loaded and writen with Pandas or Numpy if preferred,
    however, read and write support caching which can make subsequent
    reads significantly quicker. You can use the caching module separately
    though if preferred.
- read: Reads data from a file or path
- write: Writes data from a file or path
- DataType: Enum to select type for get_writer and get_reader
- get_writer: Returns an object that supports writing one event at a time
- get_reader: Returns an object that supports reading one event at a time
- ProjectDatabase: A numerical database based off of HDF5 that allows for
    working with data larger than memory. Only recommended if you have
    to use it.
- cache.read: Reads the cache for a specific source file, or for an
    intermediate step.
- cache.write: Writes the cache for a specific source file, or for an
    intermediate step.

Tools:
------
- bin_with_fixed_widths: Supports binning any dataset into a bins with
    a fixed number of events per bin
- bin_by_range: Supports binning any dataset into a fixed number of bins
- make_lego: Produces a lego plot

Provided Data Types:
--------------------
- FourVector: Represents 4 vectors
- ThreeVector: Represents 3 vectors
- Particle: A 4 vector that includes extra particle data
- ParticlePool: A collection of Particles.
- ResonanceData: Represents Resonances, this is not stable and could
    change at any point in the future.
"""

from PyPWA import info as _info
from PyPWA.libs import simulate
from PyPWA.libs.binning import bin_by_range, bin_with_fixed_widths, bin_by_list
from PyPWA.libs.file import (
    get_reader, get_writer, read, write, ProjectDatabase, cache, DataType
)
from PyPWA.libs.fit import (
    minuit, ChiSquared, LogLikelihood, EmptyLikelihood, NestedFunction,
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
    "EmptyLikelihood", "NestedFunction", "FunctionAmplitude", "cache",
    "ResonanceData", "bin_by_range", "bin_with_fixed_widths", "make_lego",
    "simulate", "DataType"
]

__author__ = _info.AUTHOR
__credits__ = ["Mark Jones"]
__version__ = _info.VERSION
__release__ = _info.RELEASE
__license__ = _info.LICENSE
