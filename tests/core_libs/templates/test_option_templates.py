import pytest

from PyPWA.core_libs.templates import option_templates


def test_AllObjects_CallAbstractMethod_RaiseNotImplementedError():
    """
    Ensures that the objects will raise a NotImplementedError when called.
    """
    with pytest.raises(NotImplementedError):
        options = option_templates.PluginsOptionsTemplate()
        options.request_metadata("name")


def test_TemplateOptions_CreateMetaObject_HoldData():
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

        def _plugin_arguments(self):
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
    assert options.request_metadata("name") == "test"
    assert options.request_metadata("interface") == "nothing"
    assert options.request_metadata("provides") == "data parser"
    assert options.request_metadata("arguments") is False
    assert options.request_options("required")["test"]["this"] == 1
    assert options.request_options("optional")["test"]["this"] == 1
    assert options.request_options("optional")["test"]["that"] == 2
    assert options.request_options("advanced")["test"]["other"] == 3
    assert options.request_options("advanced")["test"]["this"] == 1
    assert options.request_options("advanced")["test"]["that"] == 2

    with pytest.raises(KeyError):
        options.request_options("required")["test"]["other"] == 3
