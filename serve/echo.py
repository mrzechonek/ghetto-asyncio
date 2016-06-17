import socket
from itertools import count


__all__ = ('server', )


def server(loop, address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(16)
    sock.setblocking(False)

    print("Waiting for connections", address)
    while True:
        client, address = yield from loop.sock_accept(sock)
        loop.create_task(echo(loop, client, address))


def echo(loop, client, address):
    print("Client connected", address)

    for i in count(1):
        yield from loop.sock_sendall(client, b"%i> " % i)
        buffer = yield from loop.sock_recv(client, 1024)
        if not buffer:
            break

        yield from loop.sock_sendall(client, buffer)

    print("Client disconnected", address)
