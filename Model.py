from Pathfinder import pathfind


class Player:
    def __init__(self, pl_id):
        self.walls_number = 10
        self.id = pl_id
        if self.id == 1:
            self.goal, self.pos = 0, (8, 16)
        elif self.id == 2:
            self.goal, self.pos = 16, (8, 0)

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
        self.walls = []
        self.players = []

    def can_place_wall_here(self, coord, orientation):
        if not coord[0] % 2 == 1 or not coord[1] % 2 == 1:
            return False
        if coord in self.walls:
            return False
        if orientation == 'H':
            if left(coord) in self.walls or right(coord) in self.walls or self.will_block_path(coord, orientation):
                return False
        if orientation == 'V':
            if top(coord) in self.walls or bottom(coord) in self.walls or self.will_block_path(coord, orientation):
                return False
        return True

    def get_valid_wall_places(self, orientation):
        return [[(x, y) for x in range(self.board_size) if self.can_place_wall_here((x, y), orientation)] for y in range(self.board_size)]

    def move_player(self, player, moveto):
        if moveto in (self.get_valid_moves(player.pos)):
            player.pos = moveto
        else:
            return False

    def get_valid_moves(self, coord):
        valid_moves = []
        if not self.is_at_left_edge(coord) and not self.has_wall_left(coord):
            left_coord = left_tile(coord)
            if not self.has_player(left_coord):
                valid_moves.append(left_coord)
            else:
                if not self.is_at_left_edge(left_coord) and not self.has_wall_left(left_coord) and not self.has_player(left_tile(left_coord)):
                    valid_moves.append(left_tile(left_coord))
                else:
                    if not self.is_at_top_edge(left_coord) and not self.has_wall_top(left_coord) and not self.has_player(top_tile(left_coord)):
                        valid_moves.append(top_tile(left_coord))
                    if not self.is_at_bottom_edge(left_coord) and not self.has_wall_bottom(left_coord) and not self.has_player(bottom_tile(left_coord)):
                        valid_moves.append(bottom_tile(left_coord))
        if not self.is_at_right_edge(coord) and not self.has_wall_left(coord):
            right_coord = right_tile(coord)
            if not self.has_player(right_coord):
                valid_moves.append(right_coord)
            else:
                if not self.is_at_right_edge(right_coord) and not self.has_wall_right(right_coord) and not self.has_player(right_tile(right_coord)):
                    valid_moves.append(right_tile(right_coord))
                else:
                    if not self.is_at_top_edge(right_coord) and not self.has_wall_top(right_coord) and not self.has_player(top_tile(right_coord)):
                        valid_moves.append(top_tile(right_coord))
                    if not self.is_at_bottom_edge(right_coord) and not self.has_wall_bottom(right_coord) and not self.has_player(bottom_tile(right_coord)):
                        valid_moves.append(bottom_tile(right_coord))
        if not self.is_at_top_edge(coord) and not self.has_wall_top(coord):
            top_coord = top_tile(coord)
            if not self.has_player(top_coord):
                valid_moves.append(top_coord)
            else:
                if not self.is_at_top_edge(top_coord) and not self.has_wall_top(top_coord) and not self.has_player(top_tile(top_coord)):
                    valid_moves.append(top_tile(top_coord))
                else:
                    if not self.is_at_left_edge(top_coord) and not self.has_wall_left(top_coord) and not self.has_player(left_tile(top_coord)):
                        valid_moves.append(left_tile(top_coord))
                    if not self.is_at_right_edge(top_coord) and not self.has_wall_right(top_coord) and not self.has_player(right_tile(top_coord)):
                        valid_moves.append(right_tile(top_coord))
        if not self.is_at_bottom_edge(coord) and not self.has_wall_bottom(coord):
            bottom_coord = bottom_tile(coord)
            if not self.has_player(bottom_coord):
                valid_moves.append(bottom_coord)
            else:
                if not self.is_at_bottom_edge(bottom_coord) and not self.has_wall_bottom(bottom_coord) and not self.has_player(bottom_tile(bottom_coord)):
                    valid_moves.append(bottom_tile(bottom_coord))
                else:
                    if not self.is_at_left_edge(bottom_coord) and not self.has_wall_left(bottom_coord) and not self.has_player(left_tile(bottom_coord)):
                        valid_moves.append(left_tile(bottom_coord))
                    if not self.is_at_right_edge(bottom_coord) and not self.has_wall_right(bottom_coord) and not self.has_player(right_tile(bottom_coord)):
                        valid_moves.append(right_tile(bottom_coord))
        return valid_moves

    def will_block_path(self, coord, orientation):
        if_clear = []
        player1_finish = [(f_coord, self.players[0].goal) for f_coord in range(self.board_size)]
        player2_finish = [(f_coord, self.players[1].goal) for f_coord in range(self.board_size)]
        if orientation == 'H':
            supposed_walls = list(self.walls)
            supposed_walls.extend([left(coord), coord, right(coord)])
            if_clear = self.players_have_paths(supposed_walls, player1_finish, player2_finish)
        if orientation == 'V':
            supposed_walls = list(self.walls)
            supposed_walls.extend([top(coord), coord, bottom(coord)])
            if_clear = self.players_have_paths(supposed_walls, player1_finish, player2_finish)
        if True not in if_clear[0] or True not in if_clear[1]:
            return True
        else:
            return False

    def players_have_paths(self, supposed_walls, p1_finish, p2_finish):
        p1_is_clear = []
        p2_is_clear = []
        for finish in p1_finish:
            found = pathfind(self.get_path_grid(supposed_walls), self.players[0].pos[::-1], finish[::-1])
            if found is not False:
                p1_is_clear.append(found[0])
            else:
                p1_is_clear.append(found)
        for finish in p2_finish:
            found = pathfind(self.get_path_grid(supposed_walls), self.players[1].pos[::-1], finish[::-1])
            if found is not False:
                p2_is_clear.append(found[0])
            else:
                p2_is_clear.append(found)
        return p1_is_clear, p2_is_clear

    def is_at_left_edge(self, coord):
        return coord[0] == 0

    def is_at_right_edge(self, coord):
        return coord[0] == 16

    def is_at_top_edge(self, coord):
        return coord[1] == 0

    def is_at_bottom_edge(self, coord):
        return coord[1] == 16

    def has_wall_top(self, coord):
        return (coord[0], coord[1]-1) in self.walls

    def has_wall_bottom(self, coord):
        return (coord[0], coord[1]+1) in self.walls

    def has_wall_right(self, coord):
        return (coord[0]+1, coord[1]) in self.walls

    def has_wall_left(self, coord):
        return (coord[0]-1, coord[1]) in self.walls

    def has_player(self, coord):
        for player in self.players:
            if player.pos == coord:
                return True

    def add_player(self, id):
        self.players.append(Player(id))

    def place_wall(self, player, x, y, orient):
        wall = Wall(x, y, orient)
        if self.can_place_wall_here(wall.center, wall.orientation):
            self.walls.extend(wall.all_coords)
            player.walls_number -= 1
        else:
            return False

    def get_board_grid(self):
        grid = [['T' for x in range(self.board_size)] for c in range(self.board_size)]
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if x % 2 == 1 and y % 2 == 1:
                    grid[x][y] = 'E'
                elif (x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1):
                    grid[x][y] = 'E'
                if (y, x) in self.walls:
                    grid[x][y] = 'W'
                for player in self.players:
                    if player.pos == (y, x):
                        grid[x][y] = 'P'+str(player.id)
        return grid

    def get_path_grid(self, walls):
        grid = [[1 for x in range(self.board_size)] for c in range(self.board_size)]
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if x % 2 == 1 and y % 2 == 1:
                    grid[x][y] = 0
                elif (y, x) in walls:
                    grid[x][y] = 0
        return grid

    def clear_board(self):
        self.walls = []
        self.players = []


def bottom_tile(coord):
    return tuple((coord[0], coord[1] + 2))


def top_tile(coord):
    return tuple((coord[0], coord[1] - 2))


def right_tile(coord):
    return tuple((coord[0] + 2, coord[1]))


def left_tile(coord):
    return tuple((coord[0] - 2, coord[1]))


def bottom(coord):
    return tuple((coord[0], coord[1] + 1))


def top(coord):
    return tuple((coord[0], coord[1] - 1))


def right(coord):
    return tuple((coord[0] + 1, coord[1]))


def left(coord):
    return tuple((coord[0] - 1, coord[1]))

