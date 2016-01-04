import PyPWA.libs.proc.process_communication


def test_process_pipes():
    send_pipes, receive_pipes = PyPWA.libs.proc.process_communication.ProcessPipes.return_pipes(24)

    the_list = range(100, 2500, 100)

    for index, value in enumerate(the_list):
        send_pipes[index].send(value)

    for index, value in enumerate(the_list):
        assert receive_pipes[index].recv() == value
