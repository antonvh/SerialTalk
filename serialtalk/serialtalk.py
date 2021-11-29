# Symmetrical communication library for Micropython devices
# (c) 2021 Ste7an, Anton Vanhoucke

import struct
try:
    from utime import sleep_ms
except:
    from time import sleep
    def sleep_ms(ms):
        sleep(ms/1000)

class SerialTalkError(Exception):
    def __init__(self, message="An error occured with remote uart"):
        super().__init__(message)

class SerialTalk:
    """
    Use to communicate via REPL or an RPC command loop with other devices.
    """
    commands={}
    command_formats={}
    version="Nightly"

    def __init__(self, serial_device, timeout=1500, debug=False):
        # Timeout is the time the lib waits in a receive_comand() after placing a call().
        self.timeout = timeout
        self.DEBUG = debug
        self.local_repl_enabled = False
        self.serial = serial_device
        try:
            self.reads_per_ms = serial_device.READS_PER_MS
        except:
            self.reads_per_ms = 1
        self.add_command(self.enable_repl_locally, name='enable repl')
        self.add_command(self.disable_repl_locally, name='disable repl')
        self.add_command(self.echo, 'repr', name='echo')
        self.add_command(self.raw_echo, name='raw echo')

    def echo(self, *s):
        # Accepts multiple arguments, hence *s
        if self.DEBUG: print(s)
        return s

    def raw_echo(self, s):
        if self.DEBUG: print(s)
        return s

    def enable_repl_locally(self):
        self.local_repl_enabled = True
        if 'init_repl' in dir(self.serial):
            self.serial.init_repl()

    def disable_repl_locally(self):
        self.local_repl_enabled = False
        if 'init' in dir(self.serial):
            self.serial.init()

    def add_command(self,command_function, format="", name=None):
        if not name:
            name=repr(command_function).split(" ")[1]
        self.commands[name]=command_function
        self.command_formats[name]=format

    @staticmethod
    def encode(cmd,*argv):
        if argv:
            try:
                f=argv[0]
                if f=='raw':
                    # No encoding, raw bytes
                    s=b'\x03raw'+argv[1]
                elif f=='repr':
                    # use a pickle-like encoding to send any Python object.
                    s=b'\x04repr'+repr(argv[1:]).encode()
                else:
                    # struct pack
                    s = bytes((len(f),)) + f.encode() + struct.pack(f, *argv[1:])
            except:
                # raise
                t=type(argv[0])
                if t==bytes:
                    s = argv[0]
                elif t==str:
                    s = bytes(argv[0],"utf-8")
                elif t==int:
                    s = bytes((argv[0],))
                elif t==list:
                    s = bytes(argv[0])
                else:
                    s = b'\x01z'
        else: # no formatstring
            s=b'\x01z'# dummy format 'z' for no arguments
        s = bytes((1+len(cmd)+len(s),)) + bytes((len(cmd),)) + cmd.encode('utf-8') + s
        # s = bytes((len(s),)) + s
        return s

    @staticmethod
    def decode(s):
        nc=s[1] #number of bytes in command
        cmd=s[2:2+nc].decode('utf-8')
        data=s[2+nc:]
        if data==b'\x01z':
            data=None
        else:
            try:
                p=data[0]+1
                f=data[1:p]
                if f==b"raw": # Raw bytes, no decoding needed
                    data = data[p:]
                elif f==b"repr":
                    d={}
                    text = data[p:].decode('utf-8')
                    if "(" in text:
                        qualname = text.split("(", 1)[0]
                        if "." in qualname:
                            pkg = qualname.rsplit(".", 1)[0]
                            mod = __import__(pkg)
                            d[pkg] = mod
                    data = eval(text, d)
                else:
                    data=struct.unpack(f,data[p:])
                if len(data)==1:
                    # convert from tuple size 1 to single value
                    data=data[0]
            except:
                # Pass data as raw bytes
                pass
        return cmd,data

    def read_all(self):
        # Read full receive buffer
        any = self.serial.any()
        if any:
            data = self.serial.read(any)
            return data
        else:
            return b''

    def flush(self):
        _ = self.read_all()
        if self.DEBUG: print("Flushed: %r" % _)

    def force_read(self, size=1, timeout=50):
        # Keep reading for 'timeout' milliseconds
        # until we get data of 'size'. Return b'' otherwise.
        # TODO: Declare data a bytearray of the correct length to start with
        data = b''
        r=self.serial.read(1)
        for i in range(timeout*self.reads_per_ms):
            if r==None:
                # Make sure we can add r to data, even if its None
                r=b''
            data += r
            if len(data) == size:
                return data
            else:
                r=self.serial.read(1)
            if i > 3 and self.DEBUG:
                print("Waiting for data in force read...")
        return data

    def receive_command(self,timeout=-2):
        # Set timeout to -1 to wait forever.
        if timeout == -2: timeout = self.timeout
        if self.local_repl_enabled: self.disable_repl_locally()
        delim=b''
        i=0
        while True:
            if delim==b'<': break
            elif i >= timeout*self.reads_per_ms and timeout != -1: break
            else:
                delim=self.serial.read(1)
                i+=1

        if delim!=b'<':
            err = "< delim not found after timeout of {}".format(timeout)
            if self.DEBUG: print(err)
            return ("err",err)

        payload=self.force_read(1)
        for i in range(payload[0]):
                r = self.force_read(1)
                payload+=r
        delim=self.force_read(1)

        if delim!=b'>':
            if self.DEBUG: print("Delim {}".format(delim))
            return ("err","> delim not found")
        else:
            result = self.decode(payload)
            return result

    def send_command(self,command,*argv):
        if self.local_repl_enabled: self.disable_repl_locally()
        s=self.encode(command,*argv)
        msg=b'<'+s+b'>'
        self.serial.write(msg)

    def call(self,command,*args,**kwargs):
        # Send a command to a remote host that is waiting for a call.
        # wait until an answer comes.
        # Timeout for the answer is self.timout, or passable as timeout=...
        self.send_command(command,*args)
        self.flush() # Clear the uart buffer so it's ready to pick up an answer
        return self.receive_command(**kwargs)

    def reply_command(self, command, value):
        # Process command(value) and send_command() with the result and an ack.
        if command in self.commands:
            try:  # executing command
                if value!=None:
                    if type(value)==tuple:
                        resp=self.commands[command](*value)
                    else:
                        resp=self.commands[command](value)
                else:
                    resp=self.commands[command]()
            except Exception as e:
                self.ack_err(command=command, value="Command failed: {}".format(e))
                return

            try: # packing and sensing the result
                self.ack_ok(command, fmt=self.command_formats[command], value=resp)
            except Exception as e:
                self.ack_err(command=command, value="Response packing failed: {}".format(e))
                return
        else:
            self.ack_err(command=command, value='Command not found: {}'.format(command))

    def ack_ok(self, command="", value="ok", fmt="repr"):
        command_ack=command+"ack"
        if type(value) is tuple:
            # Command has returned multiple values in a tuple. Unpack the tuple
            args=(fmt,) + value
        else:
            args=(fmt, value)
        self.send_command(command_ack, *args)

    def ack_err(self, command="", value="not ok", fmt="repr"):
        command_err=command+"err"
        if self.DEBUG: print(value)
        self.send_command(command_err,fmt,value)

    def process_uart(self, sleep=-2):
        # Answer a call if there is one:
        # Receive an incoming command
        # Process the results with any commands from commands[].
        # Reply with the answer.
        # Sleep for sleep ms after every listen.
        if sleep == -2:
            sleep = 1 # Originally this was 13 on H7 platforms.
        if self.available():
            self.reply_command(*self.receive_command())
        else:
            if self.DEBUG:
                print("Nothing available. Sleeping 1000ms")
                sleep_ms(1000)
            else:
                sleep_ms(sleep)

    def loop(self):
        # Loop forever and check for incoming calls
        # You can create a similar loop yourself and your own control code to it.
        self.disable_repl_locally()
        while not self.local_repl_enabled:
            # Until someone turns the repl back on, remotely.
            self.process_uart()

    def repl_activate(self):
        # Cajole the other side into a raw REPL with a lot of ctrl-c and ctrl-a.
        self.flush()
        self.send_command('enable repl')
        sleep_ms(300)
        self.serial.write(b"r\x03\x03\x01") # Ctrl-c, Ctrl-c, Ctrl-a
        sleep_ms(300)
        self.flush()
        self.serial.write(b"r\x03\x03\x01") # Ctrl-c, Ctrl-c, Ctrl-a
        sleep_ms(10)
        data = self.read_all()
        if not data[-14:] == b'L-B to exit\r\n>':
            raise SerialTalkError("Raw REPL failed (response: %r)" % data)

    def repl_run(self, command, reply=True, raw_paste=True):
        # Execute MicroPython remotely via raw repl.
        # RAW repl must be activated first!
        command_bytes_left = bytes(command, "utf-8")
        window = 32 # On Spike 32, on others 128. Maybe 32 works for all.

        if raw_paste:
            self.serial.write(b"\x05A\x01") # Try raw paste
            result = self.force_read(2)
            if self.DEBUG: print(result)
            if result == b'R\x01':
                raw_paste = True
                result = self.serial.read(3) # Should be b'x80\x00\x01' where \x80 is the window size
                window = result[0]
            else:
                raw_paste = False
                self.flush()

        while len(command_bytes_left) > window:
            self.serial.write(command_bytes_left[:window]) # Write our MicroPython command and ctrl-D to execute
            sleep_ms(4)
            result = self.serial.read(1)
            command_bytes_left = command_bytes_left[window:]
        self.serial.write(command_bytes_left+b'\x04')

        if raw_paste:
            data = self.force_read(1)
            if data != b'\x04':
                raise SerialTalkError("Could not send command (response: %r)" % data)
        else:
            sleep_ms(10)
            # Check if we could send command
            data = self.serial.read(2)
            if data != b"OK":
                raise SerialTalkError("Could not send command (response: %r)" % data)

        if reply:
            result = b""
            decoded = []
            while not len(decoded) >= 3: # We need at least 3x'\x04'
                result += self.read_all()
                decoded = result.decode("utf-8").split("\x04")
            try:
                value, error, _ = decoded # The last 5 bytes are b'\r\n\x04\x04>' Between the \x04's there can be an exception.
            except:
                raise SerialTalkError("Unexpected answer from repl: {}".format(result))
            if error:
                if self.DEBUG: print(error)
                return error.strip() # using strip() to remove \r\n at the end.
            elif value:
                return value.strip()
            else:
                return

