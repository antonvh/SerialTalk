

import socket

class ClientSocketSerial():
    def __init__(self, host, port):
        self.s = socket.socket()
        # https://docs.micropython.org/en/latest/library/socket.html?highlight=socket#socket.socket.settimeout
        # socket.settimeout(value)
        # Guaranteed to return an address which can be connect'ed to for
        # stream operation.
        # Does this block??
        self.s.connect(socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0][-1])

    def write(self, data):
        num_written = 0
        while num_written < len(data):
            num_written += self.s.write(data[num_written:])

    def read(self, n=1):
        # Read 1 byte
        return self.s.read(n)

