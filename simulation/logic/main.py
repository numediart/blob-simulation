import random
import json

# from ant import Ant
# from gatherer import Gatherer
from simulation.logic.fsm_ant import FSMAnt
from simulation.board import Board


class Blob_Manager:

    DROP_VALUE = 25

    def __init__(self, board, max_scouters):
        """
        :type board: Board
        :type max_scouters: int
        """
        self.board = board
        self.knowledge = dict()
        self.knowledge['food'] = []
        self.knowledge['max_scouters'] = max_scouters
        self.scouters = []

        for _ in range(max_scouters):
            self.add_scouter()

    def save(self):
        return json.dumps(self.knowledge)

    def load(self, filename):
        with open(filename, 'r') as file:
            line = file.readline()
            json_acceptable_string = line.replace("'", "\"")
            k = json.loads(json_acceptable_string)
            self.knowledge['food'] = [tuple(x) for x in k['food']]
            self.knowledge['max_scouters'] = k['max_scouters']

            while len(self.scouters) < self.knowledge['max_scouters']:
                self.add_scouter()

    def move(self):
        deads = []
        for scouter in self.scouters:
            old = (scouter.x, scouter.y)
            scouter.move()
            if old == (scouter.x, scouter.y):
                deads.append(scouter)
            else:
                scouter.update()

            if self.board.has_food(scouter.x, scouter.y) and (scouter.x, scouter.y) not in self.knowledge['food']:
                self.food_discovered(scouter.x, scouter.y)

        for dead in deads:
            self.scouters.remove(dead)
            self.add_scouter()

    def add_scouter(self):
        if len(self.scouters) < self.knowledge['max_scouters']:
            if len(self.knowledge['food']) != 0:
                index = random.randrange(len(self.knowledge['food']))
                (x, y) = self.knowledge['food'][index]
            else:
                print("This will be nice in the future")
                x = 0
                y = 0

            self.scouters.append(FSMAnt(self.board, self.knowledge, x, y, Blob_Manager.DROP_VALUE))
        else:
            print("Max scouters already reached !")

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
        self.knowledge['max_scouters'] += 1

        for _ in range(1):
            self.scouters.append(FSMAnt(self.board, self.knowledge, x, y, Blob_Manager.DROP_VALUE))

        print("Food discovered in (" + str(x) + ", " + str(y) + ") - Total scouters : " + str(len(self.scouters)))
