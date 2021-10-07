import os


def cls(): #func to clear console output
    os.system('cls' if os.name=='nt' else 'clear')


def ask_main_menu_action():
    print('Menu:\n1. Play wih Human\n2. Play with randomizer bot\n3. Exit')


def get_menu_action():
    menu_actions = ['1', '2', '3']
    correct_input = False
    while not correct_input:
        action = input('Type suggested number to interact with menu: ')
        if action in menu_actions:
            return action
        else:
            print('Unknown action, type another: ')


def get_progress_action(board, player):
    cls()
    print('Move of Player' + str(player.get_player_id()))
    progress_actions = ['w', 'm']
    correct_input = False
    while not correct_input:
        action = input('Type \'m\' or \'w\' to choose to move or place wall: ')
        if action in progress_actions:
            if action == 'w':
                get_wall_action(board, player)
                correct_input = True
            else:
                get_move_action(board, player)
                correct_input = True
        else:
            print('Unknown action, type another:')


def get_move_action(board, player):
    move_actions = board.get_valid_moves(player.get_pos())
    correct_input = False
    while not correct_input:
        try:
            action = (int(input('Type x coordinate of tile to move to: ')), int(input('Type y coordinate of tile to move to: ')))
            if action in move_actions:
                board.move_player(player, action)
                correct_input = True
            else:
                print('Point is not reachable')
        except:
            print('Type in integers please')


def get_wall_action(board, player):
    orient = get_wall_orientation().capitalize()
    wall_actions = []
    wall_actions_raw = board.get_valid_wall_places(orient)
    for places in wall_actions_raw:
        if places != []:
            wall_actions.extend(places)
    correct_input = False
    while not correct_input:
        try:
            x = int(input('Type x coordinate where to place the wall: '))
            y = int(input('Type y coordinate where to place the wall: '))
            if (x, y) in wall_actions:
                board.place_wall(player, x, y, orient)
                correct_input = True
            else:
                print('Can`t place wall there!')
        except:
            print('Type in integers please')


def get_wall_orientation():
    orientations = ['h', 'v']
    correct_input = False
    while not correct_input:
        action = input('Type \'h\' or \'v\' to choose orientation of the wall(You won`t be able to change it until next move): ')
        if action in orientations:
            return action
        else:
            print('Unknown orientation, type another')
