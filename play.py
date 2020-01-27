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
import argparse
import time
from os.path import exists, join, splitext
import os
import json

from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from simulation.interface import Interface
from simulation.board import Board
from simulation.player import Player
from simulation.logic.blob_manager import BlobManager

HIDE_GUI = 0
WINDOW_GUI = 1
BORDERLESS_GUI = 2
FULLSCREEN_GUI = 3

SCREEN_RESOLUTION = (1920, 1080)
DEFAULT_DIR = "simulation/default"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--height', type=int, default=40,
                        help='New game board height resolution if no input is given(default: 40)')
    parser.add_argument('--width', type=int, default=100,
                        help='New game board width resolution if no input is given(default: 100)')
    parser.add_argument('input', metavar="INPUT", type=str, nargs='?', default=None,
                        help='Initialize game from a save. Overwrite height and width parameters. '
                             'Pass the board filename as input (.board extension)')
    parser.add_argument('-s', '--scale', type=int, default=10,
                        help='Scales board resolution by this factor (default: x10)')
    parser.add_argument('--save', type=str, default="save/",
                        help="Pass the directory where saves are stored. (default: save/)")

    parser.add_argument('--computing_ratio', type=int, default=1,
                        help='how many times computing loop is done before drawing GUI')
    parser.add_argument('--auto_loops', type=int, default=-1,
                        help='set number of loops needed before saving and closing automatically')
    parser.add_argument('--display', type=int, default=WINDOW_GUI,
                        help="Set to '{}' to display as centered window, "
                             "'{}' to display as centered window with no border, "
                             "'{}' to display as fullscreen, "
                             "'{}' to hide display (only if auto_loops is set correctly)"
                        .format(WINDOW_GUI, BORDERLESS_GUI, FULLSCREEN_GUI, HIDE_GUI))
    parser.add_argument('--init_foods', type=int, default=0,
                        help='Starts the game by initializing a certain quantity of foods in one of the half-board')

    args = parser.parse_args()

    player_file = join(DEFAULT_DIR, "player.json")
    blob_file = join(DEFAULT_DIR, "blob.json")
    gui_file = join(DEFAULT_DIR, "interface.json")

    results = dict()

    if args.input is not None:
        assert exists(args.input)
        root_name = splitext(args.input)[0]

        results['From'] = root_name

        board = Board(args.width, args.height)
        board.load(args.input)

        if exists(root_name + ".player.json"):
            player_file = root_name + ".player.json"

        if exists(root_name + ".blob.json"):
            blob_file = root_name + ".blob.json"
    else:
        board = Board(args.width, args.height)

    blob = BlobManager(board, blob_file)
    player = Player(board, blob, player_file)

    if args.init_foods > 0:
        results['Init_foods'] = player.set_random_food(args.init_foods, not player.clean_top)

    mode = 0
    window_x = int((SCREEN_RESOLUTION[0] - board.width * args.scale) / 2)
    window_y = int((SCREEN_RESOLUTION[1] - board.height * args.scale) / 2)
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(window_x) + "," + str(window_y)

    if args.display == BORDERLESS_GUI:
        mode = mode | pygame.NOFRAME
    elif args.display == FULLSCREEN_GUI:
        mode = mode | pygame.FULLSCREEN
    elif args.display == HIDE_GUI:
        if args.auto_loops <= 0:
            args.display = WINDOW_GUI

    gui = Interface(board, player, blob, args.scale, args.save, mode, args.display == HIDE_GUI, gui_file)
    if args.auto_loops > 0:
        results['Loops'] = args.auto_loops
        gui.play = True

    init_counter = 100
    timer = time.time()
    counter = init_counter

    init_computing_ratio = args.computing_ratio
    ended = False
    while not ended and args.auto_loops != 0:
        computing_ratio = init_computing_ratio
        while computing_ratio > 0 and args.auto_loops != 0:
            if gui.play or gui.do_step:
                blob.move()
                gui.do_step = False
                if args.auto_loops > 0:
                    args.auto_loops -= 1

            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    ended = True
                else:
                    used = gui.event_listener(event)

                    # Quit automatic mode if user had interactions
                    if used and args.auto_loops != -1:
                        args.auto_loops = -1
                        print("User interaction detected ! \n\t --- Automatic mode stopped.")

            computing_ratio -= 1

        if args.display != HIDE_GUI:
            gui.draw()

        pygame.time.wait(10)

        counter -= 1
        if counter == 0:
            timing = time.time() - timer
            print("Loop mean time : {:.3f}s per iteration".format(timing / init_counter))
            counter = init_counter
            timer = time.time()

    if args.auto_loops == 0:
        name = gui.save()

        up_size_percent, down_size_percent = player.check_blob_cover()
        results['Covering'] = dict()
        results['Covering']['Total'] = (up_size_percent + down_size_percent)/2
        results['Covering']['Top'] = up_size_percent
        results['Covering']['Bottom'] = down_size_percent
        results['To'] = args.save + name

        with open(args.save + name + ".results.json", 'w') as file:
            json.dump(results, file, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
