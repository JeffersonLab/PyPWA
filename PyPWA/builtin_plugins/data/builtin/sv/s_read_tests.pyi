#    PyPWA, a scientific analysis toolkit.
#    Copyright (C) 2016  JLab
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv
import io
import logging
import typing

from PyPWA.builtin_plugins.data import data_templates

__author__ = ... # type: typing.List[str]
__credits__ = ... # type: typing.List[str]
__maintainer__ = ... # type: typing.List[str]
__email__ = ... # type: str
__status__ = ... # type: str
__license__ = ... # type: str
__version__ = ... # type: str


HEADER_SEARCH_BITS = ... # type: int


class SvDataTest(data_templates.ReadTest):

    _stream = ...  # type: io.FileIO

    def quick_test(self, file_location: str): ...

    def full_test(self, file_location: str): ...

    def _set_stream(self, file_location: str): ...

    def _header_test(self): ...


class _HeaderTest(object):

    _logger = logging.getLogger(__name__)
    _stream = ...  # type: io.FileIO
    _sniffer = ...  # type: csv.Sniffer
    _sample = ...  # type: str

    def __init__(self, stream: io.FileIO): ...

    def do_test(self): ...

    def _set_sniffer(self): ...

    def _load_sample(self): ...

    def _header_test(self): ...

    def _has_a_header(self) -> bool: ...

    def _reset_stream(self): ...
