#!/usr/bin/env python3.5
import socket
from itertools import count

def makesocket(*address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(16)
    return sock

def server(sock):
    print("Waiting for connections", sock)
    while True:
        client, address = sock.accept()
        echo(client)

def echo(client):
    print("Client connected", client)

    for i in count():
        client.sendall(b"%i> " % i)
        text = client.recv(1024)
        if not text:
            break

        client.sendall(text)

    print("Client disconnected", client)

sock = makesocket('localhost', 1234)
server(sock)
