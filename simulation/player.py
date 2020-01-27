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

from math import ceil
from random import randrange
import json

from simulation.board import Board


class Player:

    def __init__(self, board, blob, default_config):
        """
        :type blob: Blob_Manager
        :type board: Board
        """
        self.board = board
        self.blob = blob

        with open(default_config, 'r') as file:
            d = json.load(file)

        self.clean_top = d['clean_top']
        self.food_size = d['food_size']
        self.use_circle = d['use_food_circle']

    def save(self):
        d = dict()
        d['clean_top'] = self.clean_top
        d['food_size'] = self.food_size
        d['use_food_circle'] = self.use_circle
        return json.dumps(d, indent=4, sort_keys=True)

    def set_random_food(self, qt, random_top=None):
        if random_top is None:  # Randomize over all the board
            y_offset = 0
            y_range = self.board.height
        elif random_top:  # Randomize over the half top board
            y_offset = 0
            y_range = ceil(self.board.height / 2)
        else:  # Randomize over the half bottom board
            y_offset = int(self.board.height / 2)
            y_range = ceil(self.board.height / 2)

        foods = 0
        while foods < qt:
            x = randrange(self.board.width)
            y = y_offset + randrange(y_range)
            if not self.board.has_food(x, y):
                if self.set_food(x, y):
                    foods += 1

    def remove_food(self, x, y):
        food_remove = False
        x0, y0 = int(x - self.food_size / 2), int(y - self.food_size / 2)
        for x_size in range(self.food_size):
            for y_size in range(self.food_size):
                if not self.use_circle or (x_size - self.food_size / 2) ** 2 + (y_size - self.food_size / 2) ** 2 <= \
                        (self.food_size / 2 - 0.5) ** 2:
                    if self.board.inside(x0 + x_size, y0 + y_size) and not self.board.is_touched(x0 + x_size,
                                                                                                 y0 + y_size):
                        self.board.remove_food(x0 + x_size, y0 + y_size)
                        food_remove = True

        if not food_remove:
            print("Blob already found it !")

    def set_food(self, x, y):
        food_put = False
        x0, y0 = int(x - self.food_size / 2), int(y - self.food_size / 2)
        for x_size in range(self.food_size):
            for y_size in range(self.food_size):
                if not self.use_circle or (x_size - self.food_size / 2) ** 2 + (y_size - self.food_size / 2) ** 2 <= \
                        (self.food_size / 2 - 0.5) ** 2:
                    if self.board.inside(x0 + x_size, y0 + y_size) and not self.board.is_touched(x0 + x_size,
                                                                                                 y0 + y_size):
                        self.board.set_food(x0 + x_size, y0 + y_size)
                        food_put = True

        if not food_put:
            print("There is blob there !")
            return False

        return True

    def check_blob_cover(self):
        return self.board.get_cover(1), self.board.get_cover(2)

    def clean_board(self):
        y_range = ceil(self.board.height/2)

        if self.clean_top:
            y_offset = 0
        else:
            y_offset = int(self.board.height/2)

        for x in range(self.board.width):
            for y in range(y_range):
                self.board.reset(x, y_offset + y)
                self.blob.reset(x, y_offset + y)

        self.clean_top = not self.clean_top
