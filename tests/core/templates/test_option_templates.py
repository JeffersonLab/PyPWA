import pytest

from PyPWA.core.templates import option_templates


def test_AllObjects_CallAbstractMethod_RaiseNotImplementedError():
    """
    Ensures that the objects will raise a NotImplementedError when called.
    """
    with pytest.raises(NotImplementedError):
        options = option_templates.PluginsOptionsTemplate()
        options.request_metadata("name")

    with pytest.raises(NotImplementedError):
        options = option_templates.MainOptionsTemplate()
        options.request_metadata("id")


def test_PluginOptionsTemplate_CreateMetaObject_HoldData():
    """
    Tests that the template object renders out its data correctly when
    supplied with usable information.
    """

    class TestObject(option_templates.PluginsOptionsTemplate):
        def _plugin_name(self):
            return "test"

        def _plugin_interface(self):
            return "nothing"

        def _plugin_type(self):
            return self._data_parser

        def _plugin_requires(self):

            function = """\
def function(this, that)
    return this * that"""

            return self._build_function("numpy", function)

        def _user_defined_function(self):
            return None

        def _default_options(self):
            return {
                "this": 1,
                "that": 2,
                "other": 3
            }

        def _option_levels(self):
            return {
                "this": self._required,
                "that": self._optional,
                "other": self._advanced
            }

        def _option_types(self):
            return {
                "this": bool,
                "that": int,
                "other": int
            }

        def _main_comment(self):
            return "test comment"

        def _option_comments(self):
            return {
                "this": "this",
                "that": "that",
                "other": "or other"
            }

    options = TestObject()
    assert options.request_metadata("name") == "test"
    assert options.request_metadata("interface") == "nothing"
    assert options.request_metadata("provides") == "data parser"
    assert options.request_options("required")["test"]["this"] == 1
    assert options.request_options("optional")["test"]["this"] == 1
    assert options.request_options("optional")["test"]["that"] == 2
    assert options.request_options("advanced")["test"]["other"] == 3
    assert options.request_options("advanced")["test"]["this"] == 1
    assert options.request_options("advanced")["test"]["that"] == 2

    with pytest.raises(KeyError):
        options.request_options("required")["test"]["other"] == 3


def test_MainOptionsTemplate_CreateMetaObject_HoldData():
    """
    Tests that the template object renders out its data correctly when
    supplied with usable information.
    """

    class TestObject(option_templates.MainOptionsTemplate):
        def _shell_id(self):
            return "test"

        def _main_type(self):
            return self._shell_main

        def _main_requires(self):
            return self._data_parser

        def _interface_object(self):
            return None

        def _requires_data_parser(self):
            return False

        def _requires_data_reader(self):
            return False

        def _requires_kernel_processing(self):
            return False

        def _requires_minimization(self):
            return False

        def _user_defined_function(self):
            return False

        def _default_options(self):
            return {
                "this": 1,
                "that": 2,
                "other": 3
            }

        def _option_levels(self):
            return {
                "this": self._required,
                "that": self._optional,
                "other": self._advanced
            }

        def _option_types(self):
            return {
                "this": bool,
                "that": int,
                "other": int
            }

        def _main_comment(self):
            return "test comment"

        def _option_comments(self):
            return {
                "this": "this",
                "that": "that",
                "other": "or other"
            }

    options = TestObject()
    assert options.request_metadata("id") == "test"
    assert options.request_metadata("ui") == "main shell"
    assert not options.requires("data parser")
    assert options.request_options("required")["test"]["this"] == 1
    assert options.request_options("optional")["test"]["this"] == 1
    assert options.request_options("optional")["test"]["that"] == 2
    assert options.request_options("advanced")["test"]["other"] == 3
    assert options.request_options("advanced")["test"]["this"] == 1
    assert options.request_options("advanced")["test"]["that"] == 2

    with pytest.raises(KeyError):
        options.request_options("required")["test"]["other"] == 3
