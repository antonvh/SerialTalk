# Symmetrical communication library for Micropython devices

__author__ = "Anton Vanhoucke, Ste7an"
__copyright__ = "Copyright 2023, AntonsMindstorms.com"
__license__ = "GPL"
__version__ = "2023083100"  # version=<date>+<version>, with <date>=<YYYYMMDD> and <version>=00..99
__status__ = "Production"

import struct

try:
    from utime import sleep_ms
except:
    from time import sleep

    def sleep_ms(ms):
        sleep(ms / 1000)


class SerialTalkError(Exception):
    def __init__(self, message="An error occured with remote uart"):
        super().__init__(message)


class SerialTalk:
    """
    Symmetrical communication library for Micropython devices:
    use the same SerialTalk class on both sides of the serial connection.
    This library allows you to call functions on a remote device. Use
    call('some_function', arg1, arg2, ...) for this.
    You can also listen for commands on a local device. Use add_command() to add
    functions to listen for.

    :param serial_device: The serial device to use for communication. It should have a write(), read() and any() method.
    :param timeout: The timeout in milliseconds to wait for a reply, default 1500.
    :param debug: If True, print debug messages, default False.
    """

    def __init__(self, serial_device, timeout=1500, debug=False, **kwargs):
        # Kwargs for backward compatibility
        self.timeout = timeout
        self.debug = debug
        self.local_repl_enabled = False
        self.serial = serial_device
        self.commands = {}
        self.command_formats = {}
        self.version = __version__

        # Add default commands to listen for.
        self.add_command(self.enable_repl_locally, name="enable repl")
        self.add_command(self.disable_repl_locally, name="disable repl")
        self.add_command(self.echo, "repr", name="echo")
        self.add_command(self.raw_echo, name="raw echo")
        self.add_command(self.module, name="module")
        self.add_command(self.get_num_commands, "repr", name="get_num_commands")
        self.add_command(self.get_nth_command, "repr", name="get_nth_command")
        self.add_command(self.get_version, "repr", name="get_version")

        # Start clean
        self.flush()

    def info(self, *args):
        if self.debug:
            if isinstance(args, tuple):
                print(*args)
            else:
                print(args)

    def echo(self, *s):
        # Accepts multiple arguments, hence *s
        self.info("echo:", s)
        return s

    def raw_echo(self, s):
        self.info("raw echo:", s)
        return s

    def enable_repl_locally(self):
        self.local_repl_enabled = True
        if "enable_repl" in dir(self.serial):
            self.serial.enable_repl()

    def disable_repl_locally(self):
        self.local_repl_enabled = False
        if "disable_repl" in dir(self.serial):
            self.serial.disable_repl()

    def get_num_commands(self):
        return len(self.commands)

    def get_nth_command(self, n):
        if n < len(self.commands):
            return self.commands[n]
        else:
            raise SerialTalkError("get_nth_command: index exceeds number of commands")

    def get_remote_commands(self):
        cmds = []
        ack, n_cmds = self.call("get_num_commands")
        try:
            for i in range(n_cmds):
                ack, cmd = self.call("get_nth_command", "B", i)
                cmds.append(cmd)
        except:
            self.info("reload or no connection")
        return cmds

    def get_version(self):
        self.info(self.version)
        return self.version

    def add_command(self, command_function, return_format="", name=None):
        """
        Add a function or method to the list of commands that can be called from a
        remote instance of SerialTalk.

        :param command_function: The function to add.
        :type command_function: function or method
        :param return_format: The format of the return value, default "" for no return value.
        :type return_format: struct.pack format string or "repr" for returning Python objects.
        :param name: The name of the command, default None for the function name.
        :type name: str
        """
        if not name:
            name = repr(command_function).split(" ")[1]
        self.commands[name] = command_function
        self.command_formats[name] = return_format

    @staticmethod
    def encode(cmd, *argv):
        if argv:
            try:
                f = argv[0]
                if f == "raw":
                    # No encoding, raw bytes
                    s = b"\x03raw" + argv[1]
                elif f == "repr":
                    # use a pickle-like encoding to send any Python object.
                    s = b"\x04repr" + repr(argv[1:]).encode()
                else:
                    # struct pack
                    s = bytes((len(f),)) + f.encode() + struct.pack(f, *argv[1:])
            except:
                # raise
                t = type(argv[0])
                if t == bytes:
                    s = argv[0]
                elif t == str:
                    s = bytes(argv[0], "utf-8")
                elif t == int:
                    s = bytes((argv[0],))
                elif t == list:
                    s = bytes(argv[0])
                else:
                    s = b"\x01z"
        else:  # no formatstring
            s = b"\x01z"  # dummy format 'z' for no arguments
        s = (
            bytes((1 + len(cmd) + len(s),))
            + bytes((len(cmd),))
            + cmd.encode("utf-8")
            + s
        )
        # s = bytes((len(s),)) + s
        return s

    @staticmethod
    def decode(s):
        nc = s[1]  # number of bytes in command
        cmd = s[2 : 2 + nc].decode("utf-8")
        data = s[2 + nc :]
        if data == b"\x01z":
            data = None
        else:
            try:
                p = data[0] + 1
                f = data[1:p]
                if f == b"raw":  # Raw bytes, no decoding needed
                    data = data[p:]
                elif f == b"repr":
                    d = {}
                    text = data[p:].decode("utf-8")
                    if "(" in text:
                        qualname = text.split("(", 1)[0]
                        if "." in qualname:
                            pkg = qualname.rsplit(".", 1)[0]
                            mod = __import__(pkg)
                            d[pkg] = mod
                    data = eval(text, d)
                else:
                    data = struct.unpack(f, data[p:])
                if len(data) == 1:
                    # convert from tuple size 1 to single value
                    data = data[0]
            except:
                # Pass data as raw bytes
                pass
        return cmd, data

    def any(self):
        return self.serial.any()

    def read_all(self):
        # Read full receive buffer
        n = self.any()
        if n > 0:
            return self.serial.read(n)
        else:
            return b""

    def flush(self):
        d = self.read_all()
        self.info("Flushed: %r" % d)

    def force_read(self, size=1):
        # Keep reading for 'timeout' milliseconds
        # until we get data of 'size'. return None otherwise.

        data = b""
        rem = size  # remaining to be read
        j = 0
        while True:
            # Assuming that if w > 0 we don't get to read b''.
            w = self.serial.any()
            if w >= rem:
                r = self.serial.read(rem)
                data += r
                return data
            elif 0 < w < size:
                r = self.serial.read(w)
                data += r
                rem -= w
            else:  # nothing waiting
                sleep_ms(1)
                j += 1
                if j > self.timeout:
                    if data:
                        self.info(
                            "Timeout after {}ms, got {}, {} remaining".format(
                                j, data, rem
                            )
                        )
                    self.info("Nothing in force read after timeout.")
                    return

    def receive_command(self, wait=False):
        if self.local_repl_enabled:
            self.disable_repl_locally()
        # Receive a command from the other side.
        # If wait is True, wait for a command to arrive,
        # otherwise return (err,...)

        d = self.force_read(1)
        if d != b"<" and wait == False:
            return ("err", "< delimiter not found")

        # Waiting for '<' if necessary.
        while wait and d != b"<":
            d = self.force_read(1)
            sleep_ms(10)  # All the time in the world...
            self.info("Waiting for <")

        l = self.force_read(1)
        if l == None:
            return ("err", "No data length")
        pl = self.force_read(l[0])
        if pl == None:
            return ("err", "Incorrect payload lenght")
        d = self.force_read(1)
        if d != b">":
            return ("err", "> delimiter not found ({})".format(d))
        else:
            result = self.decode(l + pl)
            return result

    def send_command(self, command: str, *argv, flush=True):
        """
        Send a command to a remote host that is processing serialtalk commands.
        Does not wait for an answer.

        :param command: The command to send.
        :type command: str
        :param argv: Any number arguments to send with the command.
        """
        if self.local_repl_enabled:
            self.disable_repl_locally()
        s = self.encode(command, *argv)
        msg = b"<" + s + b">"
        if flush:
            self.flush()  # Clear the uart buffer so it's ready to pick up an answer
        self.info("Sending:", msg)
        self.serial.write(msg)

    def call(self, command: str, *args, wait=False):
        """
        Send a command to a remote host that is processing serialtalk commands.
        Wait until an answer comes or until self.timeout. Return the answer,
        or (err, ...) if there was a problem.

        :param command: The command to send.
        :type command: str
        :param args: Any number arguments to send with the command.
        :param wait: If True, wait for a reply forever, default False.
        """
        self.send_command(command, *args)
        return self.receive_command(wait=wait)

    def reply_command(self, command, value):
        # Process command(value) and send_command() with the result and an ack.
        if command in self.commands:
            try:  # executing command
                if value != None:
                    # We have a value from the other side. Pass it to our function.
                    if type(value) == tuple:
                        resp = self.commands[command](*value)
                    else:
                        resp = self.commands[command](value)
                else:
                    # Just execute the function
                    resp = self.commands[command]()
            except Exception as e:
                self.ack_err(command=command, value="Command failed: {}".format(e))
                return

            try:  # packing and sending the result
                self.ack_ok(command, fmt=self.command_formats[command], value=resp)
            except Exception as e:
                self.ack_err(
                    command=command, value="Response packing failed: {}".format(e)
                )
                return
        else:
            self.ack_err(command=command, value="Command not found: {}".format(command))

    def ack_ok(self, command="", value="ok", fmt="repr"):
        if isinstance(value, tuple):
            self.send_command(command + "ack", fmt, *value, flush=False)
        else:
            self.send_command(command + "ack", fmt, value, flush=False)

    def ack_err(self, command="", value="not ok", fmt="repr"):
        self.info("Ack Error:", value)
        self.send_command(command + "err", fmt, value, flush=False)

    def process_uart(self, *args, **kwargs):
        # Backward compatibility
        self.process()

    def process(self):
        """
        Process incoming commands. Call this in your main loop.
        It will handle incoming commands, if any, reply to them, and return.
        """
        rcv = self.receive_command(wait=False)
        self.info("Processing:", rcv)
        if rcv[0] != "err":
            self.reply_command(*rcv)

    def loop(self):
        """
        Start processing incoming commands until the repl is enabled remotely.
        (If repl is supported by the local device)
        """
        self.disable_repl_locally()
        while not self.local_repl_enabled:
            self.process_uart()

    def repl_activate(self):
        """
        Cajole the other side into a raw REPL with a lot of ctrl-c and ctrl-a.
        """
        self.flush()
        self.send_command("enable repl")
        sleep_ms(300)
        self.serial.write(b"r\x03\x03\x01")  # Ctrl-c, Ctrl-c, Ctrl-a
        sleep_ms(300)
        self.flush()
        self.serial.write(b"r\x03\x03\x01")  # Ctrl-c, Ctrl-c, Ctrl-a
        sleep_ms(10)
        data = self.read_all()
        if not data[-14:] == b"L-B to exit\r\n>":
            raise SerialTalkError("Raw REPL failed (response: %r)" % data)

    def repl_run(self, command: str, reply=True, raw_paste=True):
        """
        Execute MicroPython remotely via raw repl.
        RAW repl must be activated first! with repl_activate()

        :param command: The micropython code to execute
        :type command: str
        :param reply: If True, return the result of the command, if False, return None, default True.
        :type reply: bool
        :param raw_paste: If True, use raw paste. Turn off for more compatility, default True.
        :type raw_paste: bool
        """
        command_bytes_left = bytes(command, "utf-8")
        window = 32  # On Spike 32, on others 128. Maybe 32 works for all.

        if raw_paste:
            self.serial.write(b"\x05A\x01")  # Try raw paste
            result = self.force_read(2)
            self.info(result)
            if result == b"R\x01":
                raw_paste = True
                result = self.serial.read(
                    3
                )  # Should be b'x80\x00\x01' where \x80 is the window size
                window = result[0]
            else:
                raw_paste = False
                self.flush()

        while len(command_bytes_left) > window:
            self.serial.write(
                command_bytes_left[:window]
            )  # Write our MicroPython command and ctrl-D to execute
            sleep_ms(4)
            result = self.serial.read(1)
            command_bytes_left = command_bytes_left[window:]
        self.serial.write(command_bytes_left + b"\x04")

        if raw_paste:
            data = self.force_read(1)
            if data != b"\x04":
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
            while not len(decoded) >= 3:  # We need at least 3x'\x04'
                result += self.read_all()
                decoded = result.decode("utf-8").split("\x04")
            try:
                # The last 5 bytes are b'\r\n\x04\x04>' Between the \x04's there can be an exception.
                value, error, _ = decoded
            except:
                raise SerialTalkError("Unexpected answer from repl: {}".format(result))
            if error:
                self.info(error)
                return error.strip()  # using strip() to remove \r\n at the end.
            elif value:
                return value.strip()
            else:
                return

    def module(self, mod_bytes):
        # load module in mod_bytes; this method is remotely 'call'-ed
        # the module name is passed as as type bytes
        module = mod_bytes.decode("utf-8")
        # import module
        exec("import " + module)
        # mod_objects points to the newly imported module
        m = eval(module)
        # call the function add_commands within the imported module
        # and pass our SerialTalk instance as argument.
        # TODO: add try/except and return error if it fails.
        m.add_commands(self)

    def add_module(self, module: str):
        """
        Load a module on the remote device and
        execute `add_commands(serialtalk_instance)` within that module to
        add the module's commands to the remote command list.

        :param module: The name of the module to load.
        :type module: str
        """
        l = len(module)
        self.call("module", "%ds" % l, module.encode("utf-8"))
