import pytest

from PyPWA.core.configurator import options
from PyPWA.core.configurator.create_config import _metadata


@pytest.fixture()
def metadata_storage():
    return _metadata.MetadataStorage()


def test_metadata_storage_finds_builtin_parser(metadata_storage):
    object = metadata_storage.search_plugin(
        "Builtin Parser", options.Types.DATA_PARSER
    )
    assert issubclass(object, options.Plugin)


def test_metadata_storage_finds_optimizers(metadata_storage):
    object = metadata_storage.request_plugins_by_type(
        options.Types.OPTIMIZER
    )
    assert len(object) == 2