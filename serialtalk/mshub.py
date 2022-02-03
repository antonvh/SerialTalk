from utime import sleep_ms
from hub import port

# Implement UART any(), read() and write() methods with universal behavior

class MSHubSerial():
    READS_PER_MS = 10

    def __init__(self, port_str, baudrate=115200):
        # Baud rates of up to 230400 work. 115200 is the default for REPL.
        self.baudrate=baudrate # store baudrate for repl init
        self.buff = bytearray()
        if type(port_str) == str:
            self.uart = eval("port."+port_str)
        else:
            self.uart = port_str
        self.uart.mode(1)
        sleep_ms(300)# wait for all duplex methods to appear
        self.uart.baud(baudrate) # set baud rate

    def any(self):
        while True:
            r=self.uart.read(32) #TODO test!! Was 1
            if r==b'': break
            self.buff += r
        return len(self.buff)

    def read(self,n=1):
        if len(self.buff) > n:
            return self.buff.pop(n)
        else:
            data = self.uart.read(n-len(self.buff)) + self.buff
            self.buff = bytearray()
            return data

    def write(self,data):
        window=32
        while len(data) > window:
            self.uart.write(data[:window])
            sleep_ms(5)
            data = data[window:]
        self.uart.write(data)
        
