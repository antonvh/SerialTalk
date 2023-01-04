from machine import UART
from uos import dupterm

class Esp32UART():
    
    DUPTERM_N = 1

    def __init__(self, port=1, baudrate=115200, rx_pin=18,tx_pin=19, **kwargs):
        self.rx_pin = rx_pin
        self.tx_pin = tx_pin
        self.port = port
        self.baudrate = baudrate
        self.disable_repl()

    def disable_repl(self):
        dupterm(None, self.DUPTERM_N)
        self.uart = UART(self.port, baudrate=self.baudrate,timeout=1, rx=self.rx_pin,tx=self.tx_pin)
        
    def enable_repl(self):
        dupterm(UART(self.port, baudrate=self.baudrate), self.DUPTERM_N)

    def any(self):
        return self.uart.any()

    def read(self, n=1):
        return self.uart.read(n)

    def write(self, data):
        return self.uart.write(data)
