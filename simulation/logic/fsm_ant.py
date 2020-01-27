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

from simulation.board import Board
from simulation.logic.dumb_scouter import DumbScouter
from simulation.logic.gatherer import Gatherer
from simulation.logic.sensing_scouter import SensingScouter
from simulation.logic.advanced_scouter import AdvancedScouter


class FSMAnt(DumbScouter):

    """
        Knowledge used:
            - min_harvest: (float) Min value an ant has to store to stop being starved
            - max_harvest: (float) Max value an ant can carry
            - eat: (float) Value an ant eat to do a step
            - harvest: (float) Value an ant collect by stepping on food
            - use_diagonal: (bool) Allow ants to use diagonals to travel
    """

    # Multiplication factor for drop value (see blob variable) when an ant is starving
    RATIO_DROP_STARVE = 2

    def __init__(self, board, knowledge, x, y):
        """
        :type board: Board
        :type knowledge: dict
        :type x: int
        :type y: int
        """
        DumbScouter.__init__(self, board, knowledge, x, y)
        self.gatherer_logic = Gatherer(board, knowledge, x, y, self.knowledge["use_diagonal"])
        self.scouting_logic = AdvancedScouter(board, knowledge, x, y, self.knowledge["use_diagonal"])

        self.stored = self.knowledge["min_harvest"]
        self.starving = False
        self.init_drop = self.knowledge['drop']

    def move(self):
        if self.starving:
            self.gatherer_logic.move()
            self.x = self.gatherer_logic.x
            self.y = self.gatherer_logic.y
        else:
            self.scouting_logic.move()
            self.x = self.scouting_logic.x
            self.y = self.scouting_logic.y

    def init_gathering(self):
        self.gatherer_logic.reset()
        self.gatherer_logic.x = self.x
        self.gatherer_logic.y = self.y

    def init_scouting(self):
        self.scouting_logic.reset()
        self.scouting_logic.x = self.x
        self.scouting_logic.y = self.y
        self.drop = self.init_drop

    def update(self):
        # if self.harvest > 0 and self.starving:
        #     self.drop = FSMAnt.RATIO_DROP_STARVE * self.init_drop

        self.drop = self.init_drop * self.stored
        DumbScouter.update(self)

        if not self.starving:
            self.stored -= self.knowledge["eat"]
            self.stored = max(0, self.stored)

        if self.board.has_food(self.x, self.y):
            if len(self.knowledge['food']) == 1:
                wanted = min(self.knowledge["min_harvest"], self.knowledge["max_harvest"] - self.stored)
            else:
                wanted = min(self.knowledge["harvest"], self.knowledge["max_harvest"] - self.stored)

            received, finished = self.board.eat_food(self.x, self.y, wanted)
            self.stored += received

            if finished:
                self.knowledge['food'].remove((self.x, self.y))

        if self.stored == 0 and not self.starving:
            self.starving = True
            self.init_gathering()

        if self.stored >= self.knowledge["min_harvest"] and self.starving:
            self.starving = False
            self.init_scouting()
