import pytest

from PyPWA.core.shared.interfaces import internals


@pytest.fixture
def reader():
    return internals.Reader()


@pytest.fixture
def writer():
    return internals.Writer()


@pytest.fixture(params=[internals.Reader, internals.Writer])
def writer_and_reader(request):
    return request.param


@pytest.fixture
def kernel():
    return internals.Kernel()


@pytest.fixture
def kernel_interface():
    return internals.KernelInterface()


@pytest.fixture
def minimization_option_parser():
    return internals.MinimizerOptionParser()


@pytest.fixture
def process_interface():
    return internals.ProcessInterface()


def test_reader_can_iterate(reader):
    with pytest.raises(NotImplementedError):
        for event in reader:
            pass


def test_standard_reader_close(reader):
    with pytest.raises(NotImplementedError):
        reader.close()


def test_standard_writer_close(writer):
    with pytest.raises(NotImplementedError):
        writer.close()


def test_can_enter(writer_and_reader):
    with pytest.raises(NotImplementedError):
        with writer_and_reader():
            pass


def test_process_interface_run(process_interface):
    with pytest.raises(NotImplementedError):
        process_interface.run()


def test_process_interface_previous_value(process_interface):
    with pytest.raises(NotImplementedError):
        process_interface.previous_value


def test_process_interface_stop(process_interface):
    with pytest.raises(NotImplementedError):
        process_interface.stop()


def test_process_interface_is_alive(process_interface):
    with pytest.raises(NotImplementedError):
        process_interface.is_alive


def test_kernel_process_id(kernel):
    assert kernel.processor_id is None


def test_kernel_setup(kernel):
    with pytest.raises(NotImplementedError):
        kernel.setup()


def test_kernel_process(kernel):
    with pytest.raises(NotImplementedError):
        kernel.process()


def test_kernel_interface_is_duplex(kernel_interface):
    assert isinstance(kernel_interface.is_duplex, bool)


def test_kernel_interface_run(kernel_interface):
    with pytest.raises(NotImplementedError):
        kernel_interface.run("Send", [1, 2])


def test_option_parser_convert_not_implemented(minimization_option_parser):
    with pytest.raises(NotImplementedError):
        minimization_option_parser.convert([1, 2, 3])
