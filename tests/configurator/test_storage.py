from PyPWA.configurator import _storage


def test_PluginStorage_RenderTemplate_IsDict():
    storage = _storage.PluginStorage()
    assert isinstance(storage.templates_config, dict)
