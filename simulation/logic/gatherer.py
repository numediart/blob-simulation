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
    """ An ant with the only goal is to move to different food squares"""

    # TODO Gatherer could have a more intuitive logic without knowing the exact location of foods outside sightline
    #  and by following only maximum blob quantity to hope find food.
    #  But this will likely lead to disconnection of blob from food to food...

    def __init__(self, board, knowledge, x, y, use_diagonal=True, sightline=-1, light_compute=True):
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
        self.light_compute = light_compute
        self.sightline = sightline if sightline > 0 else max(self.board.width, self.board.height)

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
                    matrix[x, y] = 1 + (Board.MAX_BLOB - self.board.get_blob(x0 + x, y0 + y))
                else:
                    if self.board.is_touched(x0 + x, y0 + y):
                        matrix[x, y] = Board.MAX_BLOB * 2
                    else:
                        matrix[x, y] = 0
        return np.transpose(matrix)

    def compute_sight_see_goal(self, x0, y0, x1, y1):
        """
        Compute and return a local goal in (x0,y0) (x1,y1) area to reach global food goal
        :param x0: the x coordinate of the up left corner of the rectangle
        :param y0: the y coordinate of the up left corner of the rectangle
        :param x1: the x coordinate of the bottom right corner of the rectangle
        :param y1: the x coordinate of the bottom right corner of the rectangle
        """

        # Check if goal is not in sightline rectangle
        if x0 <= self.goal[0] < x1 and y0 <= self.goal[1] < y1:
            return self.goal[0] - x0, self.goal[1] - y0

        # Compute linear projection from the goal inside rectangle and find minimal t parameter of this projection
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

        # First hit square by projection
        symb_goal = (int(self.goal[0] + t * delta_x), int(self.goal[1] + t * delta_y))

        # Iterate over t parameter until a touched square is found
        found = self.board.is_touched(symb_goal[0], symb_goal[1])
        while not found and t <= 1:
            inc = 1 / (self.board.width + self.board.height)
            t += inc
            symb_goal = (int(self.goal[0] + t * delta_x), int(self.goal[1] + t * delta_y))
            found = self.board.is_touched(symb_goal[0], symb_goal[1])

        return symb_goal[0] - x0, symb_goal[1] - y0

    def best_way_to(self):
        """
        Inside sightline, compute pathfinding matrix, set local goal, compute and store path
        """
        x0, y0 = max(0, self.x - self.sightline), max(0, self.y - self.sightline)
        x1, y1 = min(self.board.width, self.x + self.sightline + 1), min(self.board.height, self.y + self.sightline + 1)

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
        """
        :param goal: a x,y tuple coordinate of the goal
        :return: True if goal exists and has been reached
        """
        return goal is not None and self.x == goal[0] and self.y == goal[1]

    def choose_goal(self):
        """
        :return: a new goal for ant, based on unreached known food
        """
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
        """
        Reset the ant including goal, path and position
        """
        self.goal = None
        self.path = []
        self.x = 0
        self.y = 0

    def move(self):
        """
        Move ant towards set goal or compute a new goal if needed
        """

        # Scouter has no more goal
        if self.goal is None or self.goal not in self.knowledge['food']:
            self.goal = self.choose_goal()
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
