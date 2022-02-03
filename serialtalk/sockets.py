

import socket

class SocketSerial():
    def __init__(self, socket):
        self.s = socket
        self.buff = bytearray()

    def write(self, data):
        num_written = 0
        while num_written < len(data):
            num_written += self.s.send(data[num_written:])

    def read(self, n=1):
        if len(self.buff) > n:
            return self.buff.pop(n)
        else:
            try:
                extra = self.s.recv(n-len(self.buff))
            except socket.timeout:
                extra = b''
            data = extra + self.buff
            self.buff = bytearray()
            return data

    def any(self):
        while True:
            try:
                r=self.s.recv(1)
            except socket.timeout: #timeout
                break
            if r==b'': break
            self.buff += r
        return len(self.buff)

class ClientSocketSerial(SocketSerial):
    def __init__(self, host, port):
        super().__init__(socket.socket())
        
        # https://docs.micropython.org/en/latest/library/socket.html?highlight=socket#socket.socket.settimeout
        # socket.settimeout(value)
        # Guaranteed to return an address which can be connect'ed to for
        # stream operation.
        # Does this block??
        
        self.s.connect(socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0][-1])
        self.s.settimeout(0.01)

    
