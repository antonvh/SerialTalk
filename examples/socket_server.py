
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
    st = SerialTalk(SocketSerial(clientsocket))
    st.loop()

s.close()
# class TCPHostSocket(socket.socket):
#     def __init__(self, host="127.0.0.1", port=65432):
#         self.bind((host,port))
#         self.listen()
#         conn,addr = self.accept()

# Create host socket

# While true
    # Wait for client to connect
    # With client socket start ur.loop()
    # When socket closes, stop loop
    # Start over.