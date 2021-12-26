import socket
from pickle import loads, dumps
from Model import Board
from Console import Console
from time import sleep
# from random import randint


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

    def end_game(self, winner_id):
        self.send(("Win", False), self.queue[winner_id-1])
        self.send(("Lose", False), self.queue[winner_id-2])
        self.queue = []
        self.console.cls()
        self.server_state = "Waiting for players"
        self.board = Board()
        self.run()

    def run(self):
        self.console.cls()
        print(f"Server is running on IP: {self.local_ip}")
        print(f"With port: {self.local_port}")
        self.wait_for_players()
        while True:
            if self.server_state == "Playing":
                if self.board.current_player.id == 1:
                    data, addr = self.recieve_from(self.queue[0])
                    if self.console.get_player_action(self.board, data):
                        if self.board.players[0].is_winner():
                            self.end_game(self.board.players[0].id)
                        self.sendboard()
                    else:
                        self.send(("MoveError", True), self.queue[0])
                elif self.board.current_player.id == 2:
                    data, addr = self.recieve_from(self.queue[1])
                    if self.console.get_player_action(self.board, data):
                        if self.board.players[1].is_winner():
                            self.end_game(self.board.players[1].id)
                        self.sendboard()
                    else:
                        self.send(("MoveError", True), self.queue[1])

    def wait_for_players(self):
        while True:
            data, addr = self.sock.recvfrom(self.buffer_size)
            if self.server_state == "Waiting for players":
                if loads(data) == "queue":
                    if len(self.queue) == 0:
                        self.queue.append(addr)
                        self.send(("approved", 1), addr)
                        print(f"Player 1 connected: {addr[0]}:{addr[1]}")
                    elif len(self.queue) == 1:
                        self.queue.append(addr)
                        self.send(("approved", 2), addr)
                        print(f"Player 2 connected: {addr[0]}:{addr[1]}")
                    if len(self.queue) == 2:
                        print("Starting game")
                        self.send("start", self.queue[0])
                        self.send("start", self.queue[1])
                        sleep(2)
                        self.server_state = "Playing"
                        self.sendboard()
                        break


def main():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    # host_ip = f"127.{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}"  # For testing
    host_port = int(input("Enter host port: "))
    server = Server(host_ip, host_port)
    server.run()


if __name__ == "__main__":
    main()
