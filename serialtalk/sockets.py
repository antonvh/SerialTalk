
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
        data=extra=b''
        if len(self.buff) >= n:
            data = self.buff[0:n]
            self.buff = self.buff[n:]
        else:
            while data == b'':
                try:
                    extra = self.s.recv(n-len(self.buff))
                except BlockingIOError:
                    pass
                data = extra + self.buff
                self.buff = bytearray()
        return data

    def any(self):
        while True:
            try:
                r=self.s.recv(1)
            except BlockingIOError: #timeout
                break
            if r==b'': break
            self.buff += r
        return len(self.buff)

class ClientSocketSerial(SocketSerial):
    def __init__(self, host, port):
        super().__init__(socket.socket())
        self.addr = (host, port)
        self.connect()

    def connect(self):
        self.s.close()
        # is this necessary for upython?
        # self.s.connect(socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0][-1])
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.addr)
        self.s.setblocking(0)
        self.write_done = False
    
    def write(self, data):
        # Use the socket only once for writing, then discard
        # Necessary because of blocking behavior in sockets
        # If you keep it open, it blocks after the first call
        if self.write_done:
            self.connect()
        self.write_done = True
        return super().write(data)
