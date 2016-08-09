import copy

import ruamel.yaml.comments


class TemplateOptions(object):

    _required = "required"
    _optional = "optional"
    _advanced = "advanced"
    _kernel_processing = "kernel processing"
    _minimization = "minimization"
    _data_reader = "data reader"
    _data_parser = "data parser"

    def __init__(self):
        self.__processed = self.__build_options_dictionary()
        self.__the_required, self.__the_optional, self.__the_advanced = \
            self.__build_leveled_dictionaries()

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


class MinimizerTemplate(object):
    """
    Template for minimization plugins.
    """
    def configurator_options(self, options):
        raise NotImplementedError

    def main_options(self, calc_function):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError


class KernelProcessingTemplate(object):
    """
    Template for kernel processing plugins.
    """
    def configurator_options(self, options):
        raise NotImplementedError

    def main_options(self, data, process_template, interface_template):
        raise NotImplementedError


class DataReaderTemplate(object):
    """
    Template for data reader and writers plugins.
    """
    def return_reader(self, text_file):
        raise NotImplementedError

    def return_writer(self, text_file):
        raise NotImplementedError


class DataParserTemplate(object):
    """
    Template for data parser and writering plugins
    """
    def parse_data(self, text_file):
        raise NotImplementedError

    def write_data(self, data, text_file):
        raise NotImplementedError
