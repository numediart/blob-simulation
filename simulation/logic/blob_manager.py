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
import json

# from ant import Ant
# from gatherer import Gatherer
from simulation.logic.fsm_ant import FSMAnt
from simulation.board import Board


class BlobManager:

    def __init__(self, board, default_knowledge):
        """
        :type board: Board
        """
        self.board = board
        self.knowledge = dict()
        self.scouters = []

        with open(default_knowledge, 'r') as file:
            self.knowledge.update(json.load(file))

        self.knowledge['food'] = []
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.has_food(x, y) and self.board.is_touched(x, y):
                    self.knowledge['food'].append((x, y))

        self.knowledge['max_scouters'] = self.compute_max_scouters()
        while len(self.scouters) < self.knowledge['max_scouters']:
            self.add_scouter()

        print("Scouters: " + str(len(self.scouters)))

    def save(self):
        d = self.knowledge.copy()
        del d["food"]
        del d["max_scouters"]
        return json.dumps(d, indent=4, sort_keys=True)

    def move(self):
        deads = []
        for scouter in self.scouters:
            old = (scouter.x, scouter.y)
            scouter.move()
            if old == (scouter.x, scouter.y):
                deads.append(scouter)
            else:
                if self.board.has_food(scouter.x, scouter.y) and (scouter.x, scouter.y) not in self.knowledge['food']:
                    self.food_discovered(scouter.x, scouter.y)

                scouter.update()

        new_max = self.compute_max_scouters()
        if new_max != self.knowledge['max_scouters']:
            print("Scouters: " + str(new_max))
        self.knowledge['max_scouters'] = new_max

        scouters_qt = len(self.scouters)
        diff = self.knowledge['max_scouters'] - scouters_qt

        if diff > 0:
            for _ in range(diff):
                self.add_scouter()

        elif diff < 0:
            for _ in range(-diff):
                self.remove_scouter()

        for dead in deads:
            self.scouters.remove(dead)
            self.add_scouter()

        self.board.manage_blob(self.knowledge["Global Decrease"], self.knowledge["Remaining Blob on Food"])

    def add_scouter(self):
        if len(self.scouters) < self.knowledge['max_scouters']:
            if len(self.knowledge['food']) != 0:
                index = random.randrange(len(self.knowledge['food']))
                (x, y) = self.knowledge['food'][index]
            else:
                x, y = self.find_blob_square()

            self.scouters.append(FSMAnt(self.board, self.knowledge, x, y))
        else:
            print("Max scouters already reached !")

    def remove_scouter(self):
        nbr = random.randrange(len(self.scouters))
        del self.scouters[nbr]

    def compute_max_scouters(self):
        total_scouters = self.knowledge["Computing"]["Blob Size Factor"] * self.board.get_blob_total() \
                         + self.knowledge["Computing"]["Covering Factor"] * self.board.get_cover() \
                         + self.knowledge["Computing"]["Known Foods Factor"] * len(self.knowledge['food'])

        total_scouters *= (self.knowledge["Computing"]["Global Factor"] * (self.board.height * self.board.width / 100000))

        return max(self.knowledge["Scouters"]["Min"], int(total_scouters))

    def find_blob_square(self):
        availables = []
        total_blob = 0
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.is_touched(x, y):
                    qt = self.board.get_blob(x, y) + 1
                    total_blob += qt
                    availables.append(((x, y), qt))

        if len(availables) == 0:
            return 0, 0

        # Random need cast to integer
        # Floor cast will make sure a solution is found
        index_pond = random.randrange(int(total_blob))
        acc = 0
        for square, qt in availables:
            acc += qt
            if acc >= index_pond:
                return square

    def reset(self, x, y):
        for scouter in self.scouters.copy():
            if scouter.x == x and scouter.y == y:
                self.scouters.remove(scouter)

        for food in self.knowledge['food'].copy():
            if food == (x, y):
                self.knowledge['food'].remove(food)
                self.knowledge['max_scouters'] -= 1

    def food_discovered(self, x, y):
        self.knowledge['food'].append((x, y))
        # self.knowledge['max_scouters'] += 1

        # for _ in range(1):
        #     self.scouters.append(FSMAnt(self.board, self.knowledge, x, y, Blob_Manager.DROP_VALUE))

        # print("Food discovered in (" + str(x) + ", " + str(y) + ")")

    def food_destroyed(self, x, y):
        self.knowledge['food'].remove((x, y))
