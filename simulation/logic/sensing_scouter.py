import random

from simulation.board import Board
from simulation.logic.dumb_scouter import DumbScouter
from simulation.logic.actions import Actions


class SensingScouter(DumbScouter):

    def move(self):
        available_dirs = []
        min_pheromone = Board.MAX_BLOB + 1

        dirs = Actions.ACTIONS_SIMPLE
        for new_dir in dirs:
            if 0 <= self.x + new_dir[0] < self.board.width and 0 <= self.y + new_dir[1] < self.board.height:
                new_pheromone = self.board.get_blob(self.x + new_dir[0], self.y + new_dir[1])
                if new_pheromone is not None:
                    if new_pheromone < min_pheromone:
                        available_dirs = [new_dir]
                        min_pheromone = new_pheromone
                    elif new_pheromone == min_pheromone:
                        available_dirs.append(new_dir)

        if len(available_dirs) != 0:
            direction = available_dirs[random.randrange(len(available_dirs))]
            self.x += direction[0]
            self.y += direction[1]
