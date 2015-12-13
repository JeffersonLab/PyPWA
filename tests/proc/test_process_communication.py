import unittest
import PyPWA.proc.process_communication


class TestProcessPipes(unittest.TestCase):
    def test(self):
        send_pipes, receive_pipes = PyPWA.proc.process_communication.ProcessPipes.return_pipes(24)

        the_list = range(100, 2500, 100)

        for index, value in enumerate(the_list):
            send_pipes[index].send(value)

        for index, value in enumerate(the_list):
            self.assertEquals(receive_pipes[index].recv(), value)