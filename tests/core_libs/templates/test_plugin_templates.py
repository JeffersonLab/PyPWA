import pytest

from PyPWA.core_libs.templates import plugin_templates


def test_AllObjects_CallAbstractMethod_RaiseNotImplementedError():
    """
    Ensures that the objects will raise a NotImplementedError when called.
    """

    minimizer = plugin_templates.MinimizerTemplate({"this": "that"})
    with pytest.raises(NotImplementedError):
        minimizer.main_options("function")

    with pytest.raises(NotImplementedError):
        minimizer.start()

    processing = plugin_templates.KernelProcessingTemplate(
        {"this": "that"}
    )

    with pytest.raises(NotImplementedError):
        processing.main_options("more", "less", "something")

    with pytest.raises(NotImplementedError):
        processing.fetch_interface()

    data_reader = plugin_templates.DataReaderTemplate({"this": "that"})
    with pytest.raises(NotImplementedError):
        data_reader.return_reader("the file")

    with pytest.raises(NotImplementedError):
        data_reader.return_writer("the file", 1)

    data_parser = plugin_templates.DataParserTemplate({"this": "that"})
    with pytest.raises(NotImplementedError):
        data_parser.parse("the file")

    with pytest.raises(NotImplementedError):
        data_parser.write("the data", "the file")
