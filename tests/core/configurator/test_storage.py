import pytest

from PyPWA.core.configurator import storage
from PyPWA.progs.shell import fit


@pytest.fixture()
def module_storage():
    return storage.Storage()


def test_module_finds_shells(module_storage):
    assert len(module_storage._get_shells()) != 0


def test_module_finds_fitter(module_storage):
    found = False
    for plugin in module_storage._get_shells():
        if isinstance(plugin, fit.ShellFitting):
            found = True
            break
    assert found


def test_module_finds_options(module_storage):
    assert len(module_storage._get_plugins()) != 0
