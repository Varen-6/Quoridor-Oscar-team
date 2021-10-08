from random import randrange, choice



def random_bot_move(board, player):
    select = randrange(0, 2)
    if select == 0 and player.walls_number > 0:
        chosen_orient = choice(['H', 'V'])
        wall_places = []
        wall_places_raw = board.get_valid_wall_places(chosen_orient)
        for places in wall_places_raw:
            if places != []:
                wall_places.extend(places)
        placeto = choice(wall_places)
        board.place_wall(player, placeto[0], placeto[1], chosen_orient)
    elif select == 1 or player.walls_number < 0:
        board.move_player(player, choice(board.get_valid_moves(player.get_pos())))

