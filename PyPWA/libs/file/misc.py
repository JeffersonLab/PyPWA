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
Miscellaneous file tools.
-------------------------
"""

import hashlib
from pathlib import Path

from PyPWA import info as _info

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


_BUFFER = 40960


def get_sha512_hash(file_location: Path) -> str:
    file_hash = hashlib.sha512()
    with file_location.open("rb") as stream:
        for chunk in iter(lambda: stream.read(_BUFFER), b""):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def get_file_length(file_location: Path) -> int:
    with file_location.open("rb") as binary_stream:
        last_chunk = binary_stream.raw.read(_BUFFER)
        lines = last_chunk.count(b'\n')

        for chunk in iter(lambda: binary_stream.raw.read(_BUFFER), b""):
            lines += chunk.count(b'\n')
            if not chunk and not last_chunk.endswith(b'\n'):
                lines += 1

        if last_chunk.endswith(b'\n\n'):
            lines -= 1
    return lines
