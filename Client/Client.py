import socket
from pickle import loads, dumps
import os

class Client:
    def __init__(self):
        self.buffer_size = 1024
        hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(hostname)
        self.local_port = 5005
        self.client_state = "NotConnected"
        self.server_ip = "127.0.0.1"

    def cls(self):  # func to clear console output
        os.system('cls' if os.name=='nt' else 'clear')

    def send(self, data, addr):
        self.sock.sendto(dumps(data), addr)

    def recieve(self):
        data, addr = self.sock.recvfrom(self.buffer_size)
        return loads(data), addr

    def connect(self):
        self.local_port = int(input("Enter server port:"))
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.local_ip, self.local_port))

