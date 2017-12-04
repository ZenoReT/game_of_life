#!/usr/bin/env python3
"""Console version of <Game Of Life>"""
import sys
import argparse
from sys import argv
from modules import game
from modules import utils
parser = argparse.ArgumentParser()

game_field = game.Field(25, 25, "boundary")
help_dict = {'g': 'generate game field',
             'k': 'clear field and make all cells are dead',
             'ps': 'get previous state of field',
             'phm': 'print heat map on console',
             'ns': 'get next state of field',
             'pf': 'print field on console',
             'chr': 'change heat range (> 0)',
             'cld': 'change life density for next generation (0 - 100%)',
             'ct': 'change type of game (obsessed boundary endless)',
             'cs': 'change size of field (x, y > 3)',
             'ccs': 'change cell state (x, y on field, state: dead, alive)'}


def main():
    args = sys.argv[1:]
    basic_commands_comparer = {'g': game_field.generate,
                               'k': game_field.kill_life,
                               'ps': game_field.previous_field,
                               'phm': print_heat_map,
                               'ns': game_field.next_step,
                               'pf': print_field}
    commands_with_one_arg_comparer = {'chr': change_heat_range,
                                      'cld': change_life_density,
                                      'ct': change_type}
    commands_with_two_args_comparer = {'cs': change_size}
    commands_with_three_args_comparer = {'ccs': change_cell_state}
    comparers = (basic_commands_comparer, commands_with_one_arg_comparer,
                 commands_with_two_args_comparer,
                 commands_with_three_args_comparer)
    while len(args) != 0:
        treat_args(args, comparers)
        print('------------------------\n\
               \rcurrent size: {0} {1}\n\
               \rcurrent_type: {2}\n\
               \rcurrent heat range: {3}\n\
               \rcurrent life density: {4}\n\
               \r------------------------'.format(game_field.x_size,
                                                  game_field.y_size,
                                                  game_field.game_type,
                                                  game_field.heat_range,
                                                  game_field.life_density))
        args = input('Input new args: ').rsplit()
    return


def treat_args(args, comparers):
    key_id = 0
    while key_id < len(args):
        key = args[key_id].lower()
        if key in comparers[0]:
            comparers[0][args[key_id]]()
        elif key in comparers[1]:
            print(key_id)
            try:
                comparers[1][key](args[key_id + 1])
            except:
                print('there are not enough arguments for this key: {0}'
                      .format(key))
                break
            key_id += 1
            print(key_id)
        elif key in comparers[2]:
            try:
                comparers[2][key](args[key_id + 1], args[key_id + 2])
            except:
                print('there are not enough arguments for this key: {0}'
                      .format(key))
                break
            key_id += 2
        elif key in comparers[3]:
            try:
                comparers[3][key](args[key_id + 1],
                                  args[key_id + 2],
                                  args[key_id + 3])
            except:
                print('there are not enough arguments for this key: {0}'
                      .format(key))
                break
            key_id += 3
        elif key == 'h' or key == '--h':
            print_help(comparers)
        else:
            print('There are no such key: {0}'.format(key))
            break
        key_id += 1
    return


def change_heat_range(heat_range):
    heat_range = utils.parse_int(heat_range)
    if heat_range is None or heat_range < 2:
        return
    game_field.heat_range = heat_range
    return


def change_life_density(life_density):
    life_density = utils.parse_int(life_density)
    if life_density is None or life_density < 0 or life_density > 100:
        return
    game_field.life_density = life_density
    return


def change_type(game_type):
    game_type = game_type.lower()
    if (game_type != game_field.game_type and (game_type == "obsessed" or
                                               game_type == "boundary" or
                                               game_type == "endless")):
        game_field.game_type = game_type
    else:
        print('There are no such type: {0}'.format(game_type))
        return
    return


def change_size(x, y):
    """Change size of game field"""
    x_size = utils.parse_int(x)
    y_size = utils.parse_int(y)
    if x_size is None or y_size is None or x_size < 3 or y_size < 3:
        print('The size of field should be more then 3x3')
        return
    game_field.x_size = x_size
    game_field.y_size = y_size
    return


def print_help(comparers):
    for comparer in comparers:
        for key in comparer:
            print('{0} {1}'.format(key, help_dict[key]))
    return


def print_field():
    representation = ''
    for y in range(game_field.y_size):
        for x in range(game_field.x_size):
            if (x, y) in game_field.current_field:
                representation += ' ' + '#'
            else:
                representation += ' ' + '.'
        print(representation)
        representation = ''
    return


def print_heat_map():
    game_field.get_heat_map_state()
    representation = ''
    if len(game_field.previous_fields) == 0:
        print('There are no previous field, make some steps')
        return
    for y in range(game_field.y_size):
        for x in range(game_field.x_size):
            representation += ' ' + str(game_field.heat_map[x][y])
        print(representation)
        representation = ''
    return


def change_cell_state(x, y, state):
    x = utils.parse_int(x)
    y = utils.parse_int(y)
    state = state.lower()
    if x >= 0 and y >= 0 and x < game_field.x_size and y < game_field.y_size:
        if state == 'dead':
            if (x, y) in game_field.current_field:
                game_field.current_field.pop((x, y))
        elif state == 'alive':
            game_field.current_field[(x, y)] = 'Alive'
        else:
            print('There are no such state: {0}'.format(state))
    else:
        print('The cell should be on field!\n\
              x size: {0}\
              y size: {1}'.format(game_field.x_size, game_field.y_size))
    return

if __name__ == "__main__":
    main()
