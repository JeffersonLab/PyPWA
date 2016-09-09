import copy

import ruamel.yaml.comments

"""
Just Breath, take it slow, its all abstract.
"""


class OptionsTemplate(object):

    _required = "required"
    _optional = "optional"
    _advanced = "advanced"
    _kernel_processing = "kernel processing"
    _minimization = "minimization"
    _data_reader = "data reader"
    _data_parser = "data parser"

    def __init__(self):
        if self._default_options():
            self.__processed = self.__build_options_dictionary()
            self.__the_required, self.__the_optional, \
                self.__the_advanced = self.__build_leveled_dictionaries()
        else:
            self.__the_required = {}
            self.__the_optional = {}
            self.__the_advanced = {}

    def _plugin_name(self):
        raise NotImplementedError

    def _plugin_interface(self):
        raise NotImplementedError

    def _plugin_type(self):
        raise NotImplementedError

    def _plugin_requires(self):
        raise NotImplementedError

    def _plugin_arguments(self):
        raise NotImplementedError

    def _default_options(self):
        raise NotImplementedError

    def _option_levels(self):
        raise NotImplementedError

    def _option_types(self):
        raise NotImplementedError

    def _main_comment(self):
        raise NotImplementedError

    def _option_comments(self):
        raise NotImplementedError

    def __build_options_dictionary(self):
        """
        Builds the dictionary with the default options and the comments
        connected to to each key.

        Returns:
            dict: The dictionary with all
                the comments and the default options.
        """
        defaults = self._default_options()

        header = ruamel.yaml.comments.CommentedMap()
        header.yaml_add_eol_comment(
            self._main_comment(), self._plugin_name()
        )

        content = ruamel.yaml.comments.CommentedMap()
        header[self._plugin_name()] = content

        for key in list(self._option_comments().keys()):
            header.yaml_add_eol_comment(
                self._option_comments()[key], key
            )

            header[self._plugin_name()][key] = defaults[key]

        return header

    def __build_leveled_dictionaries(self):
        """
        Parses the dictionary out to 3 different dictionaries. Each being
        a level of potential user requests.

        Returns:
            list[dict]: The 3 dictionaries
                that hold the data that
        """
        levels = self._option_levels()

        required = copy.deepcopy(self.__processed)
        optional = copy.deepcopy(self.__processed)
        advanced = copy.deepcopy(self.__processed)

        for key in list(levels.keys()):
            if levels[key] == self._required:
                pass
            elif levels[key] == self._optional:
                required[self._plugin_name()].pop(key)
            elif levels[key] == self._advanced:
                required[self._plugin_name()].pop(key)
                optional[self._plugin_name()].pop(key)

        return [required, optional, advanced]

    @staticmethod
    def _build_function(imports, function):
        return {"function": function, "imports": set(imports)}

    def request_options(self, level):
        return {
            "required": self.__the_required,
            "optional": self.__the_optional,
            "advanced": self.__the_advanced
        }[level]

    def request_metadata(self, data):
        """

        Args:
            data (str):

        Returns:

        """
        return {
            "name": self._plugin_name(),
            "interface": self._plugin_interface(),
            "provides": self._plugin_type(),
            "requires function": self._plugin_requires(),
            "arguments": self._plugin_arguments()
        }[data]


class _InitialOptions(object):
    def __init__(self, options):
        for key in list(options.keys()):
            setattr(self, "_" + key.replace(" ", "_"), options[key])


class MinimizerTemplate(_InitialOptions):
    """
    Template for minimization plugins.
    """
    def __init__(self, options):
        super(MinimizerTemplate, self).__init__(options)

    def main_options(self, calc_function, fitting_type=False):
        raise NotImplementedError

    def convert(self, passed_value):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError


class KernelProcessingTemplate(_InitialOptions):
    """
    Template for kernel processing plugins.
    """
    def __init__(self, options):
        super(KernelProcessingTemplate, self).__init__(options)

    def main_options(self, data, process_template, interface_template):
        raise NotImplementedError

    def fetch_interface(self):
        raise NotImplementedError


class InterfaceTemplate(object):
    """
    Template for interface objects to be handed off by the KernelProcessor
    """

    def run(self, *args):
        raise NotImplementedError

    @property
    def previous_value(self):
        raise NotImplementedError

    def stop(self, force=False):
        raise NotImplementedError

    @property
    def is_alive(self):
        raise NotImplementedError


class DataParserTemplate(_InitialOptions):
    """
    Template for data parser and writing plugins
    """

    def __init__(self, options):
        super(DataParserTemplate, self).__init__(options)

    def parse(self, text_file):
        raise NotImplementedError

    def write(self, data, text_file):
        raise NotImplementedError


class DataReaderTemplate(_InitialOptions):
    """
    Template for data reader and writers plugins.
    """

    def __init__(self, options):
        super(DataReaderTemplate, self).__init__(options)

    def return_reader(self, text_file):
        raise NotImplementedError

    def return_writer(self, text_file, data_shape):
        raise NotImplementedError


class ReaderTemplate(object):

    def __init__(self, file_location):
        self._the_file = file_location

    def reset(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object reset properly when "
            "this method is called." % self.__class__.__name__
        )

    @property
    def next_event(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object read in the next "
            "event properly when its called." % self.__class__.__name__
        )

    def next(self):
        return self.next_event

    def __next__(self):
        return self.next_event

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @property
    def previous_event(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object return the last "
            "value that was parsed." % self.__class__.__name__
        )

    def close(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object return the last "
            "value that was parsed." % self.__class__.__name__
        )


class WriterTemplate(object):

    def __init__(self, file_location):
        self._the_file = file_location

    def write(self, data):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object write the data out "
            "to the disk correctly." % self.__class__.__name__
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        raise NotImplementedError(
            "%s does not overwrite method write. This is the method that "
            "you should overwrite to have the object properly operated "
            "properly when its called" % self.__class__.__name__
        )


class ShellCoreTemplate(object):
    def make_config(self, application_data):
        raise NotImplementedError

    def run(self, application_data):
        raise NotImplementedError
