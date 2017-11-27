#!/usr/bin/env python3
"""Console version of <Game Of Life>"""
import sys
from sys import argv
from modules import game
from modules import utils


game_field = game.Field(25, 25, "boundary")


def main():
    args = sys.argv
    basic_commands_comparer = {'g': game_field.generate,
                           'k': game_field.kill_life,
                           'pv': game_field.previous_field,
                           'ghm': game_field.get_heat_map_state,
                           'ns': game_field.next_step,
                           'pf': print_field,
                           'h': print_help,
                           '--h': print_help}
    commands_with_one_arg_comparer = {'chr': change_heat_range,
                                    'cld': change_life_density,
                                    'ct': change_type}
    commands_with_two_args_comparer = {'cs': change_size}
    comparers = (basic_commands_comparer, commands_with_one_arg_comparer,
                 commands_with_two_args_comparer)
    while len(args) != 0:
        treat_args(args, comparers)
        args = sys.argv
    return


def treat_args(args, comparers):
    for key_id in range(len(args)):
        if args[key_id].lower() in comparers[0]:
            comparers[0][args[key_id]]()
        elif args[key_id].lower() in comparers[1]:
            try:
                comparers[1][key.lower](args[key_id + 1])
            except:
                print('there are not enough arguments for this key: {0}'\
                    .format(args[key_id].lower()))
        elif args[key_id].lower() in comparers[2]:
            try:
                arg = (args[key_id + 1], args[key_id + 2])
                comparers[2][args[key_id].lower()](arg)
            except:
                print('there are not enough arguments for this key: {0}'\
                    .format(args[key_id].lower()))
        else:
            print('There are no such keys: {0}'.format(args[key_id].lower()))
    return


def change_heat_range(arg):
    heat_range = utils.parse_int(arg)
    if heat_range is None or heat_range < 2:
        return
    game_field.heat_range = heat_range
    return


def change_life_density(arg):
    life_density = utils.parse_int(arg)
    if life_density is None or life_density < 0 or life_density > 100:
        return
    game_field.life_density = life_density
    return


def change_type(arg):
    game_type = arg
    if (game_type != game_field.game_type):
        game_field.game_type = game_type
        gui_render_field.render_next_field(game_field)
    else:
        return


def _change_size(sizes):
    """Change size of game field"""
    if len(sizes) != 2:
        return
    x_size = utils.parse_int(sizes[0])
    y_size = utils.parse_int(sizes[1])
    if x_size is None or y_size is None or x_size < 3 or y_size < 3:
        return
    game_field.x_size = x_size
    game_field.y_size = y_size
    return


def print_help():
    for key in basic_commands_comparer.keys:
        print('{0}: {1}'.format(key, str(basic_commands_comparer[key])))
    for key in commands_with_one_arg_comparer.keys:
        print('{0}: {1}'.format(key, str(commands_with_one_arg_comparer[key])))
    for key in commands_with_two_args_comparer.keys:
        print('{0}: {1}'.format(key, str(commands_with_two_args_comparer[key])))
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

if __name__ == "__main__":
    main()
