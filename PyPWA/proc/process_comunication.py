from abc import ABCMeta, abstractmethod
import multiprocessing

class ProcessPipes(object):

    def return_pipes(self, num_pipes):
        send_to = []
        recieve_from = []

        for x in range(num_pipes):
            recieve, send = multiprocessing.Pipe(False)
            send_to.append(send)
            recieve_from(recieve)
        return [ send_to, recieve_from ]

class

class UnidirectionalPipes(object):
