# Work in progess!!

from serialtalk import SerialTalk
from serialtalk.socketserial import ClientSocketSerial

ser = SerialTalk(ClientSocketSerial("127.0.0.1",8080))

result = ser.call('echo','do you hear me?')

print(result)