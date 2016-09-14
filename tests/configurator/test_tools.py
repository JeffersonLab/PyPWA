import PyPWA.libs
from PyPWA.configurator import _tools
from PyPWA.core_libs import plugin_loader
from PyPWA.core_libs.templates import option_templates


def test_SettingsAid_SimpleDict_ValuesCorrected():
    """
    Ensures that the right values are returned for a simple dictionary
    """
    aid = _tools.SettingsAid()

    temp_dict = {
        "predetermined value": ["this", "that", "other"],
        "numbers": int,
        "exact value": float,
        "is true": bool,
        "a list": list
    }

    found_dict = {
        "predetermin value": "othr",
        "numbes": 5.001,
        "exactvalue": 2.345,
        "iss true": "tRue",
        "the list": ["list", "of", "values"]
    }

    correct = aid.correct_settings(found_dict, temp_dict)

    assert correct["predetermined value"] == "other"
    assert correct["numbers"] == 5
    assert correct["exact value"] == 2.345
    assert correct["is true"] is True
    assert correct["a list"] == ["list", "of", "values"]


def test_SettingsAid_NestedDict_ValuesCorrected():
    """
    Ensures that the right values are returned for multiple nested
    dictionaries.
    """
    aid = _tools.SettingsAid()

    temp_dict = {
        "general settings": {
            "number of threads": int,
            "debug": ["info", "debug", "warning"]
        },
        "main": {
            "settings": set,
            "data": str,
            "more nests": {
                "correct": bool
            }
        }
    }

    found_dict = {
        "General settigns": {
            "nuM of threads": 5.2,
            "debg": "inf"
        },
        "MAIN": {
            "setings": ["limit_A1", "limit_A1"],
            "daTa": "/usr/local/this",
            "moR nests": {
                "CoRRct": "tru"
            }
        }
    }

    correct = aid.correct_settings(found_dict, temp_dict)

    assert correct["general settings"]["number of threads"] == 5
    assert correct["general settings"]["debug"] == "info"
    assert correct["main"]["settings"] == {"limit_A1"}
    assert correct["main"]["data"] == "/usr/local/this"
    assert correct["main"]["more nests"]["correct"] is True


def test_MetadataStorage_LoadPluginsRandomPlugins_PluginsSorted():
    loader = plugin_loader.PluginLoading(
        option_templates.PluginsOptionsTemplate
    )

    plugin_list = loader.fetch_plugin([PyPWA.libs])

    metadata_storage = _tools.MetadataStorage()
    metadata_storage.add_plugins(plugin_list)

    assert len(metadata_storage.data_parser) == 1
    assert len(metadata_storage.data_reader) == 1
    assert len(metadata_storage.minimization) == 2
    assert len(metadata_storage.kernel_processing) == 1