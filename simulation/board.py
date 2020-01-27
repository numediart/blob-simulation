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
    """ Board keeps tracks of food or blob quantities on each square """

    MAX_BLOB = 255.0  # Blob highest possible value
    MIN_BLOB = 0.0  # Blob lowest possible value
    INIT_FOOD = 100  # Highest and initial food value

    def __init__(self, width, height):
        """
        :param width: number of squares for board width
        :param height: number of squares for board height
        """
        self.width = width
        self.height = height

        self.dropped_blob = np.zeros(shape=(width, height), dtype=float)
        self.foods = np.zeros(shape=(width, height), dtype=float)
        self.touched = np.zeros(shape=(width, height), dtype=bool)

    def save(self):
        """
        :return: a string value containing all information to save board current state
        """
        stream = str(self.width) + ' ' + str(self.height) + '\n'
        for y in range(self.height):
            for x in range(self.width):
                saved_node = "{:d},{},{} ".format(self.touched[x, y], self.foods[x, y], self.dropped_blob[x, y])
                stream += saved_node
            stream = stream.rstrip(' ')
            stream += '\n'

        return stream.rstrip('\n')

    def load(self, filename):
        """
        Restore from file the board state
        :param filename: the name of a file which contains the board saved data
        """
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
        """
        :param x: horizontal square position
        :param y: vertical square position
        :return: True if square (x,y) exists and has food
        """
        return self.inside(x, y) and self.foods[x, y] > 0

    def set_food(self, x, y, value=INIT_FOOD):
        """
        Set food on (x, y) square with 'value' as quantity of food
        :param x: horizontal square position
        :param y: vertical square position
        :param value: the quantity of food to set
        """
        if not self.foods[x, y] > 0:
            self.foods[x, y] = value

    def remove_food(self, x, y):
        """
        Set food on (x, y) square to zero
        :param x: horizontal square position
        :param y: vertical square position
        """
        if self.foods[x, y] > 0:
            self.foods[x, y] = 0

    def update_blob(self, x, y, change_value):
        """
        Modify the quantity of blob on (x, y) square and marks the square as being touched by the blob
        :param x: horizontal square position
        :param y: vertical square position
        :param change_value: the blob value to add on this square
        """
        if self.inside(x, y):
            self.touched[x, y] = True
            self.dropped_blob[x, y] = max(Board.MIN_BLOB, min(self.dropped_blob[x, y] + change_value, Board.MAX_BLOB))

    def eat_food(self, x, y, change_value):
        """
        Remove 'change_value' quantity from food quantity on (x,y) square
        :param x: horizontal square position
        :param y: vertical square position
        :param change_value: the food value to remove from this square
        :return: a tuple with actual change_value (if food was lower than given change_value)
            and a boolean if food has been finished
        """
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
        """
        :param x: horizontal square position
        :param y: vertical square position
        :return: the blob quantity on (x,y) square or None if square doesn't exist
        """
        if self.inside(x, y):
            return self.dropped_blob[x, y]
        else:
            return None

    def inside(self, x, y):
        """
        :param x: horizontal square position
        :param y: vertical square position
        :return: True if square exists
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def is_touched(self, x, y):
        """
        :param x: horizontal square position
        :param y: vertical square position
        :return: True if square exists and has been touched by blob
        """
        if self.inside(x, y):
            return self.touched[x, y]
        else:
            return False

    def get_cover(self, half_board=0):
        """
        :param half_board: 1 to return cover from up half-board,
            2 to return cover from bottom half-board
            or 0 to return cover from all the board
        :return: the covering percentage (number of touched square) on the complete board or given half-board
        """
        if half_board == 1:
            val = np.sum(self.touched[:, 0:int(self.height/2)]) * 2
        elif half_board == 2:
            val = np.sum(self.touched[:, int(self.height/2):self.height]) * 2
        else:
            val = np.sum(self.touched)

        return val / self.height / self.width * 100

    def get_blob_total(self):
        """
        :return: the total quantity of blob on the board
        """
        total = 0
        for x in range(self.width):
            for y in range(self.height):
                total += self.dropped_blob[x, y]

        return total / self.height / self.width / self.MAX_BLOB * 100

    def manage_blob(self, value, min_food_value=MIN_BLOB):
        """
        On all squares decrease blob by 'value'
        except if it's a food square then minimal value is set to 'min_food_value'
        :param value: use to decrease all blob squares
        :param min_food_value: minimal remaining blob value when it's a food square as well
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.touched[x, y]:
                    if not (self.foods[x, y] > 0 and self.dropped_blob[x, y] <= min_food_value):
                        self.update_blob(x, y, -value)

    def reset(self, x, y):
        """
        Reset square, meaning non-touched, no blob and no food
        :param x: horizontal square position
        :param y: vertical square position
        """
        if self.inside(x, y):
            self.touched[x, y] = False
            self.dropped_blob[x, y] = 0
            self.foods[x, y] = 0

    def compare(self, board):
        """
        :param board: another board instance to compare to
        :return: A new board instance set with comparison on each square:
            food is set with this food square minus the board parameter food square
            touched is true if both squares are touched or untouched
            dropped_blob is set with this blob square minus the board parameter blob square
        Return None if sizes don't match
        """
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
