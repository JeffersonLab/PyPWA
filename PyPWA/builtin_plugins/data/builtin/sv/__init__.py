from PyPWA.builtin_plugins.data import data_templates
from PyPWA.builtin_plugins.data.builtin.sv import iterator
from PyPWA.builtin_plugins.data.builtin.sv import memory
from PyPWA.builtin_plugins.data.builtin.sv import read_tests

HEADER_SEARCH_BITS = 1024  # type: int


class SvDataPlugin(data_templates.TemplateDataPlugin):

    @property
    def plugin_name(self):
        return "Delimiter Separated Variable sheets"

    def get_plugin_memory_parser(self):
        return memory.SvMemory()

    def get_plugin_reader(self, file_location):
        return iterator.SvReader(file_location)

    def get_plugin_writer(self, file_location):
        return iterator.SvWriter(file_location)

    def get_plugin_read_test(self):
        return read_tests.SvDataTest()

    @property
    def plugin_supported_extensions(self):
        return [".tsv", ".csv"]

    @property
    def plugin_supports_flat_data(self):
        return True

    @property
    def plugin_supports_gamp_data(self):
        return False
