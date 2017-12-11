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
Optimizers for PyPWA
--------------------
- LikelihoodTypes - Enumeration of the different likelihood types.
- OptimizerTypes - Enumeration of the different optimizer types.
- Optimizer - Main Plugin for Optimizers
- OptimizerOptionParser - Takes the parameters sent via the optimizer and
  converts it to something more ingestible by the user's functions.
"""

import enum
from typing import Any, Callable, Dict, Optional

from PyPWA import AUTHOR, VERSION
from PyPWA.initializers.configurator.options import Levels, FileBuilder

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class Likelihood(enum.Enum):
    OTHER = 1
    CHI_SQUARED = 2
    LOG_LIKELIHOOD = 3


class Type(enum.Enum):
    MINIMIZER = 1
    MAXIMIZER = 2


class OptimizerConf(object):

    name = NotImplemented
    optimizer_summary = NotImplemented

    def get_optimizer_type(self):
        # type: () -> Type
        raise NotImplementedError

    def get_optimizer_parser(self):
        # type: () -> OptionParser
        raise NotImplementedError

    def get_optimizer(self):
        # type: () -> Optimizer
        raise NotImplementedError

    def get_defaults(self):
        # type: () -> Dict[str, Any]
        raise NotImplementedError

    def get_difficulties(self):
        # type: () -> Dict[str, Levels]
        raise NotImplementedError

    def get_types(self):
        # type: () -> Dict[str, type]
        raise NotImplementedError

    def get_option_comments(self):
        # type: () -> Dict[str, str]
        raise NotImplementedError


class HasPrior(object):

    def get_prior_function_template(self):
        #  type: () -> FileBuilder
        raise NotImplementedError


class Optimizer(object):

    def run(self, calculation_function, fitting_type=None):
        # type: (Callable[Any], Optional[Likelihood]) -> None
        raise NotImplementedError

    def save_data(self, save_location):
        # type: (str) -> None
        raise NotImplementedError


class OptionParser(object):

    def convert(self, passed_value):
        # type: (Any) -> Any
        raise NotImplementedError
