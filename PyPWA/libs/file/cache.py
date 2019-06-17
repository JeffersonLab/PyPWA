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
Pickle Cache
------------
Stores the data in a python pickle so that it can be easily read at a
future time. Takes advantage of SHA512 file hashing to determine if the
source file hash changed since its contents were previously loaded.
"""

import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PyPWA import AUTHOR, VERSION
from PyPWA.libs.file import misc

__credits__ = ["Mark Jones"]
__author__ = AUTHOR
__version__ = VERSION


@dataclass
class _Package:
    """
    Stores the contents of any data that is loaded, as well as file
    source file hash, and the location of the cache.

    .. note::
        This is used both for finding the pickle and creating the
        pickle.
    """
    hash: str = None
    location: Path = None
    data: Any = None


class _IWrite(ABC):

    @abstractmethod
    def write_cache(self, data: Any):
        ...


class _IRead(ABC):

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        ...

    @abstractmethod
    def get_cache(self) -> Any:
        ...


class _ReadCache(_IRead):

    def __init__(self, package: _Package):
        self.__package = package
        self.__did_read = False
        self.__graciously_load_cache()

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.__package)

    def __graciously_load_cache(self):
        try:
            self.__load_data()
            self.__did_read = True
        except Exception:
            self.__did_read = False

    def __load_data(self):
        with self.__package.location.open("rb") as stream:
            self.__package = pickle.load(stream)

    def get_cache(self) -> Any:
        if self.is_valid:
            return self.__package.data
        else:
            raise RuntimeError("No valid data.")

    @property
    def is_valid(self) -> bool:
        if self.__package.hash == self.__package.hash and self.__did_read:
            return True
        else:
            return False


class _ClearCache(_IRead):

    def __init__(self, package: _Package):
        self.__package = package
        self.__attempt_to_remove_cache()

    def __repr__(self) -> str:
        return "{0}({1})".format(self.__class__.__name__, self.__package)

    @property
    def is_valid(self):
        return False

    def get_cache(self):
        raise RuntimeError("No Valid Cache")

    def __attempt_to_remove_cache(self):
        try:
            if self.__package.location.exists():
                self.__package.location.unlink()
        except Exception:
            pass


class _NoRead(_IRead):

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    @property
    def is_valid(self) -> bool:
        return False

    def get_cache(self) -> Any:
        raise RuntimeError("No valid cache.")


class _WriteCache(_IWrite):

    def __init__(self, package: _Package):
        self.__package = package

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.__package)

    def write_cache(self, data: Any):
        self.__package.data = data
        self.__try_to_write_cache()

    def __try_to_write_cache(self):
        try:
            with self.__package.location.open("wb") as stream:
                pickle.dump(self.__package, stream)
        except Exception:
            pass


class _NoWrite(_IWrite):

    def __repr__(self) -> str:
        return "{0}()".format(self.__class__.__name__)

    def write_cache(self, data: Any):
        pass


class Cache:
    """
    This class provides access to the file's cache
    .. SeeAlso:: CacheFactory
    """
    def __init__(self, read_cache: _IRead, write_cache: _IWrite):
        self.__read_cache = read_cache
        self.__write_cache = write_cache

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}"
                f"({self.__read_cache!r}, {self.__write_cache!r})")

    def write_cache(self, data: Any):
        """
        :param data: The data inside the source file, or the essential
            excerpt, that needs to be accessed at a later time.
        """
        self.__write_cache.write_cache(data)

    @property
    def is_valid(self) -> bool:
        """
        Run this first, as read_cache will raise an error if you try to
        access an invalid cache.

        :return: True if valid, False otherwise
        """
        return self.__read_cache.is_valid

    def read_cache(self) -> Any:
        """
        :raises RuntimeError: If cache is invalid.
        :return: The data that was stored in the pickle
        """
        return self.__read_cache.get_cache()


class CacheFactory:

    def __init__(self, use_cache: bool = True, clear_cache: bool = False):
        """
        Produces the cache object for the specific file that is
        provided.
        :param use_cache: If False, caching will be disabled
        :param clear_cache: If True, current cache will be removed even if
            valid. Will remove cache even if use_cache is False.
        """
        self.__use_cache = use_cache
        self.__clear_cache = clear_cache

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}"
                f"({self.__use_cache}, {self.__clear_cache})")

    def get_cache(self, file_location: Path) -> Cache:
        try:
            file_hash = misc.get_sha512_hash(file_location)
        except FileNotFoundError:
            file_hash = ""

        package = _Package(
            hash=file_hash,
            location=misc.get_cache_uri() / (file_location.stem + ".pickle")
        )
        reader = self.__get_reader(package)
        writer = self.__get_writer(package)
        return Cache(reader, writer)

    def __get_reader(self, package: _Package) -> _IRead:
        if self.__clear_cache:
            return _ClearCache(package)
        elif not self.__use_cache or not package.hash:
            return _NoRead()
        else:
            return _ReadCache(package)

    def __get_writer(self, package: _Package) -> _IWrite:
        if not self.__use_cache:
            return _NoWrite()
        else:
            return _WriteCache(package)

    @property
    def use_cache(self) -> bool:
        return self.__use_cache

    @use_cache.setter
    def use_cache(self, use_cache: bool):
        if isinstance(use_cache, bool):
            self.__use_cache = use_cache
        else:
            raise ValueError("use_cache must be boolean")

    @property
    def clear_cache(self) -> bool:
        return self.__clear_cache

    @clear_cache.setter
    def clear_cache(self, clear_cache: bool):
        if isinstance(clear_cache, bool):
            self.__clear_cache = clear_cache
        else:
            raise ValueError("clear_cache must be boolean")
