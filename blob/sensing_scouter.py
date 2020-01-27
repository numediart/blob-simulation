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

from board import Board
from blob.dumb_scouter import DumbScouter
from blob.actions import Actions


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
