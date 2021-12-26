import pyastar2d
from numpy import array, inf, float32, concatenate, append
import itertools

class Player:
    def __init__(self, pl_id):
        self.walls_number = 10
        self.id = pl_id
        if self.id == 1:
            self.goal, self.pos = 0, (8, 16)
            self.search_goal = (8, 0)
        elif self.id == 2:
            self.goal, self.pos = 16, (8, 0)
            self.search_goal = (8, 18)
        self.finishes = [(f_coord, self.goal) for f_coord in range(17) if f_coord % 2 == 0]

    def get_pos(self):
        return self.pos

    def set_name(self, name):
        if name != '':
            self.name = name

    def get_player_id(self):
        return self.id

    def has_walls(self):
        return self.walls_number > 0

    def is_winner(self):
        return self.goal == self.pos[1]


class Wall:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.center = (x, y)
        self.orientation = orientation
        if self.orientation == 'H':
            self.coord1 = (x - 1, y)
            self.coord2 = (x + 1, y)
            self.all_coords = [self.coord1, self.center, self.coord2]
        elif self.orientation == 'V':
            self.coord1 = (x, y - 1)
            self.coord2 = (x, y + 1)
            self.all_coords = [self.coord1, self.center, self.coord2]


class Board:
    def __init__(self):
        self.board_size = 17
        self.wall_bricks = []
        self.walls = []
        self.players = [Player(1), Player(2)]
        self.current_player = self.players[0]

    def can_place_wall_here(self, coord, orientation):
        if not coord[0] % 2 == 1 or not coord[1] % 2 == 1:
            return False
        if coord in self.wall_bricks:
            return False
        if orientation == 'H':
            top_wall = (top2(coord)[0], top2(coord)[1], 'V')
            bottom_wall = (bottom2(coord)[0], bottom2(coord)[1], 'V')
            left_wall = (left2(coord)[0], left2(coord)[1], 'V')
            right_wall = (right2(coord)[0], right2(coord)[1], 'V')
            top_right_wall = (right2(top2(coord))[0], right2(top2(coord))[1], 'V')
            top_left_wall = (left2(top2(coord))[0], left2(top2(coord))[1], 'V')
            bot_right_wall = (right2(bottom2(coord))[0], right2(bottom2(coord))[1], 'V')
            bot_left_wall = (left2(bottom2(coord))[0], left2(bottom2(coord))[1], 'V')
            check_walls = [top_wall, bottom_wall, left_wall, right_wall, top_right_wall, top_left_wall, bot_left_wall, bot_right_wall]
            if left(coord) in self.wall_bricks or right(coord) in self.wall_bricks:
                return False
            if any(wall in check_walls for wall in self.walls):
                if self.will_block_path(coord, orientation):
                    return False
        if orientation == 'V':
            top_wall = (top2(coord)[0], top2(coord)[1], 'H')
            bottom_wall = (bottom2(coord)[0], bottom2(coord)[1], 'H')
            left_wall = (left2(coord)[0], left2(coord)[1], 'H')
            right_wall = (right2(coord)[0], right2(coord)[1], 'H')
            top_right_wall = (right2(top2(coord))[0], right2(top2(coord))[1], 'H')
            top_left_wall = (left2(top2(coord))[0], left2(top2(coord))[1], 'H')
            bot_right_wall = (right2(bottom2(coord))[0], right2(bottom2(coord))[1], 'H')
            bot_left_wall = (left2(bottom2(coord))[0], left2(bottom2(coord))[1], 'H')
            check_walls = [top_wall, bottom_wall, left_wall, right_wall, top_right_wall, top_left_wall, bot_left_wall, bot_right_wall]
            if top(coord) in self.wall_bricks or bottom(coord) in self.wall_bricks:
                return False
            if any(wall in check_walls for wall in self.walls):
                if self.will_block_path(coord, orientation):
                    return False
        return True

    def can_place_wall_here_slow(self, coord, orientation):
        if not coord[0] % 2 == 1 or not coord[1] % 2 == 1:
            return False
        if coord in self.wall_bricks:
            return False
        if orientation == 'H':
            if left(coord) in self.wall_bricks or right(coord) in self.wall_bricks:
                return False
            if self.will_block_path(coord, orientation):
                return False
        if orientation == 'V':
            if top(coord) in self.wall_bricks or bottom(coord) in self.wall_bricks:
                return False
            if self.will_block_path(coord, orientation):
                return False
        return True

    def can_place_wall_here_without_search(self, coord, orientation):
        if not coord[0] % 2 == 1 or not coord[1] % 2 == 1:
            return False
        if coord in self.wall_bricks:
            return False
        if orientation == 'H':
            if left(coord) in self.wall_bricks or right(coord) in self.wall_bricks:
                return False
        if orientation == 'V':
            if top(coord) in self.wall_bricks or bottom(coord) in self.wall_bricks:
                return False
        return True

    def get_valid_wall_places(self, orientation):
        return [[(x, y) for x in range(self.board_size) if self.can_place_wall_here((x, y), orientation)] for y in range(self.board_size)]

    def move_player(self, player, moveto):
        if moveto in (self.get_valid_moves(player.pos)[0]):
            player.pos = moveto
            self.next_player()
        else:
            return False

    def jump_player(self, player, jumpto):
        if jumpto in (self.get_valid_moves(player.pos)[1]):
            player.pos = jumpto
            self.next_player()
        else:
            return False

    def get_valid_moves(self, coord):
        valid_moves = []
        valid_jumps = []
        if not self.is_at_top_edge(coord) and not self.has_wall_top(coord):
            top_coord = top2(coord)
            if not self.has_player(top_coord):
                valid_moves.append(top_coord)
            else:
                if not self.is_at_top_edge(top_coord) and not self.has_wall_top(top_coord) and not self.has_player(top2(top_coord)):
                    valid_jumps.append(top2(top_coord))
                else:
                    if not self.is_at_left_edge(top_coord) and not self.has_wall_left(top_coord) and not self.has_player(left2(top_coord)):
                        valid_jumps.append(left2(top_coord))
                    if not self.is_at_right_edge(top_coord) and not self.has_wall_right(top_coord) and not self.has_player(right2(top_coord)):
                        valid_jumps.append(right2(top_coord))
        if not self.is_at_left_edge(coord) and not self.has_wall_left(coord):
            left_coord = left2(coord)
            if not self.has_player(left_coord):
                valid_moves.append(left_coord)
            else:
                if not self.is_at_left_edge(left_coord) and not self.has_wall_left(left_coord) and not self.has_player(left2(left_coord)):
                    valid_jumps.append(left2(left_coord))
                else:
                    if not self.is_at_top_edge(left_coord) and not self.has_wall_top(left_coord) and not self.has_player(top2(left_coord)):
                        valid_jumps.append(top2(left_coord))
                    if not self.is_at_bottom_edge(left_coord) and not self.has_wall_bottom(left_coord) and not self.has_player(bottom2(left_coord)):
                        valid_jumps.append(bottom2(left_coord))
        if not self.is_at_right_edge(coord) and not self.has_wall_right(coord):
            right_coord = right2(coord)
            if not self.has_player(right_coord):
                valid_moves.append(right_coord)
            else:
                if not self.is_at_right_edge(right_coord) and not self.has_wall_right(right_coord) and not self.has_player(right2(right_coord)):
                    valid_jumps.append(right2(right_coord))
                else:
                    if not self.is_at_top_edge(right_coord) and not self.has_wall_top(right_coord) and not self.has_player(top2(right_coord)):
                        valid_jumps.append(top2(right_coord))
                    if not self.is_at_bottom_edge(right_coord) and not self.has_wall_bottom(right_coord) and not self.has_player(bottom2(right_coord)):
                        valid_jumps.append(bottom2(right_coord))
        if not self.is_at_bottom_edge(coord) and not self.has_wall_bottom(coord):
            bottom_coord = bottom2(coord)
            if not self.has_player(bottom_coord):
                valid_moves.append(bottom_coord)
            else:
                if not self.is_at_bottom_edge(bottom_coord) and not self.has_wall_bottom(bottom_coord) and not self.has_player(bottom2(bottom_coord)):
                    valid_jumps.append(bottom2(bottom_coord))
                else:
                    if not self.is_at_left_edge(bottom_coord) and not self.has_wall_left(bottom_coord) and not self.has_player(left2(bottom_coord)):
                        valid_jumps.append(left2(bottom_coord))
                    if not self.is_at_right_edge(bottom_coord) and not self.has_wall_right(bottom_coord) and not self.has_player(right2(bottom_coord)):
                        valid_jumps.append(right2(bottom_coord))
        return valid_moves, valid_jumps

    def will_block_path(self, coord, orientation):
        if_clear = []
        if orientation == 'H':
            supposed_walls = list(self.wall_bricks)
            supposed_walls.extend([left(coord), coord, right(coord)])
            if_clear = self.players_have_paths(supposed_walls)
        if orientation == 'V':
            supposed_walls = list(self.wall_bricks)
            supposed_walls.extend([top(coord), coord, bottom(coord)])
            if_clear = self.players_have_paths(supposed_walls)
        if not if_clear[0] or not if_clear[1]:
            return True
        else:
            return False

    def players_have_paths(self, supposed_walls):
        p1_pos = (self.players[0].pos[0], self.players[0].pos[1] + 1)
        p2_pos = (self.players[1].pos[0], self.players[1].pos[1] + 1)
        p1_weights = self.get_path_grid_walls(supposed_walls, self.players[0])
        p2_weights = self.get_path_grid_walls(supposed_walls, self.players[1])
        p1_search_end = self.players[0].search_goal
        p2_search_end = self.players[1].search_goal
        if pyastar2d.astar_path(p1_weights, p1_pos[::-1], p1_search_end[::-1]) is not None:
            p1_exist = True
        else:
            p1_exist = False
        if pyastar2d.astar_path(p2_weights, p2_pos[::-1], p2_search_end[::-1]) is not None:
            p2_exist = True
        else:
            p2_exist = False
        return p1_exist, p2_exist

    # def fastest_path_to_finish(self, player):
    #     p_pos = (player.pos[0], player.pos[1] + 1)
    #     weights = self.get_path_grid_walls(self.wall_bricks, player)
    #     p_search_end = player.search_goal
    #     shortest_path = pyastar2d.astar_path(weights, p_pos[::-1], p_search_end[::-1])
    #     if shortest_path is not None:
    #         return array([coord for coord in shortest_path if coord[0] % 2 == 0 and coord[1] % 2 == 0])
    #     else:
    #         return array([])

    def fastest_path_to_finish(self, player):
        weights = self.get_path_grid(self.wall_bricks)
        shortest_path = []
        for i in range(9):
            path = pyastar2d.astar_path(weights, player.pos[::-1], player.finishes[i][::-1])
            if path is not None:
                if shortest_path == []:
                    shortest_path = path
                elif shortest_path != [] and len(path) <= len(shortest_path):
                    shortest_path = path
        return array([coord for coord in shortest_path if coord[0] % 2 == 0 and coord[1] % 2 == 0])

    def is_at_left_edge(self, coord):
        return coord[0] == 0

    def is_at_right_edge(self, coord):
        return coord[0] == 16

    def is_at_top_edge(self, coord):
        return coord[1] == 0

    def is_at_bottom_edge(self, coord):
        return coord[1] == 16

    def has_wall_top(self, coord):
        return (coord[0], coord[1]-1) in self.wall_bricks

    def has_wall_bottom(self, coord):
        return (coord[0], coord[1]+1) in self.wall_bricks

    def has_wall_right(self, coord):
        return (coord[0]+1, coord[1]) in self.wall_bricks

    def has_wall_left(self, coord):
        return (coord[0]-1, coord[1]) in self.wall_bricks

    def has_player(self, coord):
        for player in self.players:
            if player.pos == coord:
                return True

    def next_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def place_wall(self, player, wall_data):
        wall = Wall(wall_data[0], wall_data[1], wall_data[2])
        if not self.can_place_wall_here(wall.center, wall.orientation):
            return False
        self.wall_bricks.extend(wall.all_coords)
        self.walls.append(wall_data)
        player.walls_number -= 1
        self.next_player()

    def get_board_grid(self):
        grid = [['T' for x in range(self.board_size)] for c in range(self.board_size)]
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if x % 2 == 1 and y % 2 == 1:
                    grid[x][y] = 'E'
                elif (x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1):
                    grid[x][y] = 'E'
                if (y, x) in self.wall_bricks:
                    grid[x][y] = 'W'
                for player in self.players:
                    if player.pos == (y, x):
                        grid[x][y] = 'P'+str(player.id)
        return grid

    def get_path_grid_walls(self, walls, player):
        grid = array([[1 for x in range(self.board_size)] for c in range(self.board_size+2)], dtype=float32)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if x % 2 == 1 and y % 2 == 0 and 2 <= y <= 16:
                    grid[y][x] = inf
                if (x, y) in walls:
                    grid[y+1][x] = inf
        if player.id == 1:
            grid[18] = array([inf for a in range(17)], dtype=float32)
        else:
            grid[0] = array([inf for a in range(17)], dtype=float32)
        return grid


    def get_path_grid(self, walls):
        grid = array([[1 for x in range(self.board_size)] for c in range(self.board_size)], dtype=float32)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if x % 2 == 1 and y % 2 == 1:
                    grid[y][x] = inf
                if (x, y) in walls:
                    grid[y][x] = inf
        return grid


    def clear_board(self):
        self.wall_bricks = []
        self.players = []


def bottom2(coord):
    return tuple((coord[0], coord[1] + 2))


def top2(coord):
    return tuple((coord[0], coord[1] - 2))


def right2(coord):
    return tuple((coord[0] + 2, coord[1]))


def left2(coord):
    return tuple((coord[0] - 2, coord[1]))


def bottom(coord):
    return tuple((coord[0], coord[1] + 1))


def top(coord):
    return tuple((coord[0], coord[1] - 1))


def right(coord):
    return tuple((coord[0] + 1, coord[1]))


def left(coord):
    return tuple((coord[0] - 1, coord[1]))

