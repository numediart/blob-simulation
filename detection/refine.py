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

import cv2
from simulation.board import Board
from simulation.player import Player


def simulate(discrete_img, discrete_blob, discrete_food_list, config, refine=None):

    height, width = discrete_blob.shape

    board = Board(width, height)
    player = Player(board, None, "simulation/default/player.json")
    player.food_size = compute_discrete_food_size(config, player.use_circle)
    player.clean_top = refine['Clean Top'] if refine is not None else True

    for (x, y) in discrete_food_list:
        if board.is_touched(x, y):
            # TODO Set up value
            board.set_food(x, y, value=Board.INIT_FOOD/2)
        else:
            board.set_food(x, y)

    for x in range(width):
        for y in range(height):
            if discrete_blob[y, x] != 0:
                board.update_blob(x, y, discrete_blob[y, x])

    if refine is not None:
        adapt_food(board, player, config, refine)

    return board, player, discrete_img


def adapt_food(board, player, config, refine):
    square_size = round(1 / refine["Width"] * config["Discrete Width"])

    adding_food = 0

    for food_origin in refine["Foods"]:
        discrete_food = (int(food_origin[0] / refine["Width"] * config["Discrete Width"]),
                         int(food_origin[1] / refine["Height"] * config["Discrete Height"]))

        food_found = False
        for i in range(square_size):
            for j in range(square_size):
                if board.has_food(discrete_food[0] + i, discrete_food[1] + j):
                    food_found = True

        if not food_found:
            # TODO Set up value
            player.set_food(round(discrete_food[0] + square_size/2), round(discrete_food[1] + square_size/2),
                            force=True, value=Board.INIT_FOOD/4)
            adding_food += 1

    print("Foods added: {}".format(adding_food))


def save(filename, board, player, img):
    with open(filename + ".board", 'w') as file:
        file.write(board.save())

    with open(filename + ".player.json", 'w') as file:
        file.write(player.save())

    cv2.imwrite(filename + ".jpg", img)


def compute_discrete_food_size(config, use_circle=False):

    food_size = config["Min Food Size"]
    limits = config["Limits"]
    x_min = limits[0][0]
    x_max = limits[0][0]
    y_min = limits[0][1]
    y_max = limits[0][1]

    for limit in limits:
        x_min = min(x_min, limit[0])
        x_max = max(x_max, limit[0])

        y_min = min(y_min, limit[1])
        y_max = max(y_max, limit[1])

    img_width = x_max - x_min
    img_height = y_max - y_min

    if use_circle:
        ratio = 1.5  # ~sqrt(2)
    else:
        ratio = 1

    discrete_food_size = round((food_size / img_height * config["Discrete Height"]
                                + food_size / img_width * config["Discrete Width"]) * ratio / 2)

    return discrete_food_size
