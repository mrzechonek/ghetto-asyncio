#!/usr/bin/env python3.5

import socket
from itertools import count


def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(16)

    print("Waiting for connections", address)
    while True:
        client, address = sock.accept()
        echo(client)


def echo(client):
    print("Client connected", address)

    for i in count(1):
        client.sendall(b"%i> " % i)
        buffer = client.recv(1024)
        if not buffer:
            break

        client.sendall(buffer)

    print("Client disconnected", address)


server(('localhost', 1234))
