#!/usr/bin/env python3.5

import select
import socket
from itertools import count

tasks = {}


def sock_accept(sock):
    yield sock.fileno(), select.EPOLLIN
    return sock.accept()


def sock_recv(sock, nbytes):
    yield sock.fileno(), select.EPOLLIN
    return sock.recv(1024)


def sock_sendall(sock, buffer):
    while buffer:
        yield sock.fileno(), select.EPOLLOUT
        written = sock.send(buffer)
        buffer = buffer[written:]


def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(16)
    sock.setblocking(False)

    print("Waiting for connections", address)
    while True:
        client, address = yield from sock_accept(sock)
        create_task(echo(client, address))


def echo(client, address):
    print("Client connected", address)

    for i in count(1):
        yield from sock_sendall(client, b"%i> " % i)
        buffer = yield from sock_recv(client, 1024)
        if not buffer:
            break

        yield from sock_sendall(client, buffer)

    print("Client disconnected", address)


poll = select.poll()


def create_task(task):
    fileno, eventmask = task.send(None)

    tasks[fileno] = task
    poll.register(fileno, eventmask)

create_task(server(('localhost', 1234)))

while tasks:
    for fileno, event in poll.poll():
        poll.unregister(fileno)

        try:
            task = tasks.pop(fileno)
            create_task(task)
        except StopIteration:
            pass
