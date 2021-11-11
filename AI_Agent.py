from Model import Board
from time import time
from pickle import loads, dumps
from numpy import max, array, min, inf
import itertools


class AI_Agent:
    def __init__(self, ai_player_id):
        self.chosen_action = None
        self.action_list = []
        self.max_id = ai_player_id - 1
        self.min_id = self.max_id - 1

    def score(self, state):  # Evaluation function
        return len(state.fastest_path_to_finish(state.players[self.min_id])) - len(state.fastest_path_to_finish(state.players[self.max_id]))

    def minimax(self, state, depth, alpha=-inf, beta=inf, max_player=True):  # Minimax main function
        if depth == 0:
            return self.score(state)
        if state.players[self.max_id].is_winner():
            return self.score(state) * 1.25
        if max_player:
            for action in self.get_legal_actions(state, state.current_player.id-1):
                child = self.picklecopy(state)
                self.act(child, action)
                alpha = max(array([alpha, self.minimax(child, depth-1, alpha, beta, False)]))
                if alpha >= beta or (time() - self.t) > 2:
                    break
            return alpha
        else:
            for action in self.get_legal_actions(state, state.current_player.id-1):
                child = self.picklecopy(state)
                self.act(child, action)
                beta = min(array([beta, self.minimax(child, depth-1, alpha, beta, True)]))
                if alpha >= beta or (time() - self.t) > 2:
                    break
            return beta

    def minimax_move(self, state, depth, alpha=-inf, beta=inf):  # Minimax outer that memorizes actions bot can choose
        self.t = time()
        for action in self.get_legal_actions(state, state.players[self.max_id].id-1):
            child = self.picklecopy(state)
            self.act(child, action)
            val = self.minimax(child, depth-1, alpha, beta, False)
            if val > alpha:
                alpha = val
                self.action_list.append(action)
            if alpha >= beta:
                break

    def think_and_move(self, state, depth):  # Think an action and write it to self.chosen_action
        if state.players[self.min_id].walls_number == 10:
            path = state.fastest_path_to_finish(state.current_player)
            moveto = (path[1][1], path[1][0])
            if moveto in state.get_valid_moves(state.current_player.pos)[0]:
                self.chosen_action = ("move", moveto)
                return
        self.action_list = []
        self.minimax_move(state, depth)
        for action in self.action_list[::-1]:
            if action[0] == 'wall':
                if state.can_place_wall_here((action[1][0], action[1][1]), action[1][2]):
                    self.chosen_action = action
                    break
                else:
                    pass
            else:
                self.chosen_action = action
                break

    def picklecopy(self, state):  # Makes a copy of the game state
        return loads(dumps(state))

    def act(self, state, action):  # Does the chosen move in the chosen game state
        if action[0] == 'move':
            state.move_player(state.current_player, action[1])
        elif action[0] == 'jump':
            state.jump_player(state.current_player, action[1])
        elif action[0] == 'wall':
            state.place_wall(state.current_player, action[1])

    def get_legal_actions(self, state, player):  # Gets actions that are valid for the chosen player in the chosen game state
        legal_pos_change = state.get_valid_moves(state.players[player].pos)
        legal_moves = [('move', move) for move in legal_pos_change[0]]
        legal_jumps = [('jump', jump) for jump in legal_pos_change[1]]
        if state.players[player].walls_number > 0:
            legal_walls = [('wall', wall) for wall in self.get_probable_wall_spots(state, player) if
                           state.can_place_wall_here_without_search((wall[0], wall[1]), wall[2])]
            return legal_moves+legal_jumps+legal_walls
        else: return legal_moves+legal_jumps

    def get_probable_wall_spots(self, state, player): # gets walls around enemy in radius of 2 and around itself in radius 1
        pos = state.players[player-1].pos
        my_pos = state.players[player].pos
        enemy_spot_koefs = list(itertools.product([-3, -1, 1, 3], repeat=2))
        spots = list(map(lambda spot: (pos[0] + spot[0], pos[1] + spot[1]), enemy_spot_koefs))
        nearwall_spot_coefs = [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]
        for wall in state.walls:
            spots += list(map(lambda spot: (wall[0] + spot[0], wall[1] + spot[1]), nearwall_spot_coefs))
        if state.players[player-1].walls_number > 0:
            my_spot_koefs = list(itertools.product([-1, 1], repeat=2))
            spots += list(map(lambda spot: (my_pos[0] + spot[0], my_pos[1] + spot[1]), my_spot_koefs))
        result = [(spot[0], spot[1], 'V') for spot in spots if 0 < spot[0] < 16 and 0 < spot[1] < 16] + [(spot[0], spot[1], 'H') for spot in spots if 0 < spot[0] < 16 and 0 < spot[1] < 16]
        return set(result)


def main():
    b = Board()
    ai = AI_Agent(1)
    t = time()
    ai.minimax_move(b, 4)
    print(ai.chosen_action)
    print(time()-t)


if __name__ == "__main__":
    main()