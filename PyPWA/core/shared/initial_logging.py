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
from typing import Optional as Opt

from PyPWA import AUTHOR, VERSION

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


class _LoggerData(object):

    level = ""  # type: str
    filename = ""  # type: str


class _InternalLogger(object):

    __LOGGER = logging.getLogger()
    __DATA = _LoggerData()
    __FORMATTER = logging.Formatter(
        "[%(asctime)s][%(processName)s][%(name)s][%(levelname)s]: "
        "%(message)s", "%H:%M:%S"
    )

    @classmethod
    def configure_root_logger(cls, level, file_name="", processor_id=""):
        # type: (str, str, str) -> None
        cls.__DATA.level = level
        cls.__DATA.filename = file_name
        cls.__setup_handlers(processor_id)
        cls.__set_level()

    @classmethod
    def __setup_handlers(cls, processor_id):
        # type: (str) -> None
        cls.__create_stream_handler()
        if cls.__DATA.filename:
            cls.__compute_file_name(processor_id)
            cls.__create_file_handler()

    @classmethod
    def __create_stream_handler(cls):
        handler = logging.StreamHandler()
        handler.setFormatter(cls.__FORMATTER)
        cls.__LOGGER.addHandler(handler)

    @classmethod
    def __compute_file_name(cls, processor_id):
        # type: (str) -> None
        if processor_id:
            cls.__DATA.filename = processor_id + "--" + cls.__DATA.filename

    @classmethod
    def __create_file_handler(cls):
        handler = logging.FileHandler(cls.__DATA.filename)
        handler.setFormatter(cls.__FORMATTER)
        cls.__LOGGER.addHandler(handler)

    @classmethod
    def __set_level(cls):
        cls.__LOGGER.setLevel(cls.__DATA.level)


def setup_logging(count, logfile=None):
    # type: (int, Opt[str]) -> None
    if count == 1:
        _InternalLogger.configure_root_logger(
            logging.WARNING, logfile
        )
    elif count == 2:
        _InternalLogger.configure_root_logger(
            logging.INFO, logfile
        )
    elif count >= 3:
        _InternalLogger.configure_root_logger(
            logging.DEBUG, logfile
        )
    else:
        _InternalLogger.configure_root_logger(
            logging.ERROR, logfile
        )
