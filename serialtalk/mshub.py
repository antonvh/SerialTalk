from utime import sleep_ms
from hub import port

class MSHubSerial():
    READS_PER_MS = 10 # TODO: Check if it is really this fast? Maybe it is more like 0.1

    def __init__(self, port="F", baudrate=115200, power=0, **kwargs):
        # Baud rates of up to 230400 work. 115200 is the default for REPL.
        self.baudrate=baudrate # store baudrate for repl init
        self.buff = bytearray()
        if type(port) == str:
            self.uart = eval("port."+port)
        else:
            self.uart = port
        self.uart.mode(1)
        sleep_ms(300)# wait for all duplex methods to appear
        self.uart.baud(baudrate) # set baud rate
        self.uart.pwm(power)

    def any(self):
        while True:
            r=self.uart.read(1)
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
        
