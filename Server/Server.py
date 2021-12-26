import socket
from pickle import loads, dumps
from Model import Board
from Console import Console


class Server:
    def __init__(self, ip, port):
        self.buffer_size = 1024
        self.local_ip = ip
        self.local_port = port
        self.queue = []
        self.server_state = "Waiting for players"
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.bind((ip, port))
        self.console = Console()
        self.board = Board()

    def send(self, data, addr):
        self.sock.sendto(dumps(data), addr)

    def sendboard(self):
        if self.server_state == "Playing":
            curr_player = self.board.current_player.id
            if curr_player == 1:
                self.send((self.console.con_return_out(self.board.get_board_grid()), True), self.queue[0])
                self.send((self.console.con_return_out(self.board.get_board_grid()), False), self.queue[1])
            elif curr_player == 2:
                self.send((self.console.con_return_out(self.board.get_board_grid()), False), self.queue[0])
                self.send((self.console.con_return_out(self.board.get_board_grid()), True), self.queue[1])

    def recieve(self):
        data, addr = self.sock.recvfrom(self.buffer_size)
        return loads(data), addr

    def recieve_from(self, address):
        while True:
            data, addr = self.sock.recvfrom(self.buffer_size)
            if addr[0] == address[0]:
                return loads(data), addr


