#!/usr/bin/env python3.5

import select
import socket
from itertools import count

tasks = {}


def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(16)
    sock.setblocking(False)

    print("Waiting for connections", address)
    while True:
        yield sock.fileno(), select.EPOLLIN
        client, address = sock.accept()
        create_task(echo(client, address))


def echo(client, address):
    print("Client connected", address)

    for i in count():
        client.sendall(b"%i> " % i)
        yield client.fileno(), select.EPOLLIN
        buffer = client.recv(1024)
        if not buffer:
            break

        client.sendall(buffer)

    print("Client disconnected", address)


poll = select.poll()


def create_task(task):
    fileno, eventmask = task.send(None)

    tasks[fileno] = task
    poll.register(fileno, eventmask)


# "start" the server
create_task(server(('localhost', 1234)))


# start the main loop
while True:
    for fileno, event in poll.poll():
        poll.unregister(fileno)

        try:
            task = tasks.pop(fileno)
            create_task(task)
        except StopIteration:
            pass
