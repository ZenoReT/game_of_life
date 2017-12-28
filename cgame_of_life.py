#!/usr/bin/env python3
"""Console version of <Game Of Life>"""
import sys
import argparse
from sys import argv
from modules import game
from modules import utils


def main():
    game_field = game.Field(25, 25, 'boundary')
    parser = create_parser()
    args = input('Input new args: ').split()
    while len(args) != 0:
        parsed_args = parser.parse_args(args)
        treat_args(parsed_args, game_field)
        print_states(game_field)
        args = input('Input new args: ').split()


def print_states(game_field):
    print('------------------------\n\
            \rcurrent size: {0} {1}\n\
            \rcurrent_type: {2}\n\
            \rcurrent heat range: {3}\n\
            \rcurrent life density: {4}\n\
            \rcurrent count of previous fields: {5}\n\
            \r------------------------'
          .format(game_field.x_size,
                  game_field.y_size,
                  game_field.game_type,
                  game_field.heat_range,
                  game_field.life_density,
                  len(game_field.previous_fields)))


def create_parser():
    parser = argparse.ArgumentParser(
        description='Console version of games_of_life:\n\
                    \rThe list of keys:\n\
                    \r-g\n\
                    \r-k\n\
                    \r-ps\n\
                    \r-phm\n\
                    \r-ns\n\
                    \r-pf\n\
                    \r-chr\n\
                    \r-cld\n\
                    \r-ct\n\
                    \r-cs\n\
                    \r-ccs')
    parser.add_argument('-g', '--generate',
                        help='generate game field',
                        action='store_true')
    parser.add_argument('-kl', '--kill_life',
                        help='clear field and make all cells are dead',
                        action='store_true')
    parser.add_argument('-ps', '--previous_state',
                        help='get previous state of field',
                        action='store_true')
    parser.add_argument('-phm', '--print_heat_map',
                        help='print heat map on console',
                        action='store_true')
    parser.add_argument('-ns', '--next_state',
                        help='get next state of field',
                        action='store_true')
    parser.add_argument('-pf', '--print_field',
                        help='print field on console',
                        action='store_true')
    parser.add_argument('-chr', '--change_heat_range',
                        type=int,
                        help='change heat range (value > 0)')
    parser.add_argument('-cld', '--change_life_density',
                        type=int,
                        help='change life density for next generation\
                              (value in range 0 - 100%%)')
    parser.add_argument('-ct', '--change_type',
                        type=str,
                        help='change type of game: obsessed boundary endless')
    parser.add_argument('-cs', '--change_size',
                        nargs=2,
                        help='change size of field: x, y > 3')
    parser.add_argument('-ccs', '--change_cell_state',
                        nargs=3,
                        help='change cell state:\
                              x, y on field,\
                              state: dead, alive')
    return parser


def treat_args(parsed_args, game_field):
    if parsed_args.generate:
        game_field.generate()
    if parsed_args.kill_life:
        game_field.kill_life()
    if parsed_args.previous_state:
        game_field.previous_field()
    if parsed_args.print_heat_map:
        print_heat_map(game_field)
    if parsed_args.next_state:
        game_field.next_step()
    if parsed_args.print_field:
        print_field(game_field)
    if parsed_args.change_heat_range:
        change_heat_range(parsed_args.change_heat_range, game_field)
    if parsed_args.change_life_density:
        change_life_density(parsed_args.change_life_density, game_field)
    if parsed_args.change_type:
        change_type(parsed_args.change_type, game_field)
    if parsed_args.change_size:
        x, y = parsed_args.change_size
        change_size(x, y, game_field)
    if parsed_args.change_cell_state:
        x, y, state = parsed_args.change_cell_state
        change_cell_state(x, y, state, game_field)


def change_heat_range(heat_range, game_field):
    heat_range = utils.parse_int(heat_range)
    if heat_range is None or heat_range < 2:
        return
    game_field.heat_range = heat_range
    return


def change_life_density(life_density, game_field):
    life_density = utils.parse_int(life_density)
    if life_density is None or life_density < 0 or life_density > 100:
        return
    game_field.life_density = life_density
    return


def change_type(game_type, game_field):
    game_type = game_type.lower()
    if (game_type != game_field.game_type and (game_type == "obsessed" or
                                               game_type == "boundary" or
                                               game_type == "endless")):
        game_field.game_type = game_type
    else:
        print('There are no such type: {0}'.format(game_type))
        return
    return


def change_size(x, y, game_field):
    """Change size of game field"""
    x_size = utils.parse_int(x)
    y_size = utils.parse_int(y)
    if x_size is None or y_size is None or x_size < 3 or y_size < 3:
        print('The size of field should be more then 3x3')
        return
    game_field.x_size = x_size
    game_field.y_size = y_size
    return


def print_field(game_field):
    representation = []
    for y in range(game_field.y_size):
        for x in range(game_field.x_size):
            element = "#" if (x, y) in game_field.current_field else "."
            representation.append(element)
        print(' '.join(representation))
        representation = []
    return


def print_heat_map(game_field):
    game_field.get_heat_map_state()
    representation = []
    if len(game_field.previous_fields) == 0:
        print('There are no previous field, make some steps')
        return
    for y in range(game_field.y_size):
        for x in range(game_field.x_size):
            representation.append(str(game_field.heat_map[x][y]))
        print(' '.join(representation))
        representation = []
    return


def change_cell_state(x, y, state, game_field):
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
