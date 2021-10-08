from Model import Board
from View import View
from Console import *
from time import sleep
from random import choice
from RandomBot import random_bot_move


class Game:
    def __init__(self):
        self.board = Board()
        self.view_shown = False
        self.state = 'MENU'
        self.winner = None
        self.win_delay = 10

    def init_window(self):
        self.view = View()
        self.view_shown = True

    def close_view(self):
        self.view.win.close()
        self.view_shown = True

    def init_players(self):
        self.board.add_player(1)
        self.board.add_player(2)

    def run(self):
        while self.state != 'QUIT':
            if self.state == 'MENU':
                cls()
                if self.view_shown:
                    self.close_view()
                ask_main_menu_action()
                menu_action = get_menu_action()
                if menu_action == '1':
                    cls()
                    self.state = "RUNNING_PvP"
                elif menu_action == '2':
                    cls()
                    self.state = "RUNNING_PvE"
                else:
                    self.state = 'QUIT'
            elif self.state == 'RUNNING_PvP':
                self.init_players()
                current_player = choice(self.board.players)
                self.init_window()
                while self.state != 'WIN':
                    self.view.draw(self.board, current_player)
                    self.progress(self.board, current_player)
                    if current_player.is_winner():
                        self.winner = current_player.get_player_id()
                        self.state = "WIN"
                    else:
                        if current_player.get_player_id() == 1:
                            current_player = self.board.players[1]
                        else:
                            current_player = self.board.players[0]
            elif self.state == 'RUNNING_PvE':
                self.init_players()
                current_player = choice(self.board.players)
                self.init_window()
                while self.state != 'WIN':
                    self.view.draw(self.board, current_player)
                    if current_player.get_player_id() == 1:
                        self.progress(self.board, current_player)
                    else:
                        random_bot_move(self.board, current_player)
                    if current_player.is_winner():
                        self.winner = current_player.get_player_id()
                        self.state = "WIN"
                    else:
                        if current_player.get_player_id() == 1:
                            current_player = self.board.players[1]
                        else:
                            current_player = self.board.players[0]

            elif self.state == 'WIN':
                '''Winning state, return to menu'''
                self.close_view()
                get_winner(self.winner)
                sleep(self.win_delay)
                self.board.clear_board()
                self.state = 'MENU'

    def progress(self, board, player):
        get_progress_action(board, player)