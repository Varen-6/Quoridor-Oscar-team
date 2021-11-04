from Model import Board
from time import time
from pickle import loads, dumps
from numpy import max, array, min, inf

class AI_Agent:
    def __init__(self, ai_player_id):
        self.chosen_action = None
        self.action_list = []
        self.max_id = ai_player_id - 1
        self.min_id = self.max_id - 1


    def heuristics(self, state):
        return len(state.fastest_path_to_finish(state.players[self.min_id])) - len(state.fastest_path_to_finish(state.players[self.max_id]))


    def minimax(self, state, depth, alpha=-inf, beta=inf, max_player=True):
        if depth == 0 or state.current_player.is_winner():
            return self.heuristics(state)
        if max_player:
            for action in self.get_legal_actions(state, state.current_player.id-1):
                child = self.picklecopy(state)
                self.act(child, action)
                alpha = max(array([alpha, self.minimax(child, depth-1, alpha, beta, False)]))
                if alpha >= beta:
                    break
            return alpha
        else:
            for action in self.get_legal_actions(state, state.current_player.id-1):
                child = self.picklecopy(state)
                self.act(child, action)
                beta = min(array([beta, self.minimax(child, depth-1, alpha, beta, True)]))
                if alpha >= beta:
                    break
            return beta

    def minimax_move(self, state, depth, alpha=-inf, beta=inf, max_player=True):
        if depth == 0 or state.current_player.is_winner():
            return self.heuristics(state)
        if max_player:
            for action in self.get_legal_actions(state, state.current_player.id-1):
                child = self.picklecopy(state)
                self.act(child, action)
                val = self.minimax(child, depth-1, alpha, beta, False)
                if val > alpha:
                    alpha = val
                    self.chosen_action = action
                    self.action_list.append(action)
                if alpha >= beta:
                    break
            return alpha
        else:
            for action in self.get_legal_actions(state, state.current_player.id-1):
                child = self.picklecopy(state)
                self.act(child, action)
                beta = min(array([beta, self.minimax(child, depth-1, alpha, beta, True)]))
                if alpha >= beta:
                    break
            return beta

    def think_and_move(self, state, depth):
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

    def picklecopy(self, state):
        return loads(dumps(state))

    def act(self, state, action):
        if action[0] == 'move':
            state.move_player(state.current_player, action[1])
        elif action[0] == 'jump':
            state.jump_player(state.current_player, action[1])
        elif action[0] == 'wall':
            state.place_wall(state.current_player, action[1])

    def get_legal_actions(self, state, player):
        legal_pos_change = state.get_valid_moves(state.players[player].pos)
        legal_moves = [('move', move) for move in legal_pos_change[0]]
        legal_jumps = [('jump', jump) for jump in legal_pos_change[1]]
        # legal_walls = [('wall', wall) for wall in self.get_wall_spots_around(state, player-1)]
        if state.players[player].walls_number > 0:                                                         # TO DO TESTING FOR THIS
            # legal_walls = [('wall', wall) for wall in self.get_probable_wall_spots(state, player)]
            legal_walls = [('wall', wall) for wall in self.get_probable_wall_spots(state, player) if
                           state.can_place_wall_here_without_search((wall[0], wall[1]), wall[2])]
            return legal_moves+legal_jumps+legal_walls
        else: return legal_moves+legal_jumps

    def get_probable_wall_spots(self, state, player):
        pos = state.players[player-1].pos
        my_pos = state.players[player].pos
        spots = [(pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]+1), (pos[0]-3, pos[1]-3), (pos[0]-3, pos[1]-1), (pos[0]-3, pos[1]+1), (pos[0]-3, pos[1]+3),
                 (pos[0]-1, pos[1]-3), (pos[0]+1, pos[1]-3), (pos[0]+3, pos[1]-3), (pos[0]+3, pos[1]-1), (pos[0]+3, pos[1]+1), (pos[0]+3, pos[1]+3), (pos[0]+1, pos[1]+3), (pos[0]-1, pos[1]+3)]
        # spots = [(pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]+1)]
        # for wall in state.walls:
        #     wpos = (wall[0], wall[1])
        #     spots += [(wpos[0], wpos[1]-2), (wpos[0]+2, wpos[1]), (wpos[0], wpos[1]+2), (wpos[0]-2, wpos[1])]
        if state.players[player-1].walls_number > 0:
            spots += [(my_pos[0] - 1, my_pos[1] - 1), (my_pos[0] - 1, my_pos[1] + 1), (my_pos[0] + 1, my_pos[1] - 1),(my_pos[0] + 1, my_pos[1] + 1)]
        # spots += [(my_pos[0]-1, my_pos[1]-1), (my_pos[0]-1, my_pos[1]+1), (my_pos[0]+1, my_pos[1]-1), (my_pos[0]+1, my_pos[1]+1), (pos[0]-1, pos[1]-3), (pos[0]+1, pos[1]-3), (pos[0]+1, pos[1]+3), (pos[0]-1, pos[1]+3)]
        # spots += [(my_pos[0] - 1, my_pos[1] - 1), (my_pos[0] - 1, my_pos[1] + 1), (my_pos[0] + 1, my_pos[1] - 1), (my_pos[0] + 1, my_pos[1] + 1), (my_pos[0] - 3, my_pos[1] - 3), (my_pos[0] - 3, my_pos[1] - 1), (my_pos[0] - 3, my_pos[1] + 1), (my_pos[0] - 3, my_pos[1] + 3),
        #          (my_pos[0] - 1, my_pos[1] - 3), (my_pos[0] + 1, my_pos[1] - 3), (my_pos[0] + 3, my_pos[1] - 3), (my_pos[0] + 3, my_pos[1] - 1), (my_pos[0] + 3, my_pos[1] + 1), (my_pos[0] + 3, my_pos[1] + 3), (my_pos[0] + 1, my_pos[1] + 3), (my_pos[0] - 1, my_pos[1] + 3)]
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