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

import sys
import hashlib
import os
import io
import logging

import appdirs
import numpy

from PyPWA.configurator import definitions
from PyPWA import VERSION, LICENSE, STATUS

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
        return os.path.splitext(os.path.basename(file_location))[0] + \
            extension

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
            file_location, extension, cache_dir, definitions.NoCachePath,
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
            file_location, extension, data_dir, definitions.NoDataPath,
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
            file_location, extension, log_dir, definitions.NoLogPath,
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
            file_location, extension, conf_dir, definitions.NoConfigPath,
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
            error (definitions.NoPath): The error to throw if no directory
                can be found.
            message (str): The message paried with the raised error.

        Returns:
            str: The assured directory and optional file name for the
                data.
        """
        file_name = self._make_filename(location, extension)
        try:
            return self._test_dir_group(directory) + "/" + file_name
        except definitions.NoPath:
            raise error(message)

    def _test_dir_group(self, test_dir):
        """
        Checks both the cwd and appdir.

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
            except PermissionError:
                try:
                    self._test_dir(self._cwd)
                    return self._cwd
                except PermissionError:
                    raise definitions.NoPath

        else:
            try:
                os.mkdir(test_dir)
                self._test_dir(test_dir)
                return test_dir
            except PermissionError:
                try:
                    self._test_dir(self._cwd)
                    return self._cwd
                except PermissionError:
                    raise definitions.NoPath

    @staticmethod
    def _test_dir(test_location):
        """
        Simple write test for the directory.

        Args:
            test_location (str): The directory that needs to be tested.
        """
        with io.open(test_location + "/test", "wt") as stream:
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
            stream (io.FileIO): The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA512 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha512())

    def hash_sha384(self, stream):
        """
        Makes a sha384 hash of the stream.

        Args:
            stream (io.FileIO): The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA384 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha384())

    def hash_sha256(self, stream):
        """
        Makes a sha256 hash of the stream.

        Args:
            stream (io.FileIO): The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA256 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha256())

    def hash_sha224(self, stream):
        """
        Makes a sha224 hash of the stream.

        Args:
            stream (io.FileIO): The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA224 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha224())

    def hash_sha1(self, stream):
        """
        Makes a sha1 hash of the stream.

        Args:
            stream (io.FileIO): The stream that has all the data that
                needs to be hashed.
        Returns:
            str: The SHA1 sum of the file.
        """
        return self._the_hashening(stream, hashlib.sha1())

    def hash_md5(self, stream):
        """
        Makes a md5 hash of the stream.

        Args:
            stream (io.FileIO): The stream that has all the data that
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
            stream (io.FileIO): The stream that holds the data that is
                to be hashed.
            the_hash (hashlib.HASH): The loaded hashing method.
        Returns:
            str: The hex code of the file that was hashed..
        """
        final_hash = self._stream_handle(stream, the_hash)
        return final_hash.hexdigest()

    def _stream_handle(self, stream, the_hash):
        """
        The actual method that does the hashing, loads 4096 bit chunks
        into memory to hash against until there is no data left.

        Args:
            stream (io.FileIO): The stream that holds the data that is
            to be hashed.
            the_hash (hashlib.HASH): The loaded hashing utility.
        Returns:

        """
        if stream.seekable():
            current = stream.tell()
            stream.seek(0)
            for chunk in iter(lambda: stream.read(4096), b""):
                the_hash.update(chunk)
            stream.seek(current)
        else:
            for chunk in iter(lambda: stream.read(4096), b""):
                the_hash.update(chunk)

            self._logger.warning(
                "Stream " + stream.name + "is not seekable, a crash is "
                "probably fixing to happen if the application is "
                "expecting the handle to be  it left it."
            )

        return the_hash


class DataSplit(object):
    """
    Static Object holding the splitting logic for arrays and dictionaries.
    #Todo: Add support for the new data types.
    """

    @staticmethod
    def array_split(array, num_chunks):
        """
        Simple wrapper around the numpy array split

        Args:
            array (numpy.ndarray):  The array that needs to be split.
            num_chunks (int): The number of arrays that are needed
        return:
            list[numpy.ndarray]: The list of the number of arrays that
                needs to be split.
        """

        return numpy.array_split(array, num_chunks)

    @staticmethod
    def dict_split(the_dict, num_chunks):
        """
        Splits dictionary into user defined number of chunks

        Args:
            the_dict (dict): Dictionary of arrays that needs to be split
            num_chunks (int): Number of chunks

        Returns:
            list: Each index is a chunk of the returned data in order
        """

        if num_chunks == 1:
            return [the_dict]

        split_dict = []

        for x in range(num_chunks):
            split_dict.append({})

        for data in the_dict:
            if isinstance(the_dict[data], numpy.ndarray):
                for index in range(num_chunks):
                    split_dict[index][data] = numpy.array_split(
                        the_dict[data], num_chunks)[index]

            elif isinstance(the_dict[data], dict):
                for index in range(num_chunks):
                    split_dict[index][data] = {}
                for key in the_dict[data]:
                    for index in range(num_chunks):
                        split_dict[index][data][key] = numpy.array_split(
                            the_dict[data][key], num_chunks
                        )[index]

        return split_dict


class ImportTools(object):

    def __init__(self):
        """
        Simple little object that imports objects and packages for use by
        PyPWA and its tools.

        NOTE:
            ONLY LOAD IN TRUSTED CODE, MALICIOUS CODE CAN AND WILL DO
            HARM!
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def import_package(self, folder):
        """
        Imports a package into the interpreter. Specifically folders with
        an __init__.py should use this. This is useful for packages full
        of complex plugins or many plugins.

        Args:
            folder (str): The actual location of the folder that contains
                the __init__.py that needs to be read in.

        Returns:
            module: The package that was loaded in from file.
        """
        self._append_path(folder)
        return __import__(os.path.basename(folder))

    def import_object(self, file, object_name):
        """
        Imports a single object from a single script or package. Helpful
        when you are importing a single script file and you have an idea
        of what you need from that script file.

        Args:
            file (str): The file that needs to be imported from the
                directory.
            object_name (str): The specific object that needs to be
                imported from the file.

        Returns:
            Whatever was inside the file that you want to extract.
        """
        self._append_path(file)
        imported = self._import_script(file)
        return self._extract_object(imported, object_name)

    def _import_script(self, file):
        """
        Imports a single script into the interpreter.

        Args:
            file (str): The location of the file that needs to be imported

        Returns:
            module: The module that was imported from the python file.
        """
        self._append_path(file)
        return __import__(os.path.basename(file).strip(".py"))

    @staticmethod
    def _extract_object(imported, object_name):
        """
        Extracts a single object from the module that was imported.

        Args:
            imported (module): The object that was imported.
            object_name (str): The name of the object that needs to be
                extracted.

        Returns:
            Whatever you extracted from the module.
        """
        return getattr(imported, object_name)

    @staticmethod
    def _append_path(file):
        """
        Appends the path to the file or folder being imported to the
        interpreters path so that it can find it when the importer calls
            for it.

        Args:
            file (str): The path to the file, absolute or relative.
        """
        sys.path.append(os.path.dirname(file))
