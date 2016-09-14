import importlib
import logging
import pkgutil
import sys

import os

import PyPWA


class PluginLoading(object):

    def __init__(self, root_object):
        """
        Loads plugins from either a directory or an already loaded module.
        Works by loading all attributes of that module then extracting
        the objects that subclass the supplied TemplateObject.

        Args:
            root_object (type): The Template Object to use for searching.
        """
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._root_object = root_object

    @staticmethod
    def _list_modules(module):
        """
        Simple little function that

        Args:
            module (module): The unknown module that was loaded.

        Returns:
            list[str]: A list of all the modules found in the package.

        See Also:
            http://stackoverflow.com/a/1310912
            http://stackoverflow.com/a/1708706
        """
        # Should make a list of:
        # [ ImporterInstance, name of module, is a package ]
        names = [
            name for loader, name, is_loaded in pkgutil.iter_modules(
                module.__path__
            )
        ]
        # Credit to unutbu and jp. for the discovery of how pkgutil works.
        return names

    @staticmethod
    def _import_lib(module_name):
        return importlib.import_module(module_name)

    def _find_libs(self, module):
        """
        Takes a package, finds all sub modules, then imports the
        submodules and returns those submodules.

        Args:
            module: The initial module.

        Returns:
            list[module]: The list of submodules.
        """
        libs = []
        for module_name in self._list_modules(module):
            libs.append(
                importlib.import_module(
                    module.__name__ + "." + module_name
                )
            )
        return libs

    def _extract_initializer(self, plugins):
        """
        Takes the loaded modules and searches them for the objects
        that subclass the template.

        Args:
            plugins list[module]: The list of modules that were found.

        Returns:
            list[type]: The list of objects that sub-classed the
                template.
        """
        plugin_initializer = []
        for plugin in plugins:
            self._logger.info(
                "Found the following modules: \n{0}".format(repr(plugin))
            )
            for object_name in dir(plugin):
                the_object = getattr(plugin, object_name)
                try:
                    if issubclass(the_object, self._root_object):
                        plugin_initializer.append(the_object)
                except TypeError:
                    pass

        return plugin_initializer

    def fetch_plugin(self, file_list):
        """
        Takes a list of files or modules then returns the objects that
        sub-classed the supplied Template.

        Args:
            file_list (list): The list of modules or paths that need to be
                loaded and searched

        Returns:
            list[type]: The list of objects that were found that
                sub-classed the object.
        """
        potential_plugins = []
        for the_file in file_list:
            if isinstance(the_file, str):
                # Appends the directory containing the
                sys.path.append(
                    os.path.dirname(os.path.abspath(the_file))
                )

                module = self._import_lib(
                    # Extracts the filename from the path provided
                    os.path.splitext(os.path.basename(the_file))[0]
                )

                potential_plugins.append(self._find_libs(module))
            elif isinstance(the_file, type(PyPWA)):
                potential_plugins.append(self._find_libs(the_file))

        flattened_potential = []
        for list_of_plugins in potential_plugins:
            for plugin in list_of_plugins:
                flattened_potential.append(plugin)

        plugins = self._extract_initializer(flattened_potential)

        return plugins


class SingleFunctionLoader(object):
    def __init__(self, file):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._module = None  # type: type(PyPWA)

        self._load_module(file)

    def _load_module(self, file):
        sys.path.append(
            os.path.dirname(os.path.abspath(file))
        )

        self._module = importlib.import_module(
            os.path.splitext(os.path.basename(file))[0]
        )

    def fetch_function(self, function_name, fail=False):
        try:
            return getattr(self._module, function_name)
        except Exception:
            if fail:
                raise
