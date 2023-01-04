from machine import UART, Pin
from uos import dupterm

class Esp8266UART():
    
    DUPTERM_N = 1

    def __init__(self, port=0, baudrate=115200, **kwargs):
        gpio0=Pin(0,Pin.IN)# define pin0 as input = BOOT button on board
        global interrupt_pressed
        interrupt_pressed=0
        def esp_interrupt(p):
            # called by irq on gpio0
            global interrupt_pressed
            print("Interrupt Pressed")
            dupterm(UART(0, 115200), 1) # repl with 115200baud
            interrupt_pressed=1
        gpio0.irq(trigger=Pin.IRQ_FALLING, handler=esp_interrupt)

        self.port = port
        self.baudrate = baudrate
        self.disable_repl()

    def disable_repl(self):
        dupterm(None, self.DUPTERM_N)
        self.uart = UART(self.port, baudrate=self.baudrate,timeout=1,timeout_char=1,rxbuf=100)

    def enable_repl(self):
        dupterm(UART(self.port, baudrate=self.baudrate), self.DUPTERM_N)

    def any(self):
        return self.uart.any()

    def read(self, n=1):
        return self.uart.read(n)

    def write(self, data):
        return self.uart.write(data)
