
# Work in progess!!
# Test serial talk over socket
import socket

class TCPHostSocket(socket.socket):
    def __init__(self, host="127.0.0.1", port=65432):
        self.bind((host,port))
        self.listen()
        conn,addr = self.accept()

# Create host socket

# While true
    # Wait for client to connect
    # With client socket start ur.loop()
    # When socket closes, stop loop
    # Start over.