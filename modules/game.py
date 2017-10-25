#!/usr/bin/env python3
import random
from modules import utils


class Field:
    """Game's field"""
    def __init__(self, x_size, y_size, game_type):
        """Creating square field with selected params"""
        (ok, msg) = Field._check_params(x_size, y_size, game_type)
        if not ok:
            raise ValueError(msg)
        self.x_size = int(x_size)
        self.y_size = int(y_size)
        self.game_type = game_type
        """Fields save only alives cells"""
        self.current_field = {}
        self.previous_fields = []
        self.heat_map = []
        self.heat_range = 25
        """Using for generation of game field state"""
        self.life_density = 50

    @staticmethod
    def _check_params(x_size, y_size, game_type):
        """Checking correctness of params"""
        x_size = utils.parse_int(x_size)
        y_size = utils.parse_int(y_size)
        if x_size is None or x_size < 3:
            return (False, "x_size")
        if y_size is None or y_size < 3:
            return (False, "y_size")
        if (game_type != "obsessed" and game_type != "boundary" and
            game_type != "endless"):
            return (False, "game type")
        return (True, None)

    def generate(self):
        """Generate game field"""
        self.kill_life()
        for x in range(self.x_size):
            for y in range(self.y_size):
                cell_state = random.randrange(0, 101)
                if cell_state <= self.life_density:
                    self.current_field[(x, y)] = "Alive"
    
    def kill_life(self):
        """Clean all states of fields"""
        self.current_field = {}
        self.previous_fields = []

    def previous_field(self):
        """Get previous field state"""
        if len(self.previous_fields) == 0:
            return
        self.current_field = self.previous_fields.pop()

    def get_heat_map_state(self):
        """Get heat map state with selected heat range"""
        if len(self.previous_fields) == 0:
            return
        self._build_heat_map()
        for field_id in range(
                max(0, len(self.previous_fields) - self.heat_range),
                len(self.previous_fields)):
            previous_field = self.previous_fields[field_id]
            for x in range(self.x_size):
                for y in range(self.y_size):
                    if (x, y) in previous_field:
                        self.heat_map[x][y] = min(
                            self.heat_range, self.heat_map[x][y]+1)
    
    def _shift_cells_diag(self, field, d):
        shifted_field = {}
        for x in range(self.x_size):
            for y in range(self.y_size):
                if (x, y) in field:
                    shifted_field[(x+d, y+d)] = field.pop((x, y))
        return shifted_field.copy()
    
    def next_step(self):
        """Get next state of game field"""
        next_field = {}
        if self.game_type == "endless":
            self.current_field = self._shift_cells_diag(self.current_field, 1)
            self.x_size += 2
            self.y_size += 2
        for cell_coor in self.current_field:
            if self.alive_con(cell_coor, self.get_alive_neig_num(cell_coor)):
                next_field[(cell_coor[0], cell_coor[1])] = "Alive"
            neighbors = self.get_neighbors(cell_coor)
            for neigh in neighbors:
                if self.alive_con(neigh, self.get_alive_neig_num(neigh)):
                    next_field[(neigh[0], neigh[1])] = "Alive"
        while (self.game_type == "endless" and not 
               self._is_cell_on_borderline(next_field)):
            self.current_field = self._shift_cells_diag(self.current_field, -1)
            next_field = self._shift_cells_diag(next_field, -1)
            self.x_size -= 2
            self.y_size -= 2
        self.previous_fields.append(self.current_field.copy())
        self.current_field = next_field.copy()

    def get_alive_neig_num(self, cell_coor):
        """Count alive neighbors of cell"""
        alive_num = 0
        for neig_cell_coor in self.get_neighbors(cell_coor):
            if (neig_cell_coor[0], neig_cell_coor[1]) in self.current_field:
                alive_num += 1
        return alive_num
    
    def get_neighbors(self, cell_coor):
        """Get all neighbors of cell"""
        x, y = cell_coor
        neighbors = []
        if self.game_type != "obsessed":
            neighbors = [(x+i, y+j)
                        for i in range(-1, 2)
                        for j in range(-1, 2)
                        if not i == j == 0 and self.is_on_board((x+i, y+j))]
        else:
            neighbors = [((x+i) % self.x_size, (y+j) % self.y_size)
                        for i in range(-1, 2)
                        for j in range(-1, 2)
                        if not i == j == 0]
        return neighbors

    def alive_con(self, cell_coor, alive_neig_num):
        """Alive cell condition"""
        return ((cell_coor[0], cell_coor[1]) in self.current_field and
                alive_neig_num > 1 and alive_neig_num < 4 or
                alive_neig_num == 3)

    def is_on_board(self, cell_coor):
        """Cell on board condition"""
        x, y = cell_coor
        return (x >= 0 and x < self.x_size and
                y >= 0 and y < self.y_size)

    def _build_heat_map(self):
        """Initilize heat map"""
        for x in range(self.x_size):
            self.heat_map.append([])
            for y in range(self.y_size):
                self.heat_map[x].append([])
                self.heat_map[x][y] = 0

    def _is_cell_on_borderline(self, field):
        for x in range(self.x_size):
            for y in range(self.y_size):
                if ((x == 0 or x == self.x_size - 1 or
                    y == 0 or y == self.y_size - 1) and
                    (x, y) in field):
                    return True
        return False
