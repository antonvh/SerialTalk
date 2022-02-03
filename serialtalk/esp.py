# TODO: make this interrupt communicate with SerialTalk....
# from machine import Pin
# gpio0=Pin(0,Pin.IN)# define pin0 as input = BOOT button on board
# gpio0.irq(trigger=Pin.IRQ_FALLING, handler=esp_interrupt)
# def esp_interrupt():
#   ...
from machine import UART
from uos import dupterm
class EspSerial():
    
    DUPTERM_N = 1

    def __init__(self, port, baudrate=115200):
        self.repl_port = port
        self.baudrate = baudrate
        self.init()

    def init(self):
        dupterm(None, self.DUPTERM_N)
        self.uart = UART(self.port, baudrate=self.baudrate,timeout=1,timeout_char=1,rxbuf=100)

    def init_repl(self):
        dupterm(UART(self.repl_port, baudrate=self.baudrate), self.DUPTERM_N)

    def any(self):
        return self.uart.any()

    def read(self):
        pass
