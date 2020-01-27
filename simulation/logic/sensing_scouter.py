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
    """ An ant with goal is to explore unknown (or non-touched) square """

    def __init__(self, board, knowledge, x, y, use_diagonal=False, sightline=-1, light_compute=True):
        """
        :param board: A board class instance
        :param knowledge: a dict containing all blob knowledge and set up
        :param x: current horizontal position of the ant
        :param y: current vertical position of the ant
        :param use_diagonal: boolean set to true if diagonal moves are available
        :param sightline: size of the ant sightline, used to compute goal decision
        :param light_compute: boolean set to true if path is computing only once and then memorized until reaching goal
        """
        DumbScouter.__init__(self, board, knowledge, x, y)

        self.use_diagonal = use_diagonal
        self.sightline = sightline if sightline > 0 else 1
        self.light_compute = light_compute
        self.goal = None
        self.path = []

    def get_matrix(self, x0, y0, x1, y1):
        """
        Compute and return a pathfinding matrix filled with board squares values
        in the rectangle given by (x0,y0) and (x1,y1)
        :param x0: the x coordinate of the up left corner of the rectangle
        :param y0: the y coordinate of the up left corner of the rectangle
        :param x1: the x coordinate of the bottom right corner of the rectangle
        :param y1: the x coordinate of the bottom right corner of the rectangle
        """
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
        """
        :return: a new goal for ant, based on unreached known food
        """
        x0, y0 = max(0, self.x - self.sightline), max(0, self.y - self.sightline)
        x1, y1 = min(self.board.width, self.x + self.sightline + 1), min(self.board.height, self.y + self.sightline + 1)

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
        """
        Inside sightline, compute pathfinding matrix, set local goal, compute and store path
        """
        if self.sightline > 0:
            x0, y0 = max(0, self.x - self.sightline), max(0, self.y - self.sightline)
            x1, y1 = min(self.board.width, self.x + self.sightline + 1), min(self.board.height,
                                                                             self.y + self.sightline + 1)
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
        """
        :param goal: a x,y tuple coordinate of the goal
        :return: True if goal exists and has been reached
        """
        return goal is not None and self.x == goal[0] and self.y == goal[1]

    def move(self):
        """
        Move ant towards set goal or compute a new goal if needed
        """

        # Scouter has no more goal
        if self.goal is None:  # or self.board.get_blob(self.goal[0], self.goal[1]) != 0:
            self.goal = self.choose_goal()
            if self.goal[0] == self.x and self.goal[1] == self.y:
                print("Shouldn't happen")
            self.path = []

            # No new goal found
            if self.goal is None:
                return

        # Scouter has no more path to goal
        # TODO Light compute could be integrated by only checking if next move is an autorized move
        #  and otherwise recalculate
        if len(self.path) == 0 or not self.light_compute:
            self.best_way_to()

            # No path found, search another goal next time
            if len(self.path) == 0:
                self.goal = None
                return

        # Move the ant by one square
        new_pos = self.path[0]
        self.path = self.path[1:]

        self.x = new_pos[0]
        self.y = new_pos[1]

        # Scouter reached goal
        if self.reached(self.goal):
            self.goal = None
            self.path = []

    def reset(self):
        """
        Reset the ant including goal, path and position
        """
        self.goal = None
        self.path = []
        self.x = 0
        self.y = 0
