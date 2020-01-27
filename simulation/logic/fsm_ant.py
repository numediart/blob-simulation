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
from simulation.logic.advanced_scouter import AdvancedScouter


class FSMAnt(DumbScouter):

    """
    Adapting ant with several states :
        - scouting state where she search after new food (see AdvancedScouter)
        - gathering state where she collect food to stop starving (see Gatherer)

    Knowledge used:
        - ["Harvesting"]["Min"]: (float) Min value an ant has to store to stop being starved
        - ["Harvesting"]["Max"]: (float) Max value an ant can carry
        - ["Harvesting"]["Eat"]: (float) Value an ant eat to do a step
        - ["Harvesting"]["Collect"]: (float) Value an ant collect by stepping on food
        - ["Gathering"]/["Scouting"]["Diagonal Moves"]: (bool) Allow ants to use diagonals to travel
    """

    def __init__(self, board, knowledge, x, y):
        """
        :param board: A board class instance
        :param knowledge: a dict containing all blob knowledge and set up
        :param x: current horizontal position of the ant
        :param y: current vertical position of the ant
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
        """
        Move the ant based on the state she is using
        """
        if self.starving:
            self.gatherer_logic.move()
            self.x = self.gatherer_logic.x
            self.y = self.gatherer_logic.y
        else:
            self.scouting_logic.move()
            self.x = self.scouting_logic.x
            self.y = self.scouting_logic.y

    def init_gathering(self):
        """
        Reset gathering logic
        """
        self.gatherer_logic.reset()
        self.gatherer_logic.x = self.x
        self.gatherer_logic.y = self.y

    def init_scouting(self):
        """
        Reset scouting logic
        """
        self.scouting_logic.reset()
        self.scouting_logic.x = self.x
        self.scouting_logic.y = self.y

    def update(self):
        """
        Update square where the ant is, check state based on remaining stored food and collect food if square has any
        """

        # Update square and eat used value
        eat_ratio = self.knowledge["Harvesting"]["Eat"] * (Board.MAX_BLOB - self.board.get_blob(self.x, self.y)) \
                    / Board.MAX_BLOB
        self.drop = self.knowledge["Scouters"]["Drop by eat"] * eat_ratio
        DumbScouter.update(self)

        if not self.starving:
            self.stored -= eat_ratio
            self.stored = max(0, self.stored)

        # Collect food if square has any
        if self.board.has_food(self.x, self.y):
            if len(self.knowledge['food']) == 1:
                wanted = min(self.knowledge["Harvesting"]["Min"], self.knowledge["Harvesting"]["Max"] - self.stored)
            else:
                wanted = min(self.knowledge["Harvesting"]["Collect"], self.knowledge["Harvesting"]["Max"] - self.stored)

            received, finished = self.board.eat_food(self.x, self.y, wanted)
            self.stored += received

            if finished:
                self.knowledge['food'].remove((self.x, self.y))

        # Update FSM State
        if self.stored == 0 and not self.starving:
            self.starving = True
            self.init_gathering()

        if self.stored >= self.knowledge["Harvesting"]["Min"] and self.starving:
            self.starving = False
            self.init_scouting()
