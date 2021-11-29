from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port

class PBSerial():
    def any(self):
        return self.uart.waiting()