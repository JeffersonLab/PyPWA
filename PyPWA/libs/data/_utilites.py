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

"""The utility objects for the Data Plugin

This holds all the main objects for the data plugin. This has search
functions but these objects should never know anything about the data
plugin they are trying to load, all it should ever care about is that
there is metadata that contains enough information about the plugin for
this to get started passing data to it.
"""

import logging
import pkgutil

from PyPWA.libs.data import definitions
from PyPWA import VERSION, LICENSE, STATUS

__author__ = ["Mark Jones"]
__credits__ = ["Mark Jones"]
__maintainer__ = ["Mark Jones"]
__email__ = "maj@jlab.org"
__status__ = STATUS
__license__ = LICENSE
__version__ = VERSION

"""
    In true developer fashion, we are lazy and defined the name of this
module that will be shown to users interfacing with this plugin only once.
So here exists the name, changing this one line will change the name of
the plugin throughout the program, and as such will break current
configurations.

    I would recommend writing some logic to handle multiple names before
actually changing this though so that old configuration files will still
work even without the new name being defined. Lists can hold names, lists
can be your friend, especially if you fuzz it.
"""
MODULE_NAME = "Builtin Parser"  # Name for the module externally.


class FindPlugins(object):

    def __init__(self):
        """
        Searches packages for modules and packages that contain the
        metadata needed to start and run the data module.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def find_plugin(self, package):
        """
        Starts the search for possible plugins.

        Args:
            package (module): The package that might contain the plugin(s)

        Returns:
            list[module]: The validated plugins that are likely to work
                with the data module.
        """
        possible_plugins = []

        for importer, modname, is_pkg in pkgutil.iter_modules(
                package.__path__):

            self._logger.debug(
                "Found Plugin %s, is package %s" % (modname, is_pkg)
            )

            plugin = self._import_plugin(importer, modname)
            if not isinstance(plugin, bool):
                if self._check_metadata(plugin):
                    possible_plugins.append(plugin)

        return possible_plugins

    def _import_plugin(self, importer, module):
        """
        Attempts to import the found plugins.

        Args:
            importer (importlib.machinery.FileFinder): The initialized
                importer from pkgutil.
            module (str): The name of the module that needs to be loaded.

        Returns:
            module: If the import was successful.
            False: If the import failed.
        """

        try:
            plugin = importer.find_module(module).load_module(module)
            self._logger.debug("Imported plugin %s" % plugin)
            return plugin
        except ImportError as Error:

            self._logger.info(
                "Import of plugin %s failed with error %s" % module, Error
            )
            return False

    def _check_metadata(self, plugin):
        """
        Checks for the metadata needed to use the plugin effectively.

        Args:
            plugin (module): The actual fully imported plugin.

        Returns:
            True: If the plugin contains metadata.
            False: If the plugin doesn't have metadata.
        """
        if hasattr(plugin, "metadata_data"):

            self._logger.debug(
                "Plugin %s has metadata, keeping." % plugin.__name__
            )

            return True
        else:
            self._logger.debug(
                "Plugin %s doesn't have metadata, skipping" %
                plugin.__name__
            )

            return False


class DataSearch(object):

    def __init__(self, plugins):
        """
        Attempts to search for the correct plugin using the data and the
        plugins validator.

        Args:
            plugins (list[module]): The list of the possible plugins that
                have been loaded.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._plugins = plugins

    def search(self, file_location):
        """
        Loops through the objects plugin list until it finds a validator
        that doesn't fail, then returns that plugin.

        Args:
            file_location (str): The location of the file that needs to be
                parsed.

        Returns:
            module: The plugin that should correctly parse the data that
                is being loaded from the disk.

        Raises:
            definitions.UnknownData: If no plugin reports that it can read
                the data then this will be raised to alert the caller that
                the data is unreadable.
        """
        for plugin in self._plugins:
            try:
                validator = plugin.metadata_data["validator"](
                    file_location
                )

                validator.test()
                self._logger.info("Found %s will load %s" %
                                  (plugin.__name__, file_location))
                return plugin
            except definitions.IncompatibleData:
                self._logger.debug("Skipping %s for data %s" %
                                   (plugin.__name__, file_location))
        raise definitions.UnknownData(
            "Unable to find a plugin that can load %s" % file_location
        )
