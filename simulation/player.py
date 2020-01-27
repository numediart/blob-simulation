from math import ceil
from random import randrange

from simulation.board import Board


class Player:

    def __init__(self, board, blob):
        """
        :type blob: Blob_Manager
        :type board: Board
        """
        self.board = board
        self.blob = blob
        self.clean_top = True

    def save(self):
        return format(self.clean_top, 'd')

    def load(self, filename):
        with open(filename, 'r') as file:
            self.clean_top = file.readline() == '1'

    def set_random_food(self, qt, random_top=None):
        if random_top is None:  # Randomize over all the board
            y_offset = 0
            y_range = self.board.height
        if random_top:  # Randomize over the half top board
            y_offset = 0
            y_range = ceil(self.board.height / 2)
        elif not random_top:  # Randomize over the half bottom board
            y_offset = int(self.board.height / 2)
            y_range = ceil(self.board.height / 2)

        foods = 0
        while foods < qt:
            x = randrange(self.board.width)
            y = y_offset + randrange(y_range)
            if not self.board.has_food(x, y):
                if self.set_food(x, y):
                    foods += 1

    def set_food(self, x, y, size=1):
        food_put = False

        for x_size in range(size):
            for y_size in range(size):
                if 0 <= x + x_size < self.board.width and 0 <= y + y_size < self.board.height:
                    if not self.board.board_array[x + x_size, y + y_size].touched:
                        self.board.board_array[x + x_size, y + y_size].food = True
                        food_put = True

        if not food_put:
            print("There is blob there !")
            return False

        return True

    def check_blob_size(self):
        size = 0
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.board_array[x, y].touched:
                    size += 1
        return size/(self.board.width * self.board.height) * 100

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