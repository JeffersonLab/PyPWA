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

import numpy
from PyPWA.builtin_plugins.data import data_templates

__author__ = ... # type: typing.List[str]
__credits__ = ... # type: typing.List[str]
__maintainer__ = ... # type: typing.List[str]
__email__ = ... # type: str
__status__ = ... # type: str
__license__ = ... # type: str
__version__ = ... # type: str

HEADER_SEARCH_BITS = ...  # type: int


class SvMemory(data_templates.TemplateMemory):

    def parse(self, file_location: str) -> numpy.ndarray: ...

    def write(self, file_location: str, data: numpy.ndarray): ...


class _SvParser(object):

    _logger = logging.getLogger(__name__)
    _line_count = ... # type: int
    _dialect = ...  # type: str
    _stream = ...  # type: io.FileIO
    _reader = ...  # type: csv.reader
    _header = ...  # type: typing.List[str]

    def __init__(self): ...

    def return_read_data(self, file_location: str) -> numpy.ndarray: ...

    def _set_line_number(self): ...

    def _open_stream(self, file_location: str): ...

    def _reset_stream(self): ...

    def _close_stream(self): ...

    def _set_required_data(self): ...

    def _set_dialect(self): ...

    def _set_reader(self): ...

    def _set_header(self): ...

    def _parse_data(self): ...

    def _setup_numpy_array(self) -> numpy.ndarray: ...

    def _build_numpy_types(self) -> typing.List[typing.Tuple[str]]: ...

    def _make_empty_numpy_array(self, dtype: typing.List[typing.Tuple[str]]) -> numpy.ndarray: ...

    def _fill_array(self, empty_array: numpy.ndarray) -> numpy.ndarray: ...

    def _fill_row(self, array: numpy.ndarray, row_index: int, row_data: typing.List[numpy.float64]): ...


class _SvMemoryWriter(object):

    _dialect = ... # type: str
    _column_names = ...  # type: typing.List[str]
    _stream = ...  # type: io.FileIO
    _writer = ...  # type: csv.DictWriter

    def write_memory_to_disk(self, file_location: str, data: numpy.ndarray): ...

    def _setup_basic_data(self, file_location: str, data: numpy.ndarray): ...

    def _process_dialect(self, file_location: str): ...

    @staticmethod
    def _get_extension(file_location: str) -> str: ...

    def _set_dialect(self, extension: str): ...

    def _set_column_names(self, data: numpy.ndarray): ...

    def _setup_writer(self, file_location: str): ...

    def _open_stream(self, file_location: str): ...

    def _set_writer(self): ...

    def _write_header(self): ...

    def _write_data(self, data: numpy.ndarray): ...

    def _iterator_over_columns(self, data: numpy.ndarray) -> range: ...

    def _convert_row_to_dict(self, row_index: int, data: numpy.ndarray) -> dict: ...
