import pytest

from PyPWA.configurator import templates


def test_AllObjects_CallAbstractMethod_RaiseNotImplementedError():
    """
    Ensures that the objects will raise a NotImplementedError when called.
    """
    with pytest.raises(NotImplementedError):
        options = templates.TemplateOptions()
        options.request_metadata("name")

    minimizer = templates.MinimizerTemplate()
    with pytest.raises(NotImplementedError):
        minimizer.configurator_options("this or that")

    with pytest.raises(NotImplementedError):
        minimizer.main_options("that")

    with pytest.raises(NotImplementedError):
        minimizer.start()

    processing = templates.KernelProcessingTemplate()
    with pytest.raises(NotImplementedError):
        processing.configurator_options("options")

    with pytest.raises(NotImplementedError):
        processing.main_options("more", "less", "something")

    data_reader = templates.DataReaderTemplate()
    with pytest.raises(NotImplementedError):
        data_reader.return_reader("the file")

    with pytest.raises(NotImplementedError):
        data_reader.return_writer("the file")

    data_parser = templates.DataParserTemplate()
    with pytest.raises(NotImplementedError):
        data_parser.parse_data("the file")

    with pytest.raises(NotImplementedError):
        data_parser.write_data("the data", "the file")


def test_TemplateOptions_CreateMetaObject_HoldData():
    """
    Tests that the template object renders out its data correctly when
    supplied with usable information.
    """

    class TestObject(templates.TemplateOptions):
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
