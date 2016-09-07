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

"""
#TODO
"""

import hashlib
import logging

import appdirs
import os

from PyPWA import VERSION, LICENSE, STATUS
from PyPWA.core_libs import exceptions

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


class DataLocation(object):

    def __init__(self):
        """
        Attempts to find the location to store data, cache, or logs. Uses
        appdirs to determine the location on Mac, Windoze, and Linux, with
        a builtin fallback to the common working directory if no location
        could be found.
        Will throw out a NoPath exception if no writable directory was
        found including the cwd.
        """
        self._cwd = os.getcwd()

    @staticmethod
    def _make_filename(file_location, extension=""):
        """
        Extracts the file from the path and appends an extension to it.

        Args:
            file_location (str): The location of the file.
            extension (str): The extension to put on the file.

        Returns:
            str: The filename.
        """
        if isinstance(extension, type(None)):
            extension = ""

        basename = os.path.basename(file_location)
        file_without_extension = os.path.splitext(basename)[0]

        return file_without_extension + extension

    def find_cache_dir(self, file_location=None, extension=None):
        """
        Finds the location of the cache using appdirs.

        Args:
            file_location (Optional[str]): The location of the file, if
                blank will simply return the path.
            extension (Optional[str]): The optional extension, if blank
                will return the file without an extension.

        Returns:
            str: The full path to the cache directory optionally with a
                file name and extension.
        """
        cache_dir = appdirs.user_cache_dir("PyPWA", "JLab", __version__)

        return self._start_test(
            file_location, extension, cache_dir, exceptions.NoCachePath,
            "Unable to find an appropriate cache directory."
        )

    def find_data_dir(self, file_location=None, extension=None):
        """
        Finds the location of the data using appdirs.

        Args:
            file_location (Optional[str]): The location of the file, if
                blank will simply return the path.
            extension (Optional[str]): The optional extension, if blank
                will return the file without an extension.

        Returns:
            str: The full path to the data directory optionally with a
                file name and extension.
        """
        data_dir = appdirs.user_data_dir("PyPWA", "JLab", __version__)

        return self._start_test(
            file_location, extension, data_dir, exceptions.NoDataPath,
            "Unable to find an appropriate data directory."
        )

    def find_log_dir(self, file_location=None, extension=None):
        """
        Finds the location of the log using appdirs.

        Args:
            file_location (Optional[str]): The location of the file, if
                blank will simply return the path.
            extension (Optional[str]): The optional extension, if blank
                will return the file without an extension.

        Returns:
            str: The full path to the log directory optionally with a file
                name and extension.
        """
        log_dir = appdirs.user_log_dir("PyPWA", "JLab", __version__)

        return self._start_test(
            file_location, extension, log_dir, exceptions.NoLogPath,
            "Unable to find log directory."
        )

    def find_config_dir(self, file_location=None, extension=None):
        """
        Finds the location of the config using appdirs.

        Args:
            file_location (Optional[str]): The location of the file, if
                blank will simply return the path.
            extension (Optional[str]): The optional extension, if blank
                will return the file without an extension.

        Returns:
            str: The full path to the config directory optionally with a
                file name and extension.
        """
        conf_dir = appdirs.user_config_dir("PyPWA", "JLab", __version__)

        return self._start_test(
            file_location, extension, conf_dir, exceptions.NoConfigPath,
            "Unable to find config directory."
        )

    def _start_test(self, location, extension, directory, error, message):
        """
        Starts the test on the directory to ensure that it can be accessed
        and written to.

        Args:
            location (str): The File Name or path to file.
            extension (str): The optional extension.
            directory (str): The directory rendered by appdirs
            error (definitions.NoPath()): The error to throw if no
                directory can be found.
            message (str): The message paired with the raised error.

        Returns:
            str: The assured directory and optional file name for the
                data.
        """
        file_name = self._make_filename(location, extension)
        try:
            return self._test_dir_group(directory) + "/" + file_name
        except exceptions.NoPath:
            raise error(message)

    def _test_dir_group(self, test_dir):
        """
        Checks both the cwd and appdirs.

        Args:
            test_dir (str): The directory found by appdirs.

        Returns:
            str: The usable path to store data.

        Raises:
            definitions.NoPath: Raised if it fails to find a directory.
        """
        if os.path.exists(test_dir):
            try:
                self._test_dir(test_dir)
                return test_dir
            except OSError:
                try:
                    self._test_dir(self._cwd)
                    return self._cwd
                except OSError:
                    raise exceptions.NoPath

        else:
            try:
                os.mkdir(test_dir)
                self._test_dir(test_dir)
                return test_dir
            except OSError:
                try:
                    self._test_dir(self._cwd)
                    return self._cwd
                except OSError:
                    raise exceptions.NoPath

    @staticmethod
    def _test_dir(test_location):
        """
        Simple write test for the directory.

        Args:
            test_location (str): The directory that needs to be tested.
        """
        with open(test_location + "/test", "wt") as stream:
            stream.write("test\n")
        os.remove(test_location + "/test")


class FileHash(object):

    def __init__(self):
        """
        A stream hashing utility! This utility is a simple wrapper around
        the hashlib library. This utility can make a hash from any stream
        of data that you hand it from md5 to sha512.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def hash_sha512(self, stream):
        """
        Makes a sha512 hash of the stream.

        Args:
            stream: The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA512 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha512())

    def hash_sha384(self, stream):
        """
        Makes a sha384 hash of the stream.

        Args:
            stream: The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA384 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha384())

    def hash_sha256(self, stream):
        """
        Makes a sha256 hash of the stream.

        Args:
            stream: The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA256 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha256())

    def hash_sha224(self, stream):
        """
        Makes a sha224 hash of the stream.

        Args:
            stream: The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA224 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha224())

    def hash_sha1(self, stream):
        """
        Makes a sha1 hash of the stream.

        Args:
            stream: The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA1 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha1())

    def hash_md5(self, stream):
        """
        Makes a md5 hash of the stream.

        Args:
            stream: The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The MD5 sum of the file.
        """
        return self._the_hashening(stream, hashlib.md5())

    def _the_hashening(self, stream, the_hash):
        """
        The hashing method that takes the defined hash, sends it to be
        processed, the returns the hex of the hash.

        Args:
            stream: The stream that holds the data that is
                to be hashed.
            the_hash (hashlib.HASH): The loaded hashing method.
        Returns:
            str: The hex code of the file that was hashed..
        """
        final_hash = self._stream_handle(stream, the_hash)
        return final_hash.hexdigest()

    @staticmethod
    def _stream_handle(stream, the_hash):
        """
        The actual method that does the hashing, loads 4096 bit chunks
        into memory to hash against until there is no data left.

        Args:
            stream: The stream that holds the data that is
            to be hashed.
            the_hash (hashlib.HASH): The loaded hashing utility.
        Returns:

        """
        current = stream.tell()
        stream.seek(0)
        for chunk in iter(lambda: stream.read(4096), b""):
            the_hash.update(chunk)
        stream.seek(current)
        return the_hash
