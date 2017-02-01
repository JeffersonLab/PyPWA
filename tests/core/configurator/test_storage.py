import pytest
import PyPWA.builtin_plugins
from PyPWA.core import plugin_loader
from PyPWA.core.configurator import _storage
from PyPWA.core.templates import option_templates
from PyPWA.builtin_plugins import data
from PyPWA.shell import fitting


@pytest.fixture
def setup_metadata_storage():
    loader = plugin_loader.PluginLoading(
        option_templates.PluginsOptionsTemplate
    )

    plugin_list = loader.fetch_plugin([PyPWA.builtin_plugins])

    metadata_storage = _storage.MetadataStorage()
    metadata_storage.add_plugins(plugin_list)
    return metadata_storage


@pytest.fixture()
def return_count(setup_metadata_storage):
    def the_returning(plugin_type):
        plugins = setup_metadata_storage.request_plugin_by_type(plugin_type)
        try:
            return len(plugins)
        except TypeError:
            return setup_metadata_storage.return_plugin_types()

    return the_returning


def test_metadata_finds_all_data_parsers(return_count):
    assert return_count("data parser") == 1


def test_metadata_finds_all_data_readers(return_count):
    assert return_count("data reader") == 1


def test_metadata_finds_all_kernel_processors(return_count):
    assert return_count("kernel processing") == 1


def test_metadata_finds_all_optimizers(return_count):
    assert return_count("minimization") == 2


def test_metadata_return_plugin_names(setup_metadata_storage):
    plugin_types = [
        "data parser",
        "data reader",
        "minimization",
        "kernel processing"
    ]

    for plugin_type in plugin_types:
        assert plugin_type in setup_metadata_storage.return_plugin_types()


@pytest.fixture
def setup_module_templates():
    return _storage.ModuleTemplates()


def test_templates_is_dict(setup_module_templates):
    assert isinstance(setup_module_templates.templates, dict)


def test_builtin_parser_in_templates(setup_module_templates):
    assert "Builtin Parser" in setup_module_templates.templates.keys()


@pytest.fixture()
def setup_module_picking():
    return _storage.ModulePicking()


def test_can_extract_builtin_parser(setup_module_picking):
    plugin = setup_module_picking.request_plugin_by_name("Builtin Parser")
    assert isinstance(plugin, data.DataParser)


def test_can_extract_pyfit(setup_module_picking):
    main = setup_module_picking.request_main_by_id("shell fitting method")
    assert isinstance(main, fitting.ShellFitting)
