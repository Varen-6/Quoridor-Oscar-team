import graphics as g


class View:
    def __init__(self):
        self.win = g.GraphWin('Quoridor', 760, 800, autoflush=False)
        self.tile_size = 40
        self.board_top_left_corner = 40
        self.p1_walls_text_pos = g.Point(190, 760)
        self.p2_walls_text_pos = g.Point(570, 760)
        self.curent_turn_text_pos = g.Point(380, 760)
        self.board_view = []
        self.for_undraw = []
        self.win_color = 'yellow'
        self.empty_wall_color = 'lightgrey'
        self.wall_color = 'brown'
        self.tile_color = 'white'
        self.p1_color = 'blue'
        self.p2_color = 'red'


    def get_empty_board(self):
        for j in range(17):
            if j % 2 == 0:
                board_row = []
                for i in range(17):
                    if i % 2 == 0:
                        tile = g.Rectangle(g.Point(self.board_top_left_corner + i * self.tile_size, self.board_top_left_corner + j * self.tile_size),
                                           g.Point(self.board_top_left_corner + i * self.tile_size + self.tile_size, self.board_top_left_corner + j * self.tile_size + self.tile_size))
                        tile.setOutline(self.tile_color)
                        tile.setFill(self.tile_color)
                        # tile.draw(self.win)
                        board_row.append(tile)
                    else:
                        empty_wall = g.Rectangle(g.Point(self.board_top_left_corner + i * self.tile_size,
                                                   self.board_top_left_corner + j * self.tile_size),
                                           g.Point(self.board_top_left_corner + i * self.tile_size + self.tile_size,
                                                   self.board_top_left_corner + j * self.tile_size + self.tile_size))
                        empty_wall.setOutline(self.empty_wall_color)
                        empty_wall.setFill(self.empty_wall_color)
                        # empty_wall.draw(self.win)
                        board_row.append(empty_wall)
                self.board_view.append(board_row)
            else:
                board_row = []
                for i in range(17):
                    empty_wall = g.Rectangle(g.Point(self.board_top_left_corner + i * self.tile_size, self.board_top_left_corner + j * self.tile_size),
                                       g.Point(self.board_top_left_corner + i * self.tile_size + self.tile_size, self.board_top_left_corner + j * self.tile_size + self.tile_size))
                    empty_wall.setOutline(self.empty_wall_color)
                    empty_wall.setFill(self.empty_wall_color)
                    # empty_wall.draw(self.win)
                    board_row.append(empty_wall)
                self.board_view.append(board_row)

    def draw_grid_numbers(self):
        for j in range(17):
            self.for_undraw.append(g.Text(g.Point(60 + j * self.tile_size, 20), str(j)).draw(self.win))
            self.for_undraw.append(g.Text(g.Point(20, 60 + j * self.tile_size), str(j)).draw(self.win))

    def get_walls(self, board):
        for wall in board.walls:
            self.board_view[wall[1]][wall[0]].setFill(self.wall_color)
            self.board_view[wall[1]][wall[0]].setOutline(self.wall_color)

    def get_players(self, board):
        for player in board.players:
            if player.id == 1:
                self.board_view[player.pos[1]][player.pos[0]].setFill(self.p1_color)
                self.board_view[player.pos[1]][player.pos[0]].setOutline(self.p1_color)
            else:
                self.board_view[player.pos[1]][player.pos[0]].setFill(self.p2_color)
                self.board_view[player.pos[1]][player.pos[0]].setOutline(self.p2_color)

    def draw_players_walls(self, board):
        p1_text = g.Text(self.p1_walls_text_pos, 'Player 1 walls left: ' + str(board.players[0].walls_number))
        p1_text.setFill(self.p1_color)
        p1_text.draw(self.win)
        p2_text = g.Text(self.p2_walls_text_pos, 'Player 2 walls left: ' + str(board.players[1].walls_number))
        p2_text.setFill(self.p2_color)
        p2_text.draw(self.win)
        self.for_undraw.extend([p1_text, p2_text])


    def draw_whose_turn(self, current_player):
        if current_player.id == 1 and not current_player.is_winner():
            current_turn_text = g.Text(self.curent_turn_text_pos, 'Turn of P1')
            current_turn_text.setFill(self.p1_color)
        elif current_player.id == 2 and not current_player.is_winner():
            current_turn_text = g.Text(self.curent_turn_text_pos, 'Turn of P2')
            current_turn_text.setFill(self.p2_color)
        else:
            current_turn_text = g.Text(self.curent_turn_text_pos, 'P{} has won!!'.format(current_player.id))
            current_turn_text.setFill(self.win_color)
        current_turn_text.draw(self.win)
        self.for_undraw.append(current_turn_text)

    def draw(self, board, current_player):
        try:
            self.undraw()
        except:
            pass
        self.get_empty_board()
        self.get_walls(board)
        self.get_players(board)
        self.draw_grid_numbers()
        self.draw_players_walls(board)
        self.draw_whose_turn(current_player)
        for row in self.board_view:
            for elem in row:
                elem.draw(self.win)
                self.for_undraw.append(elem)

    def undraw(self):
        for elem in self.for_undraw:
            elem.undraw()
        self.for_undraw = []
        self.board_view = []
