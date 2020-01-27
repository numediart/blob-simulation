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
import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from simulation.board import Board
from simulation.logic.dumb_scouter import DumbScouter


class Gatherer(DumbScouter):
    def __init__(self, board, knowledge, x, y, use_diagonal=True, sightline=-1, light_compute=True):
        DumbScouter.__init__(self, board, knowledge, x, y)

        self.use_diagonal = use_diagonal
        self.light_compute = light_compute
        self.sight_see = sightline if sightline > 0 else max(self.board.width, self.board.height)

        self.goal = None
        self.path = []

    def get_matrix(self, x0, y0, x1, y1):
        width = x1 - x0
        height = y1 - y0
        matrix = np.zeros((width, height))
        for y in range(height):
            for x in range(width):
                if self.board.get_blob(x0 + x, y0 + y) > 0:
                    matrix[x, y] = 1 + (Board.MAX_BLOB - self.board.get_blob(x0 + x, y0 + y))
                else:
                    if self.board.is_touched(x0 + x, y0 + y):
                        matrix[x, y] = Board.MAX_BLOB * 2
                    else:
                        matrix[x, y] = 0
        return np.transpose(matrix)

    def compute_sight_see_goal(self, x0, y0, x1, y1):
        if x0 <= self.goal[0] < x1 and y0 <= self.goal[1] < y1:
            # Goal in sight_see
            return self.goal[0] - x0, self.goal[1] - y0

        delta_x = self.x - self.goal[0]
        delta_y = self.y - self.goal[1]

        t_x = None
        if delta_x != 0:
            x_collision = x0 if delta_x > 0 else x1 - 1
            t_x = (x_collision - self.goal[0]) / delta_x

        t_y = None
        if delta_y != 0:
            y_collision = y0 if delta_y >= 0 else y1 - 1
            t_y = (y_collision - self.goal[1]) / delta_y

        if t_x is None or not (0 <= t_x <= 1):
            t = t_y
        elif t_y is None or not (0 <= t_y <= 1):
            t = t_x
        else:
            t = min(t_x, t_y)

        symb_goal = (int(self.goal[0] + t * delta_x), int(self.goal[1] + t * delta_y))

        found = self.board.is_touched(symb_goal[0], symb_goal[1])
        while not found and t <= 1:
            inc = 1 / (self.board.width + self.board.height)
            t += inc
            symb_goal = (int(self.goal[0] + t * delta_x), int(self.goal[1] + t * delta_y))
            found = self.board.is_touched(symb_goal[0], symb_goal[1])

        return symb_goal[0] - x0, symb_goal[1] - y0

    def best_way_to(self):
        x0, y0 = max(0, self.x - self.sight_see), max(0, self.y - self.sight_see)
        x1, y1 = min(self.board.width, self.x + self.sight_see + 1), min(self.board.height, self.y + self.sight_see + 1)

        grid = Grid(matrix=self.get_matrix(x0, y0, x1, y1))

        x_goal, y_goal = self.compute_sight_see_goal(x0, y0, x1, y1)

        start = grid.node(self.x - x0, self.y - y0)
        end = grid.node(x_goal, y_goal)

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

    def choose_goal(self):
        if len(self.knowledge['food']) == 0:
            return None
        elif len(self.knowledge['food']) == 1:
            if self.reached(self.knowledge['food'][0]):
                return None
            else:
                return self.knowledge['food'][0]
        else:
            i = random.randrange(len(self.knowledge['food']))
            while self.reached(self.knowledge['food'][i]):
                i = random.randrange(len(self.knowledge['food']))
            return self.knowledge['food'][i]

    def reset(self):
        self.goal = None
        self.path = []
        self.x = 0
        self.y = 0

    def move(self):
        # Scouter has no more goal
        if self.goal is None or self.goal not in self.knowledge['food']:
            self.goal = self.choose_goal()
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
