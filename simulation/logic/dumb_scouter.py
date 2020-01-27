import random

from simulation.board import Board

class DumbScouter:
    """ Dumb scouter searching food randomly and without any knowledge """

    def __init__(self, board, knowledge, x, y, drop_value):
        """
        :type board: Board
        :type knowledge: dict
        :type x: int
        :type y: int
        :type drop_value: float
        """
        self.board = board
        self.knowledge = knowledge
        self.x = x
        self.y = y
        self.drop_value = drop_value

    def move(self):
        x = self.x + random.randint(-1, 1)
        y = self.y + random.randint(-1, 1)
        if self.board.inside(x, y):
            self.x = x
            self.y = y

    def update(self):
        self.board.update_blob(self.x, self.y, self.drop_value)