
MAX_PKT=15
PYBRICKS=1
ESP32=2
try:
    import pybricks
    platform=PYBRICKS
except:
    platform=ESP32

if platform==PYBRICKS:
    import ustruct as struct
    from pybricks.iodevices import PUPDevice
    from pybricks.parameters import Port
    from pybricks.tools import wait, StopWatch
else:
    import struct
    import LPF2_esp32 as LPF2

    




"""try:
    from utime import sleep_ms
except:
    from time import sleep
    def sleep_ms(ms):
        sleep(ms/1000)
"""

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

    def __init__(self, port, mode=0,timeout=1500, debug=False, **kwargs):
        # Timeout is the time the lib waits in a receive_comand() after placing a call().
        self.timeout = timeout
        self.debug = debug
        self.port = port
        
        self.mode = mode
        self.add_command(self.echo, name='echo')
        self.add_command(self.raw_echo, name='recho')
        self.add_command(self.module,name='module')
        self.add_command(self.get_version,name='version')
        self.rcv_ctr=-1
        self.snd_ctr=-1
        if platform==PYBRICKS:
            st=StopWatch()
            while st.time()<timeout:
                try:
                    self.pup=PUPDevice(self.port)
                    break
                except:
                    wait(20)
           
        if platform==ESP32:
            mode_16bytes = ['UART',[16,LPF2.DATA8,3,0],[0,1023],[0,100],[0,1023],'RAW',[LPF2.ABSOLUTE,LPF2.ABSOLUTE],False]
            modes = [mode_16bytes]
            txpin=19
            rxpin=18
            self.lpf2 = LPF2.ESP_LPF2(2, txpin,rxpin, modes, sensor_type=LPF2.SPIKE_Ultrasonic, baud=115200, timer = -1, freq = 5)    # ESP
            self.lpf2.initialize()
            self.lpf2.set_call_back(self.lpf2_callback)
        #self.add_command(self.get_num_commands,'repr',name='get_num_commands')
        #self.add_command(self.get_nth_command,'repr',name='get_nth_command')
        #self.add_command(self.get_version,'repr',name='get_version')

    def info(self, *args):
        if self.debug:
            print(args)

    def echo(self, *s):
        # Accepts multiple arguments, hence *s
        self.info(s)
        return s

    def raw_echo(self, s):
        self.info(s)
        return s

    def add_command(self,command_function, return_format="", name=None):
        if not name:
            name=repr(command_function).split(" ")[1]
        self.commands[name]=command_function
        self.command_formats[name]=return_format

    @staticmethod
    def encode(cmd,*argv):
        preamble=len(cmd)
        if argv:
            try:
                f=argv[0]
                # struct pack
                s = struct.pack(f, *argv[1:])
                preamble += (len(s)&0xf)<<4 # add upper 4 bits as len(struct)
                f=bytes(f,'utf-8')
                f = f[:-1] + bytes( (f[-1]|0x80,) ) # mark end of fmt stringf = bytes(f,'utf-8')
                s = f + s
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
                    s = b'\x00'
        else: # no argument data
            s=b''
            
        #print(s)
        s_tot = bytes((preamble,))+bytes(cmd,'utf-8') + s
        if len(s_tot)>15:
            raise Exception("Sorry, payload length exceeds 15 bytes")
        # s = bytes((len(s),)) + s
        return s_tot+b'\x00'*(MAX_PKT-len(s_tot))



    @staticmethod
    def decode(s):
        len_c=s[0]&0xf
        len_s=s[0]>>4
        #print("len_c,len_s:",len_c,len_s)
        cmd=s[1:len_c+1]#.decode('utf-8')
        data=s[len_c+1:]
        if len_s!=0: #decode struct
            try:
                # find end of fmt string (bit 7)
                len_f=0
                while (len_f<(15-len_c)) and data[len_f]&0x80==0:
                    len_f+=1
                #len_f+=1
                f=data[:len_f]+bytes((data[len_f]&0x7f,))
                #print('fmt=',f)
                #print(data[len_f+1:len_f+1+len_s])
                data=struct.unpack(f,data[len_f+1:len_f+1+len_s])
                if len(data)==1:
                    # convert from tuple size 1 to single value
                    data=data[0]
            except:
                # Pass data as raw bytes
                pass
        
        else:
            if all(d == 0 for d in data): # check for all zero's
                data=None
                return cmd,data
        
        return cmd,data
    
    def lpf2_callback(self,size,buf):
        #print('own calback',type(buf))
        #print("recv=",buf)
        buf=bytes(buf)
        self.rcv_ctr=buf[0]
        cmd,val=self.decode(buf[1:])
        #print("recv=",buf[1:])
        self.reply_command(cmd.decode(),val)
        # reply
        #lpf2.load_payload('Int8',[i for i in buf])
        pass

    
    def receive_command(self,timeout=500,reset_rcv_ctr=False):
        # Set timeout to -1 to wait forever.
        if platform==PYBRICKS:
            if reset_rcv_ctr:
                self.rcv_ctr=-1
            sw=StopWatch()
            ctr=self.rcv_ctr
            while sw.time()<timeout and ctr==self.rcv_ctr:
                raw_array=self.pup.read(self.mode)
                raw_data=bytes([i%256 for i in raw_array]) # make values unsigned
                ctr=raw_data[0]
                #print('waiting ctr recv=',ctr)
                payload=raw_data[1:]
                
            if ctr==self.rcv_ctr: # still not received new message
                return
            else:
                #print('time,ctr=',sw.time(),ctr)
                self.rcv_ctr=ctr
        result = self.decode(payload)
        return result

 
    def send_command(self,command,*argv):
        s=self.encode(command,*argv)
        if platform==PYBRICKS:
            self.snd_ctr+=1
            #print(self.snd_ctr)
            snd_msg=[self.snd_ctr]+[i for i in s]
            #print(snd_msg)
            self.pup.write(self.mode,snd_msg)
        if platform==ESP32:
            self.snd_ctr+=1
            snd_msg=[self.snd_ctr]+[i for i in s]
            self.lpf2.load_maxarray(bytearray(snd_msg))
        
    def call(self,command,*args,**kwargs):
        # Send a command to a remote host that is waiting for a call.
        # wait until an answer comes.
        # Timeout for the answer is self.timout, or passable as timeout=...
        if platform==PYBRICKS:
            # read counter before command is send
            buf=self.pup.read(self.mode)
            self.rcv_ctr=buf[0]%256
            #print('before call ctr from pup',self.rcv_ctr)
            
        self.send_command(command,*args)
        #self.flush() # Clear the uart buffer so it's ready to pick up an answer
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

    def ack_ok(self, command="", value="ok", fmt="2s"):
        command_ack=command+"a"
        if type(value) is tuple:
            # Command has returned multiple values in a tuple. Unpack the tuple
            args=(fmt,) + value
        else:
            args=(fmt, value)
        self.send_command(command_ack, *args)

    def ack_err(self, command="", value="nok", fmt="3s"):
        command_err=command+"e"
        self.info(value)
        self.send_command(command_err,fmt,value)

    def loop(self):
        # Loop forever and check for incoming calls
        # You can create a similar loop yourself and your own control code to it.
        while not self.local_repl_enabled:
            # Until someone turns the repl back on, remotely.
            self.process_uart()

    def module(self,mod_bytes):
        # load module in mod_bytes; this method is remotely 'call'-ed 
        # the module name is passed as as type bytes
        module = mod_bytes.decode('utf-8')
        # import module
        exec('import '+module)
        # mod_objects points to the newly imported module
        mod_object = eval(module)
        # call the function add_commands within the imported module
        mod_object.add_commands(self)

    def add_module(self,module):
        # this method loads a module on the remote system
        l=len(module)
        self.call('module','%ds'%l,module.encode('utf-8'))

    def get_num_commands(self):
        return len(self.commands)

    def get_nth_command(self,n):
        if n<len(self.commands):
            return self.commands[n]
        else:
            raise SerialTalkError("get_nth_command: index exceeds number of commands")

    def get_remote_commands(self):
        cmds=[]
        ack,n_cmds=self.call('get_num_commands')
        try:
            for i in range(n_cmds):
                ack,cmd=self.call('get_nth_command','B',i)
                cmds.append(cmd)
        except:
            if self.debug:
                print('reload or no connection')
        return cmds

    def get_version(self):
        version='2023010400' # version=<date>+<version>, with <date>=<YYYYMMDD> and <version>=00..99
        if self.debug:
            print(version)
        return version


def add(a,b):
    print(s.rcv_ctr)
    return a+b

def check(a):
    print(a)


from machine import I2C, Pin

i2c = I2C(1,sda=Pin(5),scl=Pin(4))
i2c.scan()

def joy():
    x,y,p=i2c.readfrom(82,3)
    return x,y,p



s=SerialTalk(1)

s.add_command(add,'H')
s.add_command(check)
s.add_command(joy,'3B')
