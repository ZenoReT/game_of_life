#!/usr/bin/env python3
"""Graphic version of <Game Of Life>"""

from modules.gui import *
from modules.game import *
import time


def main():
    game_field = Field(25, 25, "boundary")
    gui_field_render = Field_render(game_field)
    gui_field_render.render_next_field(game_field)
    gui_menu = Menu(game_field, gui_field_render)

if __name__ == '__main__':
    main()
