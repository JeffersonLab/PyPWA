import PyPWA.builtin_plugins
from PyPWA.core import plugin_loader
from PyPWA.core.configurator import _storage
from PyPWA.core.templates import option_templates


def test_PluginStorage_RenderTemplate_IsDict():
    storage = _storage.PluginStorage()
    assert isinstance(storage.templates_config, dict)


def test_MetadataStorage_LoadPluginsRandomPlugins_PluginsSorted():
    loader = plugin_loader.PluginLoading(
        option_templates.PluginsOptionsTemplate
    )

    plugin_list = loader.fetch_plugin([PyPWA.builtin_plugins])

    metadata_storage = _storage.MetadataStorage()
    metadata_storage.add_plugins(plugin_list)

    assert len(metadata_storage.data_parser) == 1
    assert len(metadata_storage.data_reader) == 1
    assert len(metadata_storage.kernel_processing) == 1
