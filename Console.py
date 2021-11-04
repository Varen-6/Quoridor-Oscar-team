import os


class Console:
    def __init__(self):
        self.translator_map = {
            'move':
                {
                    'x':
                        {
                            'A': 0,
                            'B': 2,
                            'C': 4,
                            'D': 6,
                            'E': 8,
                            'F': 10,
                            'G': 12,
                            'H': 14,
                            'I': 16
                        },
                    'y':
                        {
                            '1': 0,
                            '2': 2,
                            '3': 4,
                            '4': 6,
                            '5': 8,
                            '6': 10,
                            '7': 12,
                            '8': 14,
                            '9': 16
                        }
                },
            'jump':
                {
                    'x':
                        {
                            'A': 0,
                            'B': 2,
                            'C': 4,
                            'D': 6,
                            'E': 8,
                            'F': 10,
                            'G': 12,
                            'H': 14,
                            'I': 16
                        },
                    'y':
                        {
                            '1': 0,
                            '2': 2,
                            '3': 4,
                            '4': 6,
                            '5': 8,
                            '6': 10,
                            '7': 12,
                            '8': 14,
                            '9': 16
                        }
                },
            'wall':
                {
                    'x':
                        {
                            'S': 1,
                            'T': 3,
                            'U': 5,
                            'V': 7,
                            'W': 9,
                            'X': 11,
                            'Y': 13,
                            'Z': 15
                        },
                    'y':
                        {
                            '1': 1,
                            '2': 3,
                            '3': 5,
                            '4': 7,
                            '5': 9,
                            '6': 11,
                            '7': 13,
                            '8': 15
                        },
                    'orient':
                        {
                            'h': 'H',
                            'v': 'V'
                        }
                }
        }

    def translate_output(self, action, data):
        if action == 'move' or action == 'jump':
            return action + ' ' + self.get_output(action, 'x', data[0]) + self.get_output(action, 'y', data[1])
        elif action == 'wall':
            return action + ' ' + self.get_output(action, 'x', data[0]) + self.get_output(action, 'y', data[1]) + self.get_output(action, 'orient', data[2])

    def translate_input(self, action, data):
        if action == 'move' or action == 'jump':
            return self.translator_map[action]['x'][data[0]], self.translator_map[action]['y'][data[1]]
        else:
            return self.translator_map[action]['x'][data[0]], self.translator_map[action]['y'][data[1]], \
                   self.translator_map[action]['orient'][data[2]]

    def get_output(self, action, x_y_orient, value):
        return list(self.translator_map[action][x_y_orient].keys())[list(self.translator_map[action][x_y_orient].values()).index(value)]

    def cls(self):  # func to clear console output
        os.system('cls' if os.name=='nt' else 'clear')

    def console_out(self, grid):
        self.cls()
        print('┌-----------------┐')
        for j in range(len(grid)):
            printable = '|'
            for i in range(len(grid[j])):
                if grid[j][i] == 'W':
                    if j % 2 == 1:
                        printable += '—'
                    else:
                        printable += '|'
                elif grid[j][i] == 'E':
                    printable += ' '
                elif grid[j][i] == 'T':
                    printable += '·'
                elif grid[j][i] == 'P1':
                    printable += '▲'
                else:
                    printable += '▼'
            printable += '|'
            print(printable)
        print('└-----------------┘')

    def get_first_player(self, board, line):
        board.current_player = board.players[0]
        if line == "black":
            return 2
        elif line == "white":
            return 1

    def get_player_action(self, board, line):
        if line[:4] == "move":
            action = line[:4]
            data = line.split()
            if board.move_player(board.current_player, self.translate_input(action, data[1])) is False:
                raise SystemError

        elif line[:4] == "jump":
            action = line[:4]
            data = line.split()
            if board.jump_player(board.current_player, self.translate_input(action, data[1])) is False:
                raise SystemError

        elif line[:4] == "wall":
            action = line[:4]
            data = line.split()
            if board.place_wall(board.current_player, self.translate_input(action, data[1])) is False:
                raise SystemError


def bot_make_move(board):
    if board.current_player == board.players[0]:
        pass



