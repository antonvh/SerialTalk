# Work in progess!!

from serialtalk import SerialTalk
from serialtalk.sockets import ClientSocketSerial
from time import sleep

ser = SerialTalk(ClientSocketSerial("127.0.0.1",8080))

result = ser.call('echo','read?')
print(result)
result = ser.call('echo','read?')
print(result)