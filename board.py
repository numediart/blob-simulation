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

    MAX_BLOB = 255
    DECREASE_BLOB = 0.1

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.board_array = np.empty(shape=(width, height), dtype=object)
        for x in range(self.width):
            for y in range(self.height):
                self.board_array[x, y] = Square()

    def save(self):
        stream = ''
        for y in range(self.height):
            for x in range(self.width):
                saved_node = self.board_array[x, y].save() + " "
                stream += str(saved_node)
            stream = stream.rstrip(' ')
            stream += '\n'

        return stream.rstrip('\n')

    def load(self, file):
        y = 0
        for line in file:
            nodes = line.split(' ')
            if len(nodes) != self.width:
                print("Error with initialized height !" + str(len(nodes)))

            x = 0
            for node in nodes:
                self.board_array[x, y].load(node)
                x += 1

            y += 1

    def has_food(self, x, y):
        return self.inside(x, y) and self.board_array[x, y].food

    def update_blob(self, x, y, change_value):
        if self.inside(x, y):
            self.board_array[x, y].update_blob(change_value)
            return True
        else:
            return False

    def get_blob(self, x, y):
        if self.inside(x, y):
            return self.board_array[x, y].blob
        else:
            return None

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_touched(self, x, y):
        if self.inside(x, y):
            return self.board_array[x, y].touched
        else:
            return False

    def next_turn(self, food_lock=True):
        for x in range(self.width):
            for y in range(self.height):
                if self.board_array[x, y].touched:
                    if not (food_lock and self.board_array[x,y].food):
                        self.board_array[x, y].update_blob(-Board.DECREASE_BLOB)

    def reset(self, x, y):
        if self.inside(x, y):
            self.board_array[x, y] = Square()


class Square:

    def __init__(self):
        self.food = False
        self.touched = False
        self.blob = 0

    def update_blob(self, change_value):
        self.touched = True
        self.blob += change_value
        self.blob = max(0, min(self.blob, Board.MAX_BLOB))

    def save(self):
        return format(self.touched, 'd') + "," + format(self.food, 'd') + "," + str(self.blob)

    def load(self, node):
        values = node.split(',')

        if len(values) != 3:
            print("Error with packaged values !")

        self.touched = values[0] == '1'
        self.food = values[1] == '1'
        self.blob = float(values[2])