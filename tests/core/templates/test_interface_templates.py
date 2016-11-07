import pytest

from PyPWA.core.templates import interface_templates


def test_AllObjects_CallAbstractMethod_RaiseNotImplementedError():
    """
    Ensures that the objects will raise a NotImplementedError when called.
    """
    writer = interface_templates.WriterInterfaceTemplate("Something")
    with pytest.raises(NotImplementedError):
        writer.write(12)

    with pytest.raises(NotImplementedError):
        writer.close()

    with pytest.raises(NotImplementedError):
        with interface_templates.WriterInterfaceTemplate("Something") as \
                stream:
            stream.write("else")

    reader = interface_templates.ReaderInterfaceTemplate("Something")
    with pytest.raises(NotImplementedError):
        reader.next_event

    with pytest.raises(NotImplementedError):
        reader.previous_event

    with pytest.raises(NotImplementedError):
        with interface_templates.ReaderInterfaceTemplate("Something") as \
                stream:
            stream.reset()

    with pytest.raises(NotImplementedError):
        for event in reader:
            pass

    with pytest.raises(NotImplementedError):
        reader.reset()

    with pytest.raises(NotImplementedError):
        reader.close()

    interface = interface_templates.InterfaceTemplate()
    with pytest.raises(NotImplementedError):
        interface.run()

    with pytest.raises(NotImplementedError):
        interface.previous_value

    with pytest.raises(NotImplementedError):
        interface.stop()

    with pytest.raises(NotImplementedError):
        interface.is_alive
