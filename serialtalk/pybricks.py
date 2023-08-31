from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port


class PBSerial:
    def __init__(self, port=None, baudrate=115200, **kwargs):
        # Baud rates of up to 230400 work. 115200 is the default for REPL.
        self.baudrate = baudrate  # store baudrate for repl init
        if port is None:
            port = Port.S1
        self.uart = UARTDevice(port, baudrate)

    def any(self):
        return self.uart.waiting()

    def read(self, n=1):
        if self.uart.waiting() < n:
            return b''
        else:
            return self.uart.read(n)

    def write(self, data):
        self.uart.write(data)
