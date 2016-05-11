import warnings
import logging


class FunctionLoading(object):
    """Object that loads the user defined functions from file
    Args:
        cwd (str): Path to folder with the functions
        function_location (str): Path to the file
        function_name (str): Name of Amplitude function
        setup_name (str): Name of Setup function.
    """

    def __init__(self, cwd, function_location, function_name, setup_name):
        self._logger = logging.getLogger(__name__)
        self._users_amplitude, self._users_setup = self._import_function(cwd, function_location, function_name,
                                                                         setup_name)

    @staticmethod
    def _import_function(cwd, function_location, function_name, setup_name):
        """Imports and sets up functions for usage.
        Args:
            cwd (str): Path to folder with the functions
            function_location (str): Path to the file
            function_name (str): Name of Amplitude function
            setup_name (str): Name of Setup function.
        Returns:
            list: [ amplitude function, setup function ]
        """
        sys.path.append(cwd)
        try:
            imported = __import__(function_location.strip(".py"))
        except ImportError:
            raise

        try:
            users_amplitude = getattr(imported, function_name)
        except:
            raise

        try:
            setup_function = getattr(imported, setup_name)
        except AttributeError:
            warnings.warn(("Setup function  {0} was not found in {1},"
                           "going without setup function").format(setup_name, function_location), UserWarning)

            def empty():
                pass
            setup_function = empty

        return [users_amplitude, setup_function]

    @property
    def return_amplitude(self):
        """Returns amplitude
        Returns:
            function: Amplitude Function
        """
        return self._users_amplitude

    @property
    def return_setup(self):
        """Returns setup
        Returns:
            function: Setup Function
        """
        return self._users_setup
