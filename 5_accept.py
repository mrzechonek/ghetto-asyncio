#!/usr/bin/env python3.5

import socket

address = ('localhost', 1234)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(address)
sock.listen(16)

print("Waiting for connections", address)

while True:
    client, address = sock.accept()
    print("Client connected", address)
