from PyPWA.libs import data, process, minuit


def check_for_data(data_object):
    data_object.request_options("required")
    data_object.request_options("optional")
    data_object.request_options("advanced")

    data_object.request_metadata("name")
    data_object.request_metadata("interface")
    data_object.request_metadata("provides")
    data_object.request_metadata("requires function")
    data_object.request_metadata("arguments")


def test_CheckDataIterator_OptionPasses():
    options = data.DataIterator()
    check_for_data(options)


def test_CheckDataParser_OptionPasses():
    options = data.DataParser()
    check_for_data(options)


def test_CheckProcess_OptionPasses():
    options = process.Processing()
    check_for_data(options)


def test_CheckMinimizer_OptionPasses():
    options = minuit.MinuitOptions()
    check_for_data(options)