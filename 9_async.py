#!/usr/bin/env python3.5
import select
import socket
from itertools import count

tasks = {}
poll = select.poll()

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
        client, address = yield from sock_accept(sock)
        create_task(echo(client))

def echo(client):
    print("Client connected", client)

    for i in count(1):
        yield from sock_sendall(client, b"%i> " % i)
        buffer = yield from sock_recv(client, 1024)
        if not buffer:
            break

        yield from sock_sendall(client, buffer)

    print("Client disconnected", client)

def create_task(task):
    fileno, eventmask = next(task)

    tasks[fileno] = task
    poll.register(fileno, eventmask)

# "start" the server
create_task(server(makesocket('localhost', 1234)))

# main loop
while tasks:
    for fileno, event in poll.poll():
        poll.unregister(fileno)

        try:
            task = tasks.pop(fileno)
            create_task(task)
        except StopIteration:
            pass
