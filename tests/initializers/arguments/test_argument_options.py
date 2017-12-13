import pytest

from PyPWA.initializers.arguments import arguments_options


@pytest.fixture()
def base():
    return arguments_options.Base()


@pytest.fixture()
def plugin():
    return arguments_options.Component()


@pytest.fixture()
def main():
    return arguments_options.Program()


def test_base_setup_raises_not_implemented(base):
    with pytest.raises(NotImplementedError):
        base.setup("a parser")


def test_base_add_arguments_raises_not_implemented(base):
    with pytest.raises(NotImplementedError):
        base._add_arguments()


def test_plugin_get_interface_raises_not_implemented(plugin):
    with pytest.raises(NotImplementedError):
        plugin.setup_db("namespace")


def test_main_get_interface_raises_not_implemented(main):
    with pytest.raises(NotImplementedError):
        main.setup_db("namespace")
