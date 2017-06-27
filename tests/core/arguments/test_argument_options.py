import pytest

from PyPWA.core.arguments import arguments_options


@pytest.fixture()
def base():
    return arguments_options.Base()


@pytest.fixture()
def plugin():
    return arguments_options.Plugin()


@pytest.fixture()
def main():
    return arguments_options.Main()


def test_base_setup_raises_not_implemented(base):
    with pytest.raises(NotImplementedError):
        base.setup("a parser")


def test_base_add_arguments_raises_not_implemented(base):
    with pytest.raises(NotImplementedError):
        base._add_arguments()


def test_plugin_get_interface_raises_not_implemented(plugin):
    with pytest.raises(NotImplementedError):
        plugin.get_interface("namespace")


def test_main_get_interface_raises_not_implemented(main):
    with pytest.raises(NotImplementedError):
        main.get_interface("namespace", {"plugins": "value"})
