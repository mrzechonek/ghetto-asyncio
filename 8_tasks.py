#!/usr/bin/env python3.5
import select
import socket
from itertools import count

tasks = {}
poll = select.poll()

def makesocket(*address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(16)
    sock.setblocking(False)

    return sock

def server(sock):
    print("Waiting for connections", sock)
    while True:
        yield sock.fileno(), select.EPOLLIN
        client, address = sock.accept()

        create_task(echo(client))

def echo(client):
    print("Client connected", client)

    for i in count():
        yield client.fileno(), select.EPOLLOUT
        client.sendall(b"%i> " % i)

        yield client.fileno(), select.EPOLLIN
        buffer = client.recv(1024)

        if not buffer:
            break

        client.sendall(buffer)

    print("Client disconnected", client)

def create_task(task):
    fileno, eventmask = next(task)

    tasks[fileno] = task
    poll.register(fileno, eventmask)

# "start" the server
create_task(server(makesocket('localhost', 1234)))

# main loop
while True:
    for fileno, event in poll.poll():
        poll.unregister(fileno)

        try:
            task = tasks.pop(fileno)
            create_task(task)
        except StopIteration:
            pass
