import pytest

from PyPWA.core.shared.interfaces import plugins


@pytest.fixture
def minimizer():
    return plugins.Optimizer()


@pytest.fixture
def kernel_processing():
    return plugins.KernelProcessing()


@pytest.fixture
def data_parser():
    return plugins.DataParser()


@pytest.fixture
def data_iterator():
    return plugins.DataIterator()


@pytest.fixture
def main():
    return plugins.Main()


def test_minimizer_main_options_raise_not_implemented(minimizer):
    with pytest.raises(NotImplementedError):
        minimizer.main_options("Function Here", "ChiSquared")


def test_minimizer_start_raise_not_implemented(minimizer):
    with pytest.raises(NotImplementedError):
        minimizer.start()


def test_minimizer_return_parser_raise_not_implemented(minimizer):
    with pytest.raises(NotImplementedError):
        minimizer.return_parser()


def test_minimizer_save_extra_raise_not_implemented(minimizer):
    with pytest.raises(NotImplementedError):
        minimizer.save_extra("ChiSquared")


def test_kernel_proc_main_options_raise_not_implemented(kernel_processing):
    with pytest.raises(NotImplementedError):
        kernel_processing.main_options("Data", "Template", "Another Temp")


def test_kernel_proc_fetch_interface_raise_not_implemented(kernel_processing):
    with pytest.raises(NotImplementedError):
        kernel_processing.fetch_interface()


def test_data_parser_parse_raise_not_implemented(data_parser):
    with pytest.raises(NotImplementedError):
        data_parser.parse("file")


def test_data_parser_write_raise_not_implemented(data_parser):
    with pytest.raises(NotImplementedError):
        data_parser.write("file", "data")


def test_data_iterator_return_reader_raise_not_implemented(data_iterator):
    with pytest.raises(NotImplementedError):
        data_iterator.return_reader("File")


def test_data_iterator_return_writer_raise_not_implemented(data_iterator):
    with pytest.raises(NotImplementedError):
        data_iterator.return_writer("File", "shape")


def test_main_start_raises_not_implemented(main):
    with pytest.raises(NotImplementedError):
        main.start()
