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

import pygame
import time
import datetime
import os.path

from pygame.locals import *
from simulation.board import Board


class Interface:

    FOOD_COLOR = (244, 210, 128) # (0, 150, 0)
    TOUCHED_COLOR = (218, 196, 136) # (50, 50, 0)
    BLOB_LOWER_COLOR = (206, 182, 86) # (255, 255, 0)
    BLOB_HIGHER_COLOR = (162, 106, 59) # (255, 0, 0)
    BACKGROUND = (120, 120, 120)

    def __init__(self, board, player, blob, scale, save_dir):
        """
        :type board: Board
        :type player: Player
        :type blob: Blob_Manager
        :type scale: float
        :type save_dir: str
        """
        pygame.init()
        # pygame.key.set_repeat(5, 50)

        self.board = board
        self.player = player
        self.blob = blob
        self.scale = scale

        self.save_dir = save_dir

        self.debug_mode = False
        self.play = False
        self.do_step = False
        self.show_ants = True

        width = self.board.width * scale
        height = self.board.height * scale
        self.window = pygame.display.set_mode((width, height))

        cross_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cross.png")

        discovered_food = pygame.image.load(cross_file).convert()
        discovered_food.set_colorkey((255, 255, 255))
        self.discovered_food = pygame.transform.scale(discovered_food, (scale, scale))

    def draw(self):

        width = self.board.width * self.scale
        height = self.board.height * self.scale

        game_surface = pygame.Surface((self.board.width, self.board.height))
        pixel_array = pygame.PixelArray(game_surface)

        for x in range(self.board.width):
            for y in range(self.board.height):
                pixel_array[x, y] = Interface.BACKGROUND

                if self.board.has_food(x, y):
                    pixel_array[x, y] = Interface.FOOD_COLOR

                if self.board.is_touched(x, y):
                    pixel_array[x, y] = Interface.TOUCHED_COLOR

                val = self.board.get_blob(x, y)
                if val != Board.MIN_BLOB:
                    val = (val - Board.MIN_BLOB) / (Board.MAX_BLOB - Board.MIN_BLOB)
                    red = (Interface.BLOB_HIGHER_COLOR[0] - Interface.BLOB_LOWER_COLOR[0]) * val + \
                          Interface.BLOB_LOWER_COLOR[0]
                    green = (Interface.BLOB_HIGHER_COLOR[1] - Interface.BLOB_LOWER_COLOR[1]) * val + \
                          Interface.BLOB_LOWER_COLOR[1]
                    blue = (Interface.BLOB_HIGHER_COLOR[2] - Interface.BLOB_LOWER_COLOR[2]) * val + \
                          Interface.BLOB_LOWER_COLOR[2]
                    pixel_array[x, y] = (red, green, blue)

        if self.show_ants:
            for scouter in self.blob.scouters:
                pixel_array[scouter.x, scouter.y] = (255, 255, 255)

        del pixel_array

        game_window = pygame.transform.scale(game_surface, (width, height))

        pygame.draw.line(game_window, (125, 125, 125), (0, height / 2), (width, height / 2))

        self.window.blit(game_window, (0, 0))
        for food in self.blob.knowledge['food']:
            self.window.blit(self.discovered_food, (food[0] * self.scale, food[1] * self.scale))
        pygame.display.flip()

    def save(self):
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H.%M.%S')

        print("Data saved at " + ts)
        f = open(self.save_dir + ts + ".board", 'w')
        f.write(self.board.save())
        f.close()

        f = open(self.save_dir + ts + ".blob.json", 'w')
        f.write(self.blob.save())
        f.close()

        f = open(self.save_dir + ts + ".player.json", 'w')
        f.write(self.player.save())
        f.close()

        pygame.image.save(self.window, self.save_dir + ts + ".jpg")

    def event_listener(self, event):

        # ADMIN ACTIONS
        if event.type == KEYDOWN and event.key == 100:  # D Letter
            self.debug_mode = not self.debug_mode
            print("Debug Mode: " + str(self.debug_mode))

        elif event.type == KEYDOWN and event.key == K_UP:
            Board.DECREASE_BLOB += 0.1
            print("Pheromone evaporation : " + str(Board.DECREASE_BLOB))

        elif event.type == KEYDOWN and event.key == K_DOWN:
            Board.DECREASE_BLOB -= 0.1
            print("Pheromone evaporation : " + str(Board.DECREASE_BLOB))

        elif event.type == KEYDOWN and event.key == K_SPACE:
            self.show_ants = not self.show_ants

        elif event.type == KEYDOWN and event.key == 115:  # S Letter
            self.save()

        # DEBUG ACTIONS
        elif self.debug_mode and event.type == MOUSEBUTTONDOWN and event.button == 1:  # Right Click
                x = int(pygame.mouse.get_pos()[0] / self.scale)
                y = int(pygame.mouse.get_pos()[1] / self.scale)
                self.board.update_blob(x, y, 10)

        # PLAYER ACTIONS
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Right Click
            x = int(pygame.mouse.get_pos()[0]/self.scale)
            y = int(pygame.mouse.get_pos()[1]/self.scale)
            if self.board.has_food(x, y):
                self.player.remove_food(x, y)
            else:
                self.player.set_food(x, y)

        elif event.type == KEYDOWN and event.key == 99:  # C Letter
            self.player.clean_board()

        elif event.type == KEYDOWN and event.key == 114:  # R Letter
            self.player.set_random_food(10, not self.player.clean_top)

        elif event.type == KEYDOWN and event.key == 104:  # H Letter
            up_size_percent, down_size_percent = self.player.check_blob_cover()
            print("Blob covering:")
            print("\t{:.2f}% of the board.".format((up_size_percent + down_size_percent)/2))
            print("\t{:.2f}% of the upper board.".format(up_size_percent))
            print("\t{:.2f}% of the lower board.".format(down_size_percent))

        # BLOB ACTIONS
        elif event.type == KEYDOWN and event.key == 112:  # P Letter
            self.play = not self.play

        elif event.type == KEYDOWN and event.key == K_RETURN:
            self.do_step = True

        elif event.type == KEYDOWN and event.key == 107:  # K Letter
            if self.blob.knowledge['min_scouters'] > 0:
                self.blob.knowledge['min_scouters'] -= 1
                print("New minimal scouters : " + str(self.blob.knowledge['min_scouters']) + " - Currently : " + str(len(self.blob.scouters)))

        elif event.type == KEYDOWN and event.key == 113:  # A letter
            self.blob.knowledge['min_scouters'] += 1
            print("New minimal scouters : " + str(self.blob.knowledge['min_scouters']) + " - Currently : " + str(len(self.blob.scouters)))

        elif event.type == KEYDOWN:
            print("Unrecognised key code : " + str(event.key))