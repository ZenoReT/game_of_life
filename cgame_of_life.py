#!/usr/bin/env python3
"""Console version of <Game Of Life>"""
import sys
from sys import argv
from modules import game
from modules import utils


def main():
    game_field = game.Field(25, 25, "boundary")
    gui_field_render = gui.Field_render(game_field)
    gui_field_render.render_next_field(game_field)
    gui_menu = gui.Menu(game_field, gui_field_render)

if __name__ == "__main__":
    main()
