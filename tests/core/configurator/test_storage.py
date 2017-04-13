import pytest

from PyPWA.core.configurator import storage
from PyPWA.shell import pyfit


@pytest.fixture()
def module_storage():
    return storage.Storage()


def test_module_finds_shells(module_storage):
    assert len(module_storage._get_shells()) != 0


def test_module_finds_fitter(module_storage):
    assert pyfit.ShellFitting in module_storage._get_shells()


def test_module_finds_options(module_storage):
    assert len(module_storage._get_plugins()) != 0
