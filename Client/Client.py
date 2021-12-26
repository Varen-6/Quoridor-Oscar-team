import socket
from pickle import loads, dumps
import os
import sys


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
        if addr[0] == self.server_ip:
            return loads(data), addr
        else:
            self.recieve()

    def connect(self):
        while True:
            if self.client_state == "NotConnected":
                self.server_ip = input("Enter server IP:")
                self.local_port = int(input("Enter server port:"))
                self.sock = socket.socket(socket.AF_INET,  # Internet
                                          socket.SOCK_DGRAM)  # UDP
                self.sock.bind((self.local_ip, self.local_port))
                self.server_addr = (self.server_ip, self.local_port)
                self.send("queue", self.server_addr)
                self.client_state = "Connecting"
            elif self.client_state == "Connecting":
                msg, addr = self.recieve()
                if msg[0] == "approved":
                    self.player_id = msg[1]
                    self.client_state = "Connected"
            elif self.client_state == "Connected":
                print(f"Connected successfully, waiting for the game to start")
                srvr_msg = self.recieve()[0]
                if srvr_msg == "start":
                    self.client_state = "Playing"
                    break

    def client_output(self, data):
        self.cls()
        if data[1]:
            print("Your move!")
        elif not data[1]:
            print("Wait for opponent to make move.")
        print(data[0])

    def run(self):
        self.cls()
        self.connect()
        while True:
            if self.client_state == "Playing":
                data = self.recieve()[0]
                if data[0] == "Win":
                    self.cls()
                    if input("You WON! Do you want to enter a new queue?\n(\"y\" for yes, any other symbol for exit):") == "y":
                        self.client_state = "NotConnected"
                        self.run()
                    else:
                        sys.exit()
                if data[0] == "Lose":
                    self.cls()
                    if input("You LOST! Do you want to enter a new queue?\n(\"y\" for yes, any other symbol for exit):") == "y":
                        self.client_state = "NotConnected"
                        self.run()
                    else:
                        sys.exit()
                if data[0] == "MoveError":
                    print("Wrong move!")
                else:
                    self.client_output(data)
                if data[1]:
                    action = input("Make your move:")
                    self.send(action, self.server_addr)


client = Client()
client.run()
