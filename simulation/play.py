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

from pygame.locals import QUIT
from simulation.interface import Interface
from simulation.board import Board
from simulation.player import Player
from simulation.logic.main import Blob_Manager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--height', type=int, default=40,
                        help='Board height resolution (default = 40)')
    parser.add_argument('--width', type=int, default=100,
                        help='Board width resolution (default = 100)')
    parser.add_argument('-s', '--scale', type=int, default=10,
                        help='Scaling from board resolution to window resolution (default = x10)')
    parser.add_argument('--init_from', type=str,
                        help='Initialize game from a save. Pass the board filename')
    parser.add_argument('--save_dir', type=str, default="save/",
                        help='Directory where saves are stored.')
    parser.add_argument('--computing_ratio', type=int, default=1,
                        help='how many times computing loop is done before drawing GUI')

    args = parser.parse_args()

    default_dir = "simulation/default"
    player_file = join(default_dir, "player.json")
    blob_file = join(default_dir, "blob.json")

    if args.init_from is not None:
        board_file = join(args.save_dir, args.init_from)
        assert exists(board_file)
        root_name = splitext(board_file)[0]

        board = Board(args.width, args.height)
        board.load(args.save_dir + args.init_from)

        if exists(root_name + ".player.json"):
            player_file = root_name + ".player.json"

        if exists(root_name + ".blob.json"):
            blob_file = root_name + ".blob.json"
    else:
        board = Board(args.width, args.height)

    blob = Blob_Manager(board, blob_file)
    player = Player(board, blob, player_file)

    gui = Interface(board, player, blob, args.scale, args.save_dir)

    init_counter = 100
    timer = time.time()
    counter = init_counter

    init_computing_ratio = args.computing_ratio
    ended = False
    while not ended:
        computing_ratio = init_computing_ratio
        while computing_ratio > 0:
            if gui.play or gui.do_step:
                blob.move()
                board.next_turn()
                gui.do_step = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    ended = True
                else:
                    gui.event_listener(event)

            computing_ratio -= 1

        gui.draw()

        pygame.time.wait(10)

        counter -= 1
        if counter == 0:
            timing = time.time() - timer
            print("Loop mean time : {:.3f}s per iteration".format(timing / init_counter))
            counter = init_counter
            timer = time.time()


if __name__ == "__main__":
    main()
