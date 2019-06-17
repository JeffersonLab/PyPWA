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
Sets the logging conditions for the entire program.
This controls the formatting off the logs, where the logs are located, and
the level of verbosity of those logs.
"""

import logging
from pathlib import Path
from typing import Optional

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


def setup_logging(count: int, logfile: Optional[Path] = None):
    root_logger = logging.getLogger()
    formatter = logging.Formatter(
        "[%(asctime)s+.%(msecs)03d][%(name)s][%(levelname)s]: "
        "%(message)s", "%H:%M:%S"
    )

    # Setup the stderr handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # If a file is provided, setup the file handler
    if isinstance(logfile, Path):
        file_handler = logging.FileHandler(str(logfile))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Setup the logging level
    if count == 1:
        root_logger.setLevel(logging.WARNING)
    elif count == 2:
        root_logger.setLevel(logging.INFO)
    elif count >= 3:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.ERROR)
