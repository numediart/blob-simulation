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
import json
import datetime
import time
from shutil import copyfile
from os import path, makedirs

from detection.limits_maker import LimitsMaker
from detection.food_limits import FoodLimits
from detection.food_colors import FoodColors


def setup(setup_img, config_filename, scale=1.0, bkp_path="detection/bkp/"):
    """
    Display an image and show menu to setup every parameter in config.json file

    :param setup_img: a image filename to use to setup "config.json" file
    :param config_filename: the "config.json" file to load from and adapt
    :param scale: the scale to use for window with respect to image size
    :param bkp_path: path where old 'config_filename' will be saved for back up
    """
    img = cv2.imread(setup_img)
    height, width, _ = img.shape

    window_name = "Setup"
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, cv2.resize(img, (0, 0), fx=scale, fy=scale))
    cv2.setMouseCallback(window_name, null_callback)

    food_color = FoodColors(img, scale, window_name)
    board_setup = LimitsMaker(img, scale, window_name, "Board Setup")
    food_limits = FoodLimits(img, scale, window_name)
    setup_vars = {'Aspect Ratio': 1.0, 'Discrete Height': 100, 'Discrete Width': 100}

    # Load previous configurations
    if path.exists(config_filename):
        with open(config_filename, "r") as file:
            config = json.load(file)
        setup_vars['Aspect Ratio'] = config['Aspect Ratio']
        setup_vars['Discrete Height'] = config['Discrete Height']
        setup_vars['Discrete Width'] = config['Discrete Width']
        board_setup.limits = [tuple(x) for x in config['Limits']]
        food_color.colors.append(tuple(config["High Food Color"]))
        food_color.colors.append(tuple(config["Low Food Color"]))
        food_color.show_selected()
        food_limits.min_dist = config["Min Food Size"]

    def show_menu():
        print("\nCommands: ")
        print("\tEnter '1' to setup board limits")
        low, high = food_color.compute()
        print("\tEnter '2' to setup food color. (Current from {} to {})".format(low, high))
        print("\tEnter '3' to insert image aspect ratio. (Current: {})".format(setup_vars['Aspect Ratio']))
        print("\tEnter '4' to insert discrete image width and height. (Current: {}x{})"
              .format(setup_vars['Discrete Width'], setup_vars['Discrete Height']))
        print("\tEnter '5' to setup food limits. (Current min food size: {})".format(food_limits.min_dist))
        print("\tEnter 's' to save & quit")
        print("\tEnter 'q' to quit without saving")

    show_menu()
    done = False
    state = 0
    while not done:
        cv2.waitKey(10)

        if state == 0:  # Waiting commands
            cv2.imshow(window_name, cv2.resize(img, (0, 0), fx=scale, fy=scale))
            cv2.setMouseCallback(window_name, null_callback)

            key = input("Enter command: ")

            if key == "q":  # Quit without saving
                done = True

            elif key == "1":  # Setup board limits
                state = 1
                board_setup.help()
                cv2.setMouseCallback(window_name, board_setup.on_mouse)

            elif key == "2":  # Setup food color range
                state = 2
                food_color.help()
                cv2.setMouseCallback(window_name, food_color.on_mouse)

            elif key == "3":  # Insert aspect ratio value
                setup_vars['Aspect Ratio'] = -1
                while setup_vars['Aspect Ratio'] <= 0:
                    try:
                        setup_vars['Aspect Ratio'] = float(input("Insert image height by width ratio here: "))
                    except ValueError:
                        setup_vars['Aspect Ratio'] = -1

                    if setup_vars['Aspect Ratio'] <= 0:
                        print("Insert only a floating number with dot as separator.")

                show_menu()

            elif key == "4":  # Insert discrete width and height values
                setup_vars['Discrete Width'] = -1
                while setup_vars['Discrete Width'] <= 0:
                    try:
                        setup_vars['Discrete Width'] = int(input("Insert width discrete resolution: "))
                    except ValueError:
                        setup_vars['Discrete Width'] = -1

                    if setup_vars['Discrete Width'] <= 0:
                        print("Insert only round numbers.")

                setup_vars['Discrete Height'] = -1
                while setup_vars['Discrete Height'] <= 0:
                    try:
                        setup_vars['Discrete Height'] = int(input("Insert height discrete resolution: "))
                    except ValueError:
                        setup_vars['Discrete Height'] = -1

                    if setup_vars['Discrete Height'] <= 0:
                        print("Insert only round numbers.")

                show_menu()

            elif key == "5":  # Setup food size limits
                state = 3
                food_limits.clear()
                food_limits.help()
                cv2.setMouseCallback(window_name, food_limits.on_mouse)

            elif key == "s":  # Save configuration
                ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H.%M.%S-')
                if path.exists(config_filename):
                    if not path.exists(bkp_path):
                        makedirs(bkp_path)
                    copyfile(config_filename, bkp_path + ts + path.basename(config_filename))

                with open(config_filename, "w") as file:
                    json.dump({**setup_vars, **board_setup.toJSON(), **food_color.toJSON(), **food_limits.toJSON()},
                              file, indent=4, sort_keys=True)

                done = True

            else:
                print("Error: Unrecognised Command.")
                show_menu()

        elif state == 1:  # Adapt image to board limits setup
            board_setup.draw()
            if board_setup.done:
                state = 0
                show_menu()

        elif state == 2:  # Adapt image to food color setup
            food_color.draw()
            if food_color.done:
                state = 0
                show_menu()

        elif state == 3:  # Adapt image to food limits setup
            food_limits.draw()
            if food_limits.done:
                state = 0
                show_menu()


def null_callback(event, x, y, flags, param):
    return

