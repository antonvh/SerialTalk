
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
        # print(data)
        return data

    def any(self):
        while True:
            try:
                r=self.s.recv(1)
            except BlockingIOError: #timeout
                break
            if r==b'': break
            self.buff += r
        print(self.buff)
        return len(self.buff)

class ClientSocketSerial(SocketSerial):
    def __init__(self, host, port):
        super().__init__(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        
        # self.s.connect(socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)[0][-1])
        # self.s = socket.socket()
        self.s.connect((host, port))
        self.s.setblocking(0)
        self.read_done = False

    def read(self, n=1):
        data = super().read(n)
        self.read_done = True
        # self.s.close()
        return data
    
