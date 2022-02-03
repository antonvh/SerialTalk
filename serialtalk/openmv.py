from machine import UART
from uos import dupterm

class OpenMvSerial():    
    DUPTERM_N = 2
    READS_PER_MS = 20

    def __init__(self, port, baudrate=115200):
        self.repl_port = port
        self.baudrate = baudrate
        self.init()

    def init(self):
        dupterm(None, self.DUPTERM_N)
        self.uart = UART(self.port, baudrate=self.baudrate,timeout_char=1)

    def init_repl(self):
        dupterm(UART(self.repl_port, baudrate=self.baudrate), self.DUPTERM_N)

    def any(self):
        # H7 can return 0x00,0x00 or 0x00 instead of no bytes
        waiting = self.uart.any()
        if 0 > waiting > 3:
            self.unprocessed_data=self.uart.read(1)
            if self.unprocessed_data == b'\x00':
                waiting = 0
                self.flush()
        return waiting