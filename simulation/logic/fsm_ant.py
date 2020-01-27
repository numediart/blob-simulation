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
            - ["Harvesting"]["Min"]: (float) Min value an ant has to store to stop being starved
            - ["Harvesting"]["Max"]: (float) Max value an ant can carry
            - ["Harvesting"]["Eat"]: (float) Value an ant eat to do a step
            - ["Harvesting"]["Collect"]: (float) Value an ant collect by stepping on food
            - ["Gathering"]/["Scouting"]["Diagonal Moves"]: (bool) Allow ants to use diagonals to travel
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
        self.gatherer_logic = Gatherer(board, knowledge, x, y, self.knowledge["Gathering"]["Diagonal Moves"],
                                       self.knowledge["Gathering"]["Sightline"],
                                       self.knowledge["Gathering"]["Light Compute"])
        self.scouting_logic = AdvancedScouter(board, knowledge, x, y, self.knowledge["Scouting"]["Diagonal Moves"],
                                              self.knowledge["Scouting"]["Sightline"],
                                              self.knowledge["Scouting"]["Light Compute"])

        self.stored = self.knowledge["Harvesting"]["Min"]
        self.starving = False

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

    def update(self):
        eat_ratio = self.knowledge["Harvesting"]["Eat"] * (Board.MAX_BLOB - self.board.get_blob(self.x, self.y)) \
                    / Board.MAX_BLOB
        self.drop = self.knowledge["Scouters"]["Drop by eat"] * eat_ratio
        DumbScouter.update(self)

        if not self.starving:
            self.stored -= eat_ratio
            self.stored = max(0, self.stored)

        if self.board.has_food(self.x, self.y):
            if len(self.knowledge['food']) == 1:
                wanted = min(self.knowledge["Harvesting"]["Min"], self.knowledge["Harvesting"]["Max"] - self.stored)
            else:
                wanted = min(self.knowledge["Harvesting"]["Collect"], self.knowledge["Harvesting"]["Max"] - self.stored)

            received, finished = self.board.eat_food(self.x, self.y, wanted)
            self.stored += received

            if finished:
                self.knowledge['food'].remove((self.x, self.y))

        if self.stored == 0 and not self.starving:
            self.starving = True
            self.init_gathering()

        if self.stored >= self.knowledge["Harvesting"]["Min"] and self.starving:
            self.starving = False
            self.init_scouting()
