#!/usr/bin/env python3
import sys
import unittest
import game


class FieldTest(unittest.TestCase):
    def test_incorrect_init(self):
        try:
            field = Field(0, 0, "boundary")
        except ValueError:
            self.assertTrue(True)
            return
        self.assertFalse(True)
        return

    def test_correct_alive_neig_num_boundary(self):
        field = Field(3, 3, "boundary")
        field.current_field = {(0, 0): "Alive",
                               (1, 1): "Alive"}

        expected = 2
        actual = field.get_alive_neig_num((0, 1))

        self.assertEqual(expected, actual)
        return

    def test_correct_alive_neig_obsessed(self):
        field = Field(3, 3, "obsessed")
        field.current_field = {(0, 0): "Alive",
                               (1, 1): "Alive",
                               (2, 1): "Alive"}

        expected = 3
        actual = field.get_alive_neig_num((0, 1))

        self.assertEqual(expected, actual)
        return

    def test_correct_alive_neigh_endless(self):
        field = Field(3, 3, "endless")
        field.current_field = {(2, 0): "Alive",
                               (2, 1): "Alive",
                               (2, 2): "Alive"}
        field.next_step()

        expected = 2
        actual = field.get_alive_neig_num((4, 1))

        self.assertEqual(expected, actual)
        return

    def test_next_state_boundary(self):
        field = Field(3, 3, "boundary")
        field.current_field = {(0, 0): "Alive",
                               (1, 0): "Alive",
                               (2, 0): "Alive"}

        expected = {(1, 0): "Alive",
                    (1, 1): "Alive"}
        field.next_step()

        self.assertEqual(expected, field.current_field)
        return

    def test_next_state_obsessed(self):
        field = Field(3, 3, "obsessed")
        field.current_field = {(0, 0): "Alive",
                               (1, 0): "Alive",
                               (2, 0): "Alive"}

        expected = {}
        for x in range(3):
            for y in range(3):
                field.current_field[(x, y)] = "Alive"
        field.next_step()

        self.assertEqual(expected, field.current_field)
        return

    def test_next_state_endless(self):
        field = Field(3, 3, "endless")
        field.current_field = {(0, 0): "Alive",
                               (1, 0): "Alive",
                               (2, 0): "Alive"}

        expected = {(2, 0): "Alive",
                    (2, 1): "Alive",
                    (2, 2): "Alive"}
        field.next_step()

        self.assertEqual(expected, field.current_field)
        return

    def test_kill_life_correct(self):
        field = Field(5, 5, "obsessed")
        field.generate()
        field.kill_life()

        self.assertEqual({}, field.current_field)
        return

    def test_heat_map_correct(self):
        field = Field(5, 5, "boundary")
        field.current_field = {(2, 1): "Alive",
                               (2, 2): "Alive",
                               (3, 1): "Alive",
                               (3, 2): "Alive"}
        for x in range(3):
            field.next_step()
        field.get_heat_map_state()

        expected = []
        for x in range(field.x_size):
            expected.append([])
            for y in range(field.y_size):
                expected[x].append([])
                if (x == 2 or x == 3) and (y == 1 or y == 2):
                    expected[x][y] = 3
                else:
                    expected[x][y] = 0

        self.assertEqual(expected, field.heat_map)
        return

    def test_get_neigh_correct(self):
        field = Field(5, 5, "boundary")

        expected = [
            (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 3),
            (3, 1), (3, 2), (3, 3)]
        actual = field.get_neighbors((2, 2))

        self.assertEqual(expected, actual)
        return

    def test_shift_cells_diag_left_correct(self):
        field = Field(5, 5, "endless")
        field.current_field = {(0, 0): "Alive",
                               (2, 2): "Alive",
                               (2, 3): "Alive",
                               (4, 4): "Alive"}
        field.x_size += 2
        field.y_size += 2
        field.current_field = field._shift_cells_diag(field.current_field, -1)

        expected = {(-1, -1): "Alive",
                    (1, 1): "Alive",
                    (1, 2): "Alive",
                    (3, 3): "Alive"}

        self.assertEqual(expected, field.current_field)
        return

    def test_shift_cells_diag_right_correct(self):
        field = Field(5, 5, "endless")
        field.current_field = {(0, 0): "Alive",
                               (2, 2): "Alive",
                               (2, 3): "Alive",
                               (4, 4): "Alive"}
        field.x_size += 2
        field.y_size += 2
        field.current_field = field._shift_cells_diag(field.current_field, 1)

        expected = {(1, 1): "Alive",
                    (3, 3): "Alive",
                    (3, 4): "Alive",
                    (5, 5): "Alive"}

        self.assertEqual(expected, field.current_field)
        return


if __name__ == '__main__':
    unittest.main()
