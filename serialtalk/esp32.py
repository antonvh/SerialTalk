from machine import UART
try:
    # Compatibility with LMS-ESP32 v2
    from lms_esp32 import RX_PIN, TX_PIN
except ImportError:
    RX_PIN = 18
    TX_PIN = 19

class Esp32UART():

    def __init__(self, port=1, baudrate=115200, rx_pin=None,tx_pin=None, **kwargs):
        if rx_pin==None:
            rx_pin=RX_PIN
        if tx_pin==None:
            tx_pin=TX_PIN
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
