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

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from simulation.board import Board
from simulation.logic.dumb_scouter import DumbScouter


class SensingScouter(DumbScouter):

    def __init__(self, board, knowledge, x, y, use_diagonal=False, sightline=-1, light_compute=True):
        DumbScouter.__init__(self, board, knowledge, x, y)

        self.use_diagonal = use_diagonal
        self.sight_see = sightline if sightline > 0 else 1
        self.light_compute = light_compute
        self.goal = None
        self.path = []

    def get_matrix(self, x0, y0, x1, y1):
        width = x1 - x0
        height = y1 - y0
        matrix = np.zeros((width, height))
        for y in range(height):
            for x in range(width):
                if self.board.get_blob(x0 + x, y0 + y) > 0:
                    matrix[x, y] = (1 + Board.MAX_BLOB - self.board.get_blob(x0 + x, y0 + y)) * 1.5
                elif self.board.is_touched(x0 + x, y0 + y):
                    matrix[x, y] = Board.MAX_BLOB * 2
                else:
                    matrix[x, y] = 1
        return np.transpose(matrix)

    def choose_goal(self):
        x0, y0 = max(0, self.x - self.sight_see), max(0, self.y - self.sight_see)
        x1, y1 = min(self.board.width, self.x + self.sight_see + 1), min(self.board.height, self.y + self.sight_see + 1)

        mask = np.zeros((x1 - x0, y1 - y0), dtype=bool)
        mask[self.x - x0, self.y - y0] = True
        see = np.ma.masked_where(mask, self.board.dropped_blob[x0:x1, y0:y1])
        min_indices = np.ma.where(see == np.min(see))

        if len(min_indices[0]) == 0:
            return None
        else:
            i = np.random.randint(len(min_indices[0]))
            return min_indices[0][i] + x0, min_indices[1][i] + y0

    def best_way_to(self):
        if self.sight_see > 0:
            x0, y0 = max(0, self.x - self.sight_see), max(0, self.y - self.sight_see)
            x1, y1 = min(self.board.width, self.x + self.sight_see + 1), min(self.board.height,
                                                                             self.y + self.sight_see + 1)
        else:
            x0, y0 = 0, 0
            x1, y1 = self.board.width, self.board.height

        grid = Grid(matrix=self.get_matrix(x0, y0, x1, y1))

        start = grid.node(self.x - x0, self.y - y0)
        end = grid.node(self.goal[0] - x0, self.goal[1] - y0)

        if self.use_diagonal:
            finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        else:
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

        self.path, runs = finder.find_path(start, end, grid)
        self.path = self.path[1:]
        for i, step in enumerate(self.path):
            self.path[i] = (step[0] + x0, step[1] + y0)

    def reached(self, goal):
        return goal is not None and self.x == goal[0] and self.y == goal[1]

    def move(self):
        # Scouter has no more goal
        if self.goal is None:  # or self.board.get_blob(self.goal[0], self.goal[1]) != 0:
            self.goal = self.choose_goal()
            if self.goal[0] == self.x and self.goal[1] == self.y:
                print("Shouldn't happen")
            self.path = []

            # No goal
            if self.goal is None:
                return

        # Scouter has no more path to goal
        if len(self.path) == 0 or not self.light_compute:
            self.best_way_to()

            # No path found, search another goal next time
            if len(self.path) == 0:
                self.goal = None
                return

        new_pos = self.path[0]
        self.path = self.path[1:]

        self.x = new_pos[0]
        self.y = new_pos[1]

        # Scouter reached goal
        if self.reached(self.goal):
            self.goal = None
            self.path = []

    def reset(self):
        self.goal = None
        self.path = []
        self.x = 0
        self.y = 0
