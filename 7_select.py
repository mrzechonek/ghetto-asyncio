#!/usr/bin/env python3.5
import select
import socket
from itertools import count

tasks = {}
poll = select.poll()

def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(16)
    sock.setblocking(False)

    print("Waiting for connections", address)
    while True:
        yield
        client, address = sock.accept()
        task = echo(client)
        next(task)
        tasks[client.fileno()] = task

def echo(client):
    print("Client connected", address)

    for i in count():
        client.sendall(b"%i> " % i)
        yield
        buffer = client.recv(1024)
        if not buffer:
            break

        client.sendall(buffer)

    print("Client disconnected", address)

# start the server
tasks[sock.fileno()] = server(('localhost', 1234))

# main loop
while True:
    for fileno, task in tasks.items():
        poll.register(fileno, select.EPOLLIN)

    for fileno, event in poll.poll():
        poll.unregister(fileno)

        try:
            tasks[fileno].send(None)
        except StopIteration:
            pass
