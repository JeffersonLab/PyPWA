import pytest

from PyPWA.initializers.configurator import storage
from PyPWA.progs.shell import fit


@pytest.fixture()
def module_storage():
    return storage.Storage()


def test_module_finds_shells(module_storage):
    assert len(module_storage._get_programs()) != 0


def test_module_finds_fitter(module_storage):
    found = False
    for plugin in module_storage._get_programs():
        if isinstance(plugin, fit.ShellFitting):
            found = True
            break
    assert found


def test_module_finds_options(module_storage):
    assert len(module_storage._get_components()) != 0
