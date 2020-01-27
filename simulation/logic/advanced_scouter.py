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

from simulation.logic.sensing_scouter import SensingScouter


class AdvancedScouter(SensingScouter):
    """
           Knowledge used:
                - ["Scouting"]["Global Explore Probability"] : (float, between 0 and 1) Set the ratio between exploring
                    globally and exploring locally
                - ["Scouting"]["Search Locally on Food"] : when stepping on food, automatically search locally
    """

    def __init__(self, board, knowledge, x, y, use_diagonal=False, sightline=3, light_compute=True):
        SensingScouter.__init__(self, board, knowledge, x, y, use_diagonal, sightline, light_compute)
        self.state = 0

    def choose_goal(self):
        if self.state == 0:
            if not (self.board.has_food(self.x, self.y) and self.knowledge["Scouting"]["Search Locally on Food"]) \
                    and self.knowledge["Scouting"]["Global Explore Probability"] < random.random():
                self.state = 1
            return self.choose_local_goal()
        else:
            if self.knowledge["Scouting"]["Global Explore Probability"] >= random.random():
                self.state = 0
            return self.choose_global_goal()

    def choose_local_goal(self):
        return SensingScouter.choose_goal(self)

    def choose_global_goal(self):
        x0, y0 = max(0, self.x - self.sight_see), max(0, self.y - self.sight_see)
        x1, y1 = min(self.board.width, self.x + self.sight_see + 1), min(self.board.height, self.y + self.sight_see + 1)

        scores = np.zeros((x1 - x0, y1 - y0), dtype=float)
        for x in range(x1 - x0):
            for y in range(y1 - y0):
                local_x0, local_y0 = max(x0, x0 + x - self.sight_see), max(y0, y0 + y - self.sight_see)
                local_x1, local_y1 = min(x1, x0 + x + self.sight_see + 1),  min(y1, y0 + y + self.sight_see + 1)

                scores[x, y] = np.sum(self.board.dropped_blob[local_x0:local_x1, local_y0:local_y1])
                total_area = (y1-y0) * (x1-x0)
                scores[x, y] = scores[x, y] / total_area

        min_indices = np.where(scores == np.min(scores))

        if len(min_indices[0]) == 0:
            return None
        else:
            i = np.random.randint(len(min_indices[0]))
            return min_indices[0][i] + x0, min_indices[1][i] + y0

    def move(self):
        if self.board.has_food(self.x, self.y) and self.knowledge["Scouting"]["Search Locally on Food"] \
                and self.state == 1:
            self.goal = None
            self.state = 0  # Food found, search locally

        SensingScouter.move(self)
