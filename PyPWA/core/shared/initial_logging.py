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


class _LoggerData(object):

    level = None
    filename = None


class InternalLogger(object):

    __logger = logging.getLogger()
    __data = _LoggerData()
    __formatter = logging.Formatter(
        "[%(asctime)s][%(processName)s][%(name)s][%(levelname)s]: "
        "%(message)s", "%H:%M:%S"
    )

    @classmethod
    def configure_root_logger(cls, level, file_name="", processor_id=""):
        cls.__data.level = level
        cls.__data.filename = file_name
        cls.__setup_handlers(processor_id)
        cls.__set_level()

    @classmethod
    def __setup_handlers(cls, processor_id):
        cls.__create_stream_handler()
        if cls.__data.filename:
            cls.__compute_file_name(processor_id)
            cls.__create_file_handler()

    @classmethod
    def __create_stream_handler(cls):
        handler = logging.StreamHandler()
        handler.setFormatter(cls.__formatter)
        cls.__logger.addHandler(handler)

    @classmethod
    def __compute_file_name(cls, processor_id):
        if processor_id:
            cls.__data.filename = processor_id + "--" + cls.__data.filename

    @classmethod
    def __create_file_handler(cls):
        handler = logging.FileHandler(cls.__data.filename)
        handler.setFormatter(cls.__formatter)
        cls.__logger.addHandler(handler)

    @classmethod
    def __set_level(cls):
        cls.__logger.setLevel(cls.__data.level)

    @classmethod
    def get_level(cls):
        return cls.__data.level

    @classmethod
    def get_filename(cls):
        return cls.__data.filename

    @classmethod
    def set_level_to_global(cls):
        cls.__data.level = cls.__logger.getEffectiveLevel()
