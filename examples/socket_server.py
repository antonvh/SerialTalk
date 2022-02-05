
# Work in progess!!
# Test serial talk over socket
import socket
from serialtalk import SerialTalk
from serialtalk.sockets import SocketSerial

#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)
MAX_CONNECTIONS = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(MAX_CONNECTIONS)

while True:
    clientsocket, address = s.accept()
    print("{} connected!", address)
    
    st = SerialTalk(SocketSerial(clientsocket), debug=True)
    st.reply_command(*st.receive_command())

s.close()