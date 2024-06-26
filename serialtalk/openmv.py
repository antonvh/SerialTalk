from machine import UART
from uos import dupterm

class OpenMvSerial():    
    DUPTERM_N = 2
    READS_PER_MS = 20

    def __init__(self, port=3, baudrate=115200, **kwargs):
        self.port = port
        self.baudrate = baudrate
        self.disable_repl()

    def disable_repl(self):
        dupterm(None, self.DUPTERM_N)
        self.uart = UART(self.port, baudrate=self.baudrate,timeout_char=1)

    def enable_repl(self):
        dupterm(UART(self.port, baudrate=self.baudrate), self.DUPTERM_N)

    def any(self):
        # In the past, H7 could return 0x00,0x00 or 0x00 instead of no bytes
        # waiting = 
        # if 0 > waiting > 3:
        #     self.unprocessed_data=self.uart.read(1)
        #     if self.unprocessed_data == b'\x00':
        #         waiting = 0
        #         self.flush()
        # It seems to be better behaved now, but we'll keep this code around
        return self.uart.any()

    def read(self, n=1):
        b = self.uart.read(n)
        return b'' if b == None else b

    def write(self, data):
        return self.uart.write(data)