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
import os
import io
import logging

import appdirs
import fuzzywuzzy.process
import numpy

from PyPWA.configuratr import definitions
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION


FUZZY_STRING_CONFIDENCE_LEVEL = 75  # percent from 0 to 100


class BaseSettings(object):
    """
    Base Object for manipulating the settings dictionaries are loaded from
    the yaml and passed to each of the plugins and modules. Should help
    simplify the process of parsing arguments and even account for user error
    to a degree.
    """

    @staticmethod
    def _string_to_bool(string):
        """
        Converts a string to a bool with a level of certainty.

        Args:
            string (str): The string that needs to be converted into a bool.

        Returns:
            bool: If the conversion was successful.
            None: If the conversion fails.
        """
        value = fuzzywuzzy.process.extractOne(string, ["true", "false"])
        if value[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            if value[0] == "true":
                return True
            elif value[0] == "false":
                return False
            else:
                return None
        else:
            return None

    @staticmethod
    def _return_options(string):
        """
        Extracts options from a single string for inline option parsing.

        Args:
            string (str): The string to be rendered by plugins that support it.

        Returns:
            list[str]: The extracted options, unparsed.
        """
        options =[]
        for possible_option in string.split(";"):
            if "=" in possible_option:
                options.append(possible_option)
        return options

    @staticmethod
    def _extract_options(supported_options, options):
        """
        Extracts the options from an unparsed string.

        Args:
            supported_options (list[str]): The list of possible options that are
                supported.
            options (list[str]): The list of the unparsed options.

        Returns:
            dict: The completely parsed options from the string. Option = Value
        """
        correct_options = {}
        for possible_option in options:
            option = possible_option.split("=")[0]
            the_value = option.split("=")[1]
            the_key = fuzzywuzzy.process.extractOne(option, supported_options)
            if the_key[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
                correct_options[the_key[0]] = the_value
        return correct_options

    @staticmethod
    def _correct_values(supported_values, value):
        """
        Corrects a single value to match what is expected.
        Args:
            supported_values (list[str]): The possible values.
            value (str): The parsed value.

        Returns:
            str: The corrected value.
        """
        possible_value = fuzzywuzzy.process.extractOne(value, supported_values)
        if possible_value[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
            return possible_value[0]
        else:
            return None

    def _dict_values(self, found_value, template_value):
        """
        Corrects the dictionary based off another dictionary.

        Args:
            found_value (dict): The parsed dictionary with corrected keys.
            template_value (dict): The template dictionary that contains all the
                possible options and values/

        Returns:
            dict: The corrected dictionary.
        """

        # Checks for types that are known, but could be any value
        if isinstance(template_value, type):
            if template_value == bool:
                return self._string_to_bool(found_value)
            elif template_value == str:
                return str(found_value)
            elif template_value == int:
                try:
                    return int(found_value)
                except ValueError:
                    return None
            elif template_value == numpy.float64:
                try:
                    return numpy.float64(found_value)
                except ValueError:
                    return None
            return None

        # Checks for a list of potential values, then extracts the best match.
        elif isinstance(template_value, list):
            return self._correct_values(template_value, found_value)
        else:
            return None


class CorrectSettings(BaseSettings):

    def __init__(self):
        """
        Corrects simple settings.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def correct_dictionary(self, the_dictionary, template_dictionary):
        """
        Corrects the values and keys.

        Args:
            the_dictionary (dict): The parsed dictionary.
            template_dictionary (dict): The template dictionary.

        Returns:
            dict: The corrected dictionary.
        """
        corrected_dict = {}
        correct_keys = list(template_dictionary.keys())
        for key in the_dictionary:
            potential_key = fuzzywuzzy.process.extractOne(key, correct_keys)
            if potential_key[1] >= FUZZY_STRING_CONFIDENCE_LEVEL:
                value = self._dict_values(the_dictionary[key],
                                          template_dictionary[potential_key])

                if not isinstance(value, type(None)):
                    corrected_dict[potential_key] = value


class DataLocation(object):

    def __init__(self):
        """
        Attempts to find the location to nest specific data.
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
            file_location (Optional[str]): The location of the file, if blank
                will simply return the path.
            extension (Optional[str]): The optional extension, if blank will
                return the file without an extension.

        Returns:
            str: The full path to the cache directory optionally with a file
                name and extension.
        """
        cache_dir = appdirs.user_cache_dir("PyPWA", "JLab", __version__)
        return self._start_test(file_location, extension, cache_dir,
                                definitions.NoCachePath,
                                "Unable to find an appropriate cache "
                                "directory.")

    def find_data_dir(self, file_location=None, extension=None):
        """
        Finds the location of the data using appdirs.

        Args:
            file_location (Optional[str]): The location of the file, if blank
                will simply return the path.
            extension (Optional[str]): The optional extension, if blank will
                return the file without an extension.

        Returns:
            str: The full path to the data directory optionally with a file
                name and extension.
        """
        data_dir = appdirs.user_data_dir("PyPWA", "JLab", __version__)
        return self._start_test(file_location, extension, data_dir,
                                definitions.NoDataPath,
                                "Unable to find an appropriate data directory.")

    def find_log_dir(self, file_location=None, extension=None):
        """
        Finds the location of the log using appdirs.

        Args:
            file_location (Optional[str]): The location of the file, if blank
                will simply return the path.
            extension (Optional[str]): The optional extension, if blank will
                return the file without an extension.

        Returns:
            str: The full path to the log directory optionally with a file
                name and extension.
        """
        log_dir = appdirs.user_log_dir("PyPWA", "JLab", __version__)
        return self._start_test(file_location, extension, log_dir,
                                definitions.NoLogPath,
                                "Unable to find log directory.")

    def find_config_dir(self, file_location=None, extension=None):
        """
        Finds the location of the config using appdirs.

        Args:
            file_location (Optional[str]): The location of the file, if blank
                will simply return the path.
            extension (Optional[str]): The optional extension, if blank will
                return the file without an extension.

        Returns:
            str: The full path to the config directory optionally with a file
                name and extension.
        """
        config_dir = appdirs.user_config_dir("PyPWA", "JLab", __version__)
        return self._start_test(file_location, extension, config_dir,
                                definitions.NoConfigPath,
                                "Unable to find config directory.")

    def _start_test(self, location, extension, directory, error, message):
        """
        Starts the test on the directory to ensure that it can be accessed and
        written to.

        Args:
            location (str): The File Name or path to file.
            extension (str): The optional extension.
            directory (str): The directory rendered by appdirs
            error (definitions.NoPath): The error to throw if no directory can
                be found.
            message (str): The message paried with the raised error.

        Returns:
            str: The assured directory and optional file name for the data.
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
        The hash utility to use on a stream of any kind.
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
        The actual method that does the hashing, loads 4096 bit chunks into
        memory to hash against until there is no data left.
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
            self._logger.warning("Stream " + stream.name + "is not seekable, "
                                 "a crash is probably fixing to happen if the"
                                 " application is expecting the handle to be "
                                 " it left it.")
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
            list[numpy.ndarray]: The list of the number of arrays that need
                to be split.
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
                            the_dict[data][key], num_chunks)[index]

        return split_dict
