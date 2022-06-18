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
Caching
-------
Stores the data in a pickle cache. By taking advantage of SHA-512 and
python's pickle, caches can be loaded and stored rapidly, while allowing
us to automatically invalidate the cache when the source file has changed
in any way.

Both read and write support being used as an intermediate step. The
intermediate step would allow you to save your data quickly for loading
later. The resulting file would only be readable in Python. This method
is very fast.
"""

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Tuple, Union

from PyPWA import info as _info
from PyPWA.libs.file import misc

__credits__ = ["Mark Jones"]
__author__ = _info.AUTHOR
__version__ = _info.VERSION


@dataclass
class _Package:
    """
    Stores the contents of any data that is loaded and the files hash.
    """
    hash: str = None
    data: Any = None
    version: int = 1


def read(
        path: Union[str, Path], intermediate=True, remove_cache=False
) -> Tuple[bool, Any]:
    """Reads a cache object

    This reads caches objects from the disk. With its default settings
    it'll load the cache file as long as the source file's hash hasn't
    changed. It can also be used to store an intermediate step directly
    by providing a name and setting intermediate to True.

    Parameters
    ----------
    path : Path or str
        The path of the source file, or path where you want the
        intermediate step t0 be stored.
    intermediate : bool
        If set to true, the cache will be treated as an intermediate step,
        this means it will assume there is no data file associated with
        the data, and will not check file hashes.
    remove_cache : bool
        Setting this to true will remove the cache.

    Returns
    -------
    Tuple[bool, any]
        The first value in the tuple is whether the cache is valid or not
        and the second value in the returned tuple is whatever data was
        stored in the cache.
    """
    path = Path(path)
    cache_path = path.parent / (path.stem + ".cache")

    if intermediate:
        cache_path = Path(path.stem + ".intermediate")
        file_hash = ""
    else:
        try:
            file_hash = misc.get_sha512_hash(path)
        except FileNotFoundError:
            return False, None

    if remove_cache:
        cache_path.unlink()
        return False, None

    try:
        with cache_path.open("rb") as stream:
            data_package = pickle.load(stream)  # type: _Package
    except Exception:
        return False, None

    if data_package.hash == file_hash or intermediate:
        return True, data_package.data
    else:
        return False, None


def write(path, data, intermediate=False):
    """Writes a cache file

    With its default settings, it'll write the cache file into the cache
    location and store the source file's hash in the cache for future
    comparison. If intermediate is set to true though, it'll store the
    cache in the provided location, and will not store a hash.

    Parameters
    ----------
    path : Path or str
        The path of the source file, or path where you want the
        intermediate step t0 be stored.
    data : Any
        Whatever data you wish to be stored in the cache. Almost anything
        that can be stored in a variable, can be stored on disk.
    intermediate : bool
        If set to true, the cache will be treated as an intermediate step,
        this means it will assume there is no data file associated with
        the data, and will not check file hashes.
    """
    path = Path(path)
    cache_path = Path(path.stem + ".intermediate")
    file_hash = ""
    if not intermediate:
        file_hash = misc.get_sha512_hash(path)
        cache_path = path.stem / Path(path.stem + ".cache")

    data_package = _Package(file_hash, data)

    try:
        with cache_path.open("wb") as stream:
            pickle.dump(data_package, stream)
    except Exception:
        if cache_path.exists():
            cache_path.unlink()
        raise RuntimeWarning("Your data can not be saved in cache!")
