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


class FSMAnt(DumbScouter):

    # Max value an ant has to store to stop being starved
    MAX_HARVESTING = 100

    # Value an ant eat to do a step
    EAT_VALUE = 1

    # Value an ant collect by stepping on food
    HARVEST_VALUE = 10

    # Multiplication factor for drop value (see blob variable) when an ant is starving
    RATIO_DROP_STARVE = 2

    USE_DIAGONAL = False

    def __init__(self, board, knowledge, x, y, drop_value):
        """
        :type board: Board
        :type knowledge: dict
        :type x: int
        :type y: int
        :type drop_value: float
        """
        DumbScouter.__init__(self, board, knowledge, x, y, drop_value)
        self.gatherer_logic = Gatherer(board, knowledge, x, y, drop_value, FSMAnt.USE_DIAGONAL)
        self.scouting_logic = SensingScouter(board, knowledge, x, y, drop_value)

        self.harvest = FSMAnt.MAX_HARVESTING
        self.starving = False
        self.init_drop = drop_value

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
        self.scouting_logic.x = self.x
        self.scouting_logic.y = self.y
        self.drop_value = self.init_drop

    def update(self):
        if self.harvest > 0 and self.starving:
            self.drop_value = FSMAnt.RATIO_DROP_STARVE * self.init_drop

        DumbScouter.update(self)

        if len(self.knowledge['food']) != 0 and not self.starving:
            self.harvest -= FSMAnt.EAT_VALUE
            self.harvest = max(0, self.harvest)

        if self.board.has_food(self.x, self.y):
            if len(self.knowledge['food']) == 1:
                self.harvest = FSMAnt.MAX_HARVESTING
            else:
                self.harvest += FSMAnt.HARVEST_VALUE
                self.harvest = min(self.harvest, FSMAnt.MAX_HARVESTING)

        if self.harvest == 0 and not self.starving:
            self.starving = True
            self.init_gathering()

        if self.harvest == FSMAnt.MAX_HARVESTING and self.starving:
            self.starving = False
            self.init_scouting()
