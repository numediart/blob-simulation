import random

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from simulation.board import Board
from simulation.logic.dumb_scouter import DumbScouter


class Gatherer(DumbScouter):
    def __init__(self, board, knowledge, x, y, drop_value, use_diagonal=True, light_compute=True):
        DumbScouter.__init__(self, board, knowledge, x, y, drop_value)

        self.use_diagonal = use_diagonal
        self.light_compute = light_compute

        self.goal = None
        self.path = []

    def get_matrix(self):
            matrix = []
            for y in range(self.board.height):
                matrix.append([])
                for x in range(self.board.width):
                    matrix[y].append(
                        0 if self.board.board_array[x, y].blob <= 0
                        else Board.MAX_BLOB - self.board.board_array[x, y].blob + 1)
            return matrix

    def best_way_to(self):

        grid = Grid(matrix=self.get_matrix())

        start = grid.node(self.x, self.y)
        end = grid.node(self.goal[0], self.goal[1])

        if self.use_diagonal:
            finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        else:
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

        self.path, runs = finder.find_path(start, end, grid)
        self.path = self.path[1:]

    def reached(self, goal):
        return goal is not None and self.x == goal[0] and self.y == goal[1]

    def choose_goal(self):
        goals = []
        for food in self.knowledge['food']:
            if not self.reached(food):
                goals.append(food)

        if len(goals) == 0:
            return None
        else:
            return goals[random.randrange(len(goals))]

    def reset(self):
        self.goal = None
        self.path = []
        self.x = 0
        self.y = 0

    def move(self):
        if self.goal is None or self.goal not in self.knowledge['food']:
            self.goal = self.choose_goal()
            self.path = []

            # No goal
            if self.goal is None:
                return

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

        if self.reached(self.goal):
            self.goal = None
            self.path = []

        if self.reached(self.goal) or (self.goal not in self.knowledge['food']):
            val = self.choose_goal()
            if val is None:
                return
            else:
                self.goal = val
