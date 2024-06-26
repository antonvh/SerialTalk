from machine import UART
try:
    # Compatibility with LMS-ESP32 v2
    from lms_esp32 import RXPIN, TXPIN
except ImportError:
    RXPIN = 18
    TXPIN = 19

class Esp32UART():

    def __init__(self, port=1, baudrate=115200, rx_pin=18,tx_pin=19, **kwargs):
        self.uart = UART(port, baudrate=baudrate,timeout=1, rx=rx_pin,tx=tx_pin)

    def disable_repl(self):
        # Not supported on ESP32
        pass
        
    def enable_repl(self):
        # Not supported on ESP32
        pass

    def any(self):
        return self.uart.any()

    def read(self, n=1):
        return self.uart.read(n)

    def write(self, data):
        return self.uart.write(data)
