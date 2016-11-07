from PyPWA.builtin_plugins import process, data, minuit
from PyPWA.core.configurator import configurator


def the_real_options_test(options):
    required = options.request_options("required")
    optional = options.request_options("optional")
    advanced = options.request_options("advanced")
    template = options.request_options("template")

    assert isinstance(required, bool) or isinstance(required, dict)
    assert isinstance(optional, bool) or isinstance(optional, dict)
    assert isinstance(advanced, bool) or isinstance(advanced, dict)

    name = options.request_metadata("name")
    interface = options.request_metadata("interface")
    provides = options.request_metadata("provides")
    requires_function = options.request_metadata("user functions")

    assert isinstance(name, str)


def test_ConfiguratorOptions_AllOptionsValid():
    configurator_options = configurator.ConfiguratorOptions()
    the_real_options_test(configurator_options)


def test_MinuitOptions_AllOptionsValid():
    minuit_options = minuit.MinuitOptions()
    the_real_options_test(minuit_options)


def test_Processing_AllOptionsValid():
    processing_options = process.Processing()
    the_real_options_test(processing_options)


def test_DataParser_AllOptionsValid():
    memory_options = data.DataParser()
    the_real_options_test(memory_options)


def test_DataIterator_AllOptionsValid():
    iterator_options = data.DataIterator()
    the_real_options_test(iterator_options)
