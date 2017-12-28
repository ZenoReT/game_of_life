#!/usr/bin/env python3
from modules import game
from modules import utils
from tkinter import *


root = Tk()
frame = Frame(root)
frame.grid()


class Menu:
    def __init__(self, game_field, gui_render_field):
        self.generate_but = Button(frame)
        self.start_but = Button(frame)
        self.stop_but = Button(frame)
        self.kill_life_but = Button(frame)
        self.previous_state_but = Button(frame)
        self.next_state_but = Button(frame)
        self.change_size_but = Button(frame)
        self.change_game_type_but = Button(frame)
        self.heat_map_but = Button(frame)
        self.change_heat_range_but = Button(frame)
        self.change_life_density_but = Button(frame)

        self.generate_but.config(text="Generate")
        self.start_but.config(text="Start")
        self.stop_but.config(text="Stop")
        self.kill_life_but.config(text="Kill life")
        self.previous_state_but.config(text="Previous state")
        self.next_state_but.config(text="Next state")
        self.change_size_but.config(text="Change size (x, y)")
        self.change_game_type_but.config(text="Change type")
        self.heat_map_but.config(text="Show heat map")
        self.change_heat_range_but.config(text="Change heat range")
        self.change_life_density_but.config(text="change life density %")

        self.generate_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._generate(game_field, gui_render_field))
        self.start_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._start(game_field, gui_render_field))
        self.stop_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._stop(game_field, gui_render_field))
        self.kill_life_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._kill_life(game_field, gui_render_field))
        self.previous_state_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._previous(game_field, gui_render_field))
        self.next_state_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._next(game_field, gui_render_field))
        self.change_size_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._change_size(game_field, gui_render_field))
        self.change_game_type_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._change_type(game_field, gui_render_field))
        self.heat_map_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._change_heat_mode(game_field, gui_render_field))
        self.change_heat_range_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._change_heat_range(game_field))
        self.change_life_density_but.bind(
            "<ButtonRelease-1>",
            lambda event: self._change_life_density(game_field))

        self.size_entry = Entry(frame)
        self.heat_range_entry = Entry(frame)
        self.life_density_entry = Entry(frame)
        self.type_listbox = Listbox(frame, height=3, width=15)
        self.info_label = Label(
            root,
            text="size: {0} {1} game type: {2} heat range: {3}\
                                life density %: {4}".format(
               game_field.x_size, game_field.y_size, game_field.game_type,
               game_field.heat_range, game_field.life_density))

        game_types_list = ["boundary", "obsessed", "endless"]
        for game_type in game_types_list:
            self.type_listbox.insert(END, game_type)

        self.generate_but.grid(row=0, column=0)
        self.start_but.grid(row=0, column=1)
        self.stop_but.grid(row=0, column=2)
        self.kill_life_but.grid(row=0, column=3)
        self.previous_state_but.grid(row=0, column=4)
        self.next_state_but.grid(row=0, column=5)
        self.size_entry.grid(row=1, column=0)
        self.change_size_but.grid(row=1, column=1)
        self.type_listbox.grid(row=1, column=2)
        self.change_game_type_but.grid(row=1, column=3)
        self.heat_map_but.grid(row=1, column=4)
        self.heat_range_entry.grid(row=2, column=0)
        self.change_heat_range_but.grid(row=2, column=1)
        self.life_density_entry.grid(row=2, column=3)
        self.change_life_density_but.grid(row=2, column=4)
        self.info_label.grid(row=3, column=0)

        self._performed = False
        self._heat_mode = False

        root.mainloop()

    def _generate(self, game_field, gui_render_field):
        game_field.generate()
        gui_render_field.render_next_field(game_field)

    def _start(self, game_field, gui_render_field):
        self._performed = True
        sleep_time = 100
        previous_fields_len = 0
        while self._performed:
            if previous_fields_len > len(game_field.previous_fields):
                break
            if self._heat_mode:
                root.after(sleep_time, game_field.next_step(),
                           gui_render_field.render_heat_map(game_field))
            else:
                root.after(sleep_time, game_field.next_step(),
                           gui_render_field.render_next_field(game_field))
            root.update()
            previous_fields_len += 1

    def _stop(self, game_field, gui_render_field):
        self._performed = False

    def _kill_life(self, game_field, gui_render_field):
        game_field.kill_life()
        gui_render_field.render_next_field(game_field)

    def _previous(self, game_field, gui_render_field):
        game_field.previous_field()
        if self._heat_mode:
            gui_render_field.render_heat_map(game_field)
        else:
            gui_render_field.render_next_field(game_field)

    def _next(self, game_field, gui_render_field):
        game_field.next_step()
        if self._heat_mode:
            gui_render_field.render_heat_map(game_field)
        else:
            gui_render_field.render_next_field(game_field)

    def _change_size(self, game_field, gui_render_field):
        """Change size of game field"""
        sizes = self.size_entry.get().split()
        if len(sizes) != 2:
            return
        x_size = utils.parse_int(sizes[0])
        y_size = utils.parse_int(sizes[1])
        if x_size is None or y_size is None or x_size < 3 or y_size < 3:
            return
        game_field.x_size = x_size
        game_field.y_size = y_size
        gui_render_field.render_next_field(game_field)
        self.info_label.config(text="size: {0} {1} game type: {2} heat range: {3}\
                                life density %: {4}".format(
               game_field.x_size, game_field.y_size, game_field.game_type,
               game_field.heat_range, game_field.life_density))

    def _change_heat_range(self, game_field):
        """Change heat range of heat map"""
        heat_range = utils.parse_int(self.heat_range_entry.get())
        if heat_range is None or heat_range < 2:
            return
        game_field.heat_range = heat_range
        self.info_label.config(text="size: {0} {1} game type: {2} heat range: {3}\
                                life density %: {4}".format(
               game_field.x_size, game_field.y_size, game_field.game_type,
               game_field.heat_range, game_field.life_density))

    def _change_life_density(self, game_field):
        """Change heat range of heat map"""
        life_density = utils.parse_int(self.life_density_entry.get())
        if life_density is None or life_density < 0 or life_density > 100:
            return
        game_field.life_density = life_density
        self.info_label.config(text="size: {0} {1} game type: {2} heat range: {3}\
                                life density %: {4}".format(
               game_field.x_size, game_field.y_size, game_field.game_type,
               game_field.heat_range, game_field.life_density))

    def _change_type(self, game_field, gui_render_field):
        """Change game type"""
        game_type = self.type_listbox.get(ACTIVE)
        if game_type != game_field.game_type:
            game_field.game_type = game_type
            if game_type == "endless":
                self._heat_mode = False
        else:
            return
        self.info_label.config(text="size: {0} {1} game type: {2} heat range: {3}\
                                life density %: {4}".format(
               game_field.x_size, game_field.y_size, game_field.game_type,
               game_field.heat_range, game_field.life_density))

    def _change_heat_mode(self, game_field, gui_render_field):
        if self._heat_mode:
            self._heat_mode = False
            gui.render_field.render_field(game_field)
        elif game_field.game_type != "endless":
            self._heat_mode = True
            gui_render_field.render_heat_map(game_field)


class Field_render:
    def __init__(self, game_field):
        self.window_width = 900
        self.window_height = 600
        self.canv = Canvas(
            root,
            width=self.window_width,
            height=self.window_height,
            bg="grey")
        self.cell_width = self.window_width / game_field.x_size
        self.cell_height = self.window_height / game_field.y_size

    def change_cell(self, game_field, x, y, ip):
        """If user click on cell change it"""
        state = "Dead"
        if (x, y) in game_field.current_field:
            state = "Alive"
        if state == "Alive":
            game_field.current_field.pop((x, y))
            self.canv.itemconfigure(ip, fill="white")
        else:
            game_field.current_field[(x, y)] = "Alive"
            self.canv.itemconfigure(ip, fill="green")

    def update_cells_size(self, game_field):
        self.cell_width = self.window_width / game_field.x_size
        self.cell_height = self.window_height / game_field.y_size

    def render_next_field(self, game_field):
        """Next graphic representation of game field"""
        self.update_cells_size(game_field)
        self.canv.delete("all")
        for x in range(game_field.x_size):
            for y in range(game_field.y_size):
                state = "Dead"
                if (x, y) in game_field.current_field:
                    state = "Alive"
                color = "white"
                if state == "Alive":
                    color = "green"
                ip = self.canv.create_rectangle(
                    x * self.cell_width,
                    y * self.cell_height,
                    x * self.cell_width + self.cell_width,
                    y * self.cell_height + self.cell_height,
                    fill=color,
                    outline="black")
                self.canv.tag_bind(
                    ip,
                    "<ButtonRelease-1>",
                    lambda event, x=x, y=y, ip=ip:
                    self.change_cell(game_field, x, y, ip))
        self.canv.grid(row=1, column=0)

    def render_heat_map(self, game_field):
        """Next graphic representation of heat map"""
        if (game_field.game_type == "endless" or
                len(game_field.previous_fields) == 0):
            return
        game_field.get_heat_map_state()
        self.canv.delete("all")
        for x in range(game_field.x_size):
            for y in range(game_field.y_size):
                state = game_field.heat_map[x][y]
                color = self._get_color(state)
                ip = self.canv.create_rectangle(
                    x * self.cell_width,
                    y * self.cell_height,
                    x * self.cell_width + self.cell_width,
                    y * self.cell_height + self.cell_height,
                    fill=color,
                    outline="black")

    def _get_color(self, state):
        """Get color of cell for heat map"""
        red_hue = hex(int(255 / (state + 1)))[2:]
        green_hue = hex(255 - int(str(red_hue), 16))[2:]
        if len(green_hue) < 2:
            green_hue = "0" + green_hue
        if len(red_hue) < 2:
            red_hue = "0" + red_hue
        color = "#{0}{1}{2}".format(red_hue, green_hue, "00")
        return color
