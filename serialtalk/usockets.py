# micropython implementation of sockets
import socket

class SocketSerial():
    def __init__(self, sock):
        self.s = sock
        self.buff = bytearray()

    def write(self, data):
        num_written = 0
        while num_written < len(data):
            num_written += self.s.write(data[num_written:])

    def read(self, n=1):
        data=extra=b''
        if len(self.buff) >= n:
            data = self.buff[0:n]
            self.buff = self.buff[n:]
        else:
            try:
                extra = self.s.recv(n-len(self.buff))
            except OSError:
                pass
            data = extra + self.buff
            self.buff = bytearray()
        return data

    def any(self):
        while True:
            try:
                r=self.s.read(1)
            except OSError as e: #timeout
                break
            if r==None: break
            self.buff += r
        return len(self.buff)


class ClientSocketSerial(SocketSerial):
    def __init__(self, host, port):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        self.s.close()
        self.s = socket.socket()
        self.s.connect(socket.getaddrinfo(self.host, self.port, 0, socket.SOCK_STREAM)[0][-1])
        self.s.settimeout(0)
        self.buff = bytearray()
        self.write_done = False

    def write(self, data):
        # Use the socket only once for writing, then discard
        # Necessary because of blocking behavior in sockets
        # If you keep it open, it blocks after the first call
        if self.write_done:
            self.connect()
        self.write_done = True
        return super().write(data)