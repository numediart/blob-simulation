# Copyright (C) 2019 - UMons
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import numpy as np


class Board:

    MAX_BLOB = 255.0
    MIN_BLOB = 0.0
    INIT_FOOD = 100

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.dropped_blob = np.zeros(shape=(width, height), dtype=float)
        self.foods = np.zeros(shape=(width, height), dtype=float)
        self.touched = np.zeros(shape=(width, height), dtype=bool)

    def save(self):
        stream = str(self.width) + ' ' + str(self.height) + '\n'
        for y in range(self.height):
            for x in range(self.width):
                saved_node = "{:d},{},{} ".format(self.touched[x, y], self.foods[x, y], self.dropped_blob[x, y])
                stream += saved_node
            stream = stream.rstrip(' ')
            stream += '\n'

        return stream.rstrip('\n')

    def load(self, filename):
        with open(filename, 'r') as file:
            dim = file.readline()
            dims = dim.split(' ')
            if dims[0] != self.width and dims[1] != self.height:
                self.__init__(int(dims[0]), int(dims[1]))

            y = 0
            for line in file:
                nodes = line.split(' ')
                if len(nodes) != self.width:
                    print("Error with given height !" + str(len(nodes)))

                x = 0
                for node in nodes:
                    values = node.split(',')

                    if len(values) != 3:
                        print("Error with packaged values !")

                    self.touched[x, y] = values[0] == '1'
                    self.foods[x, y] = float(values[1])
                    self.dropped_blob[x, y] = float(values[2])
                    x += 1

                y += 1

    def has_food(self, x, y):
        return self.inside(x, y) and self.foods[x, y] > 0

    def set_food(self, x, y, value=INIT_FOOD):
        if not self.foods[x, y] > 0:
            self.foods[x, y] = value

    def remove_food(self, x, y):
        if self.foods[x, y] > 0:
            self.foods[x, y] = 0

    def update_blob(self, x, y, change_value):
        if self.inside(x, y):
            self.touched[x, y] = True
            self.dropped_blob[x, y] = max(Board.MIN_BLOB, min(self.dropped_blob[x, y] + change_value, Board.MAX_BLOB))
            return True
        else:
            return False

    def eat_food(self, x, y, change_value):
        if self.foods[x, y] > 0:
            if self.foods[x, y] - change_value >= 0:
                self.foods[x, y] -= change_value
            else:
                change_value = self.foods[x, y]
                self.foods[x, y] = 0
        else:
            change_value = 0

        return change_value, self.foods[x, y] <= 0

    def get_blob(self, x, y):
        if self.inside(x, y):
            return self.dropped_blob[x, y]
        else:
            return None

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_touched(self, x, y):
        if self.inside(x, y):
            return self.touched[x, y]
        else:
            return False

    def get_cover(self, half_board=0):
        if half_board == 1:
            val = np.sum(self.touched[:, 0:int(self.height/2)]) * 2
        elif half_board == 2:
            val = np.sum(self.touched[:, int(self.height/2):self.height]) * 2
        else:
            val = np.sum(self.touched)

        return val / self.height / self.width * 100

    def get_blob_total(self):
        total = 0
        for x in range(self.width):
            for y in range(self.height):
                total += self.dropped_blob[x, y]

        return total / self.height / self.width / self.MAX_BLOB * 100

    def manage_blob(self, value, min_food_value=MIN_BLOB):
        for x in range(self.width):
            for y in range(self.height):
                if self.touched[x, y]:
                    if not (self.foods[x, y] > 0 and self.dropped_blob[x, y] <= min_food_value):
                        self.update_blob(x, y, -value)

    def reset(self, x, y):
        if self.inside(x, y):
            self.touched[x, y] = False
            self.dropped_blob[x, y] = 0
            self.foods[x, y] = 0

    def compare(self, board):
        if board.height != self.height and board.width != self.width:
            print("Size don't match !")
            return None

        board_comp = Board(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                board_comp.foods[x, y] = board.foods[x, y] - self.foods[x, y]
                board_comp.touched[x, y] = self.touched[x, y] == board.touched[x, y]
                board_comp.dropped_blob[x, y] = board.dropped_blob[x, y] - self.dropped_blob[x, y]

        return board_comp
