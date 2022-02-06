from serial import Serial

class Py3Serial():
    
    DUPTERM_N = 1

    def __init__(self, port="/dev/tty.AMA0", baudrate=115200, **kwargs):
        self.port = port
        self.uart = Serial(port, baudrate, timeout=1)
        self.baudrate = baudrate

    def any(self):
        return self.uart.any()

    def read(self, n=1):
        return self.uart.read(n)

    def write(self, data):
        return self.uart.write(data)
