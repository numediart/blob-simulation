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

import random

from simulation.board import Board


class DumbScouter:
    """ Dumb scouter searching food randomly and without any knowledge except a drop ratio"""

    def __init__(self, board, knowledge, x, y):
        """
        :param board: A board class instance
        :param knowledge: a dict containing all blob knowledge and set up
        :param x: current horizontal position of the ant
        :param y: current vertical position of the ant
        """
        self.board = board
        self.knowledge = knowledge
        self.x = x
        self.y = y
        self.drop = self.knowledge["Scouters"]["Drop by eat"]

    def move(self):
        """
        Move the scouter by one square
        """
        x = self.x + random.randint(-1, 1)
        y = self.y + random.randint(-1, 1)
        if self.board.inside(x, y):
            self.x = x
            self.y = y

    def update(self):
        """
        Update board with drop ratio on the current position
        """
        self.board.update_blob(self.x, self.y, self.drop)