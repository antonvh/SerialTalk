from fpioa_manager import fm
from machine import UART
from uos import dupterm

class K210Serial():
    
    DUPTERM_N = 1

    def __init__(self, baudrate=115200, rx_pin=34,tx_pin=35, **kwargs):
        fm.register(rx_pin,fm.fpioa.UART2_RX,force=True)
        fm.register(tx_pin,fm.fpioa.UART2_TX,force=True)
        self.port = port
        self.baudrate = baudrate
        self.disable_repl()

    def disable_repl(self):
        dupterm(None, self.DUPTERM_N)
        self.uart=UART(UART.UART2,self.baudrate,8,1,0,timeout=1000,read_buf_len=4096)
        
    def enable_repl(self):
        dupterm(UART(UART.UART2,self.baudrate,8,1,0,timeout=1000,read_buf_len=4096), self.DUPTERM_N)

    def any(self):
        return self.uart.any()

    def read(self, n=1):
        return self.uart.read(n)

    def write(self, data):
        return self.uart.write(data)
