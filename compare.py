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

import argparse
from simulation import board
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--first", required=True, help="first board file")
    ap.add_argument("--second", required=True, help="second board file")
    ap.add_argument("-s", "--scale", type=float, default=10,
                    help="Scales board resolution by this factor (default: x10)")
    ap.add_argument("-o", "--output", type=str, help="Give a name to save the jpeg file")
    args = ap.parse_args()

    board_1 = board.Board(0, 0)
    board_1.load(args.first)

    board_2 = board.Board(0, 0)
    board_2.load(args.second)

    board_comp = board_1.compare(board_2)

    if board_comp is None:
        return

    width = int(board_1.width * args.scale)
    height = int(board_1.height * args.scale)

    game_surface = pygame.Surface((board_1.width, board_1.height))
    pixel_array = pygame.PixelArray(game_surface)
    for x in range(board_1.width):
        for y in range(board_1.height):
            pixel_array[x, y] = (0, 0, 0)

            val = max(-255, min(board_comp.get_blob(x, y), 255))
            if val < 0:
                val = - val  # int(-val/2) + 125
                pixel_array[x, y] = (val/4, val/4, val)
            elif val > 0:
                val = val  # int(val/2) + 125
                pixel_array[x, y] = (val, val/4, val/4)
            else:
                if not board_comp.is_touched(x, y):
                    if board_1.is_touched(x, y):
                        pixel_array[x, y] = (75, 75, 125)
                    else:
                        pixel_array[x, y] = (125, 75, 75)

            if board_comp.has_food(x, y):
                pixel_array[x, y] = (0, board_comp.foods[x, y], 0)

    del pixel_array

    game_window = pygame.transform.scale(game_surface, (width, height))

    if args.output is not None:
        pygame.image.save(game_window, args.output)

    else:
        pygame.init()
        window = pygame.display.set_mode((width, height))
        window.blit(game_window, (0, 0))
        pygame.display.flip()

        ended = False
        while not ended:
            pygame.time.wait(10)
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    ended = True


if __name__ == "__main__":
    main()
