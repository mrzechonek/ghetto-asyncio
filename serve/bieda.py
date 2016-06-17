#!/usr/bin/python3.5


import select


class MainLoop:
    def __init__(self):
        self.tasks = {}
        self.poll = select.poll()

    def sock_accept(self, sock):
        yield sock, select.POLLIN
        return sock.accept()

    def sock_recv(self, sock, nbytes):
        yield sock, select.POLLIN
        return sock.recv(nbytes)

    def sock_sendall(self, sock, buffer):
        while buffer:
            yield sock, select.POLLOUT
            written = sock.send(buffer)
            buffer = buffer[written:]

    def create_task(self, task):
        sock, eventmask = task.send(None)
        fileno = sock.fileno()

        self.tasks[fileno] = task
        self.poll.register(fileno, eventmask)

    def run_forever(self):
        while self.tasks:
            for fileno, event in self.poll.poll():
                self.poll.unregister(fileno)

                try:
                    task = self.tasks.pop(fileno)
                    self.create_task(task)
                except Exception:
                    pass


_loop = MainLoop()


def get_event_loop():
    return _loop

