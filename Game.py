from Model import Board
from Console import Console
from AI_Agent import AI_Agent

class Game:
    def __init__(self):
        self.board = Board()
        self.console = Console()

    def run(self):
        first_player = self.console.get_first_player(self.board, input())
        ai = AI_Agent(first_player)
        while True:
            if first_player == 1:
                ai.think_and_move(self.board, 2)
                ai.act(self.board, ai.chosen_action)
                print(self.console.translate_output(ai.chosen_action[0], ai.chosen_action[1]))
                self.console.get_player_action(self.board, input())
            else:
                self.console.get_player_action(self.board, input())
                ai.think_and_move(self.board, 2)
                ai.act(self.board, ai.chosen_action)
                print(self.console.translate_output(ai.chosen_action[0], ai.chosen_action[1]))
