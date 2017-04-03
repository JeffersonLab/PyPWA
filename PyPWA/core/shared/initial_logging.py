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
A simple function that sets the logging conditions for the entire program.
This controls the formatting off the logs, where the logs are located, and
the level of verbosity of those logs.
"""

import logging

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


def define_logger(level):
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
