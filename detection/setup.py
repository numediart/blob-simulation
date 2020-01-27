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
import cv2
import json
import datetime
import time
from shutil import copyfile
from os.path import exists
from os import makedirs


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="input image")
    ap.add_argument("-s", "--scale", type=float, default=0.25, help="scales input image by this factor (default: x0.25)")
    ap.add_argument("-c", "--config", type=str, default="config.json",
                    help="name file to save config (default: config.json)")

    args = vars(ap.parse_args())

    img = cv2.imread(args["input"])
    height, width, _ = img.shape
    scale = args["scale"]

    window_name = "Setup"
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, cv2.resize(img, (0, 0), fx=scale, fy=scale))
    cv2.setMouseCallback(window_name, null_callback)
    show_menu()

    food_color = FoodColor(img, scale, window_name)
    board_setup = BoardLimits(img, scale, window_name)

    done = False
    state = 0
    setup_vars = {'Aspect Ratio': 1.0, 'Discrete Height': 100, 'Discrete Width': 100}
    while not done:
        cv2.waitKey(10)

        if state == 0:
            cv2.imshow(window_name, cv2.resize(img, (0, 0), fx=scale, fy=scale))
            cv2.setMouseCallback(window_name, null_callback)

            key = input("Enter command: ")

            if key == "q":
                done = True

            elif key == "1":
                state = 1
                board_setup.clear()
                board_setup.help()
                cv2.setMouseCallback(window_name, board_setup.on_mouse)

            elif key == "2":
                state = 2
                food_color.clear()
                food_color.help()
                cv2.setMouseCallback(window_name, food_color.on_mouse)

            elif key == "3":
                setup_vars['Aspect Ratio'] = -1
                while setup_vars['Aspect Ratio'] <= 0:
                    try:
                        setup_vars['Aspect Ratio'] = float(input("Insert image height by width ratio here: "))
                    except ValueError:
                        setup_vars['Aspect Ratio'] = -1

                    if setup_vars['Aspect Ratio'] <= 0:
                        print("Insert only a floating number with dot as separator.")

                show_menu()

            elif key == "4":
                setup_vars['Discrete Height'] = -1
                while setup_vars['Discrete Height'] <= 0:
                    try:
                        setup_vars['Discrete Height'] = int(input("Insert height discrete resolution: "))
                    except ValueError:
                        setup_vars['Discrete Height'] = -1

                    if setup_vars['Discrete Height'] <= 0:
                        print("Insert only round numbers.")

                setup_vars['Discrete Width'] = -1
                while setup_vars['Discrete Width'] <= 0:
                    try:
                        setup_vars['Discrete Width'] = int(input("Insert width discrete resolution: "))
                    except ValueError:
                        setup_vars['Discrete Width'] = -1

                    if setup_vars['Discrete Width'] <= 0:
                        print("Insert only round numbers.")

                show_menu()

            elif key == "s":
                ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H.%M.%S-')
                if exists(args["config"]):
                    if not exists("bkp/"):
                        makedirs("bkp")
                    copyfile(args["config"], "bkp/" + ts + args["config"])

                with open(args["config"], "w") as file:
                    json.dump({**setup_vars, **board_setup.toJSON(), **food_color.toJSON()}, file)

                done = True

            else:
                print("Error: Unrecognised Command.")
                show_menu()

        elif state == 1:
            board_setup.draw()
            if board_setup.done:
                state = 0
                show_menu()

        elif state == 2:
            food_color.draw()
            if food_color.done:
                state = 0
                show_menu()


def show_menu():
    print("\nCommands: ")
    print("\tEnter '1' to setup board limits")
    print("\tEnter '2' to setup food color")
    print("\tEnter '3' to insert image aspect ratio")
    print("\tEnter '4' to insert discrete image height and width")
    print("\tEnter 's' to save & quit")
    print("\tEnter 'q' to quit without saving")


def null_callback(event, x, y, flags, param):
    return


class BoardLimits:

    def __init__(self, img, scale, window_name):
        self.limits = []
        self.max_limits = 4
        self.orig = img
        self.img = img.copy()
        self.scale = scale
        self.window_name = window_name
        self.done = False
        self.limits_drawn = False

    def add_limit(self, x, y):
        x_img = int(x / self.scale)
        y_img = int(y / self.scale)
        self.limits.append((x_img, y_img))
        cv2.drawMarker(self.img, (x_img, y_img), (0, 0, 255), thickness=5)

    def draw(self):
        if len(self.limits) == self.max_limits and not self.limits_drawn:
            for i, limit in enumerate(self.limits):
                cv2.line(self.img, self.limits[i-1], limit, (0, 0, 255), thickness=3)
            self.limits_drawn = True

        cv2.imshow(self.window_name, cv2.resize(self.img, (0, 0), fx=self.scale, fy=self.scale))

        if self.enough_data():
            self.confirm()

    def enough_data(self):
        return len(self.limits) == self.max_limits

    def compute(self):
        return self.limits

    def toJSON(self):
        return {'Limits': self.limits}

    def help(self):
        print("--- Board Setup: Click on the {} corners of the board".format(self.max_limits))
        print("--- Board Setup: Please start from left corner and do it in the right order")

    def clear(self):
        self.limits = []
        self.limits_drawn = False
        self.img = self.orig.copy()
        self.done = False

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP and not self.enough_data() :
            if len(self.limits) < self.max_limits:
                self.add_limit(x, y)

    def confirm(self):
        print("--- Board Setup: Press enter if you're ok with data or any other key if you want to restart setup...")
        key = cv2.waitKey(0)
        if key == 13:  # Enter
            print("--- Board Setup: " + str(self.compute()))
            self.done = True
        else:
            self.clear()
            self.help()


class FoodColor:

    def __init__(self, img, scale, window_name, max_qt=0):
        self.colors = []
        self.orig = img
        self.img = img.copy()
        self.scale = scale
        self.max_qt = max_qt
        self.window_name = window_name
        self.done = False

    def add(self, x, y):
        x_img = int(x / self.scale)
        y_img = int(y / self.scale)
        self.colors.append(self.orig[y_img, x_img])
        cv2.drawMarker(self.img, (x_img, y_img), (0, 0, 255), thickness=5)

    def draw(self):
        cv2.imshow(self.window_name, cv2.resize(self.img, (0, 0), fx=self.scale, fy=self.scale))
        if self.enough_data():
            self.confirm()

    def enough_data(self):
        if self.max_qt == 0:
            key = cv2.waitKey(10)
            return key == 13  # Enter
        else:
            return len(self.colors) == self.max_qt

    def compute(self):
        low_color = [255, 255, 255]
        high_color = [0, 0, 0]

        if len(self.colors) == 0:
            return tuple(high_color), tuple(low_color)

        for color in self.colors:
            for i, c in enumerate(color):
                if c < low_color[i]:
                    low_color[i] = c

                if c > high_color[i]:
                    high_color[i] = c

        return tuple(low_color), tuple(high_color)

    def toJSON(self):
        l, h = self.compute()
        l = tuple([int(x) for x in l])
        h = tuple([int(x) for x in h])
        return {'Low Food Color': l, 'High Food Color': h}

    def help(self):
        if self.max_qt == 0:
            print("--- Color Setup: Click several times on foods to setup food color and then press enter.")
        else:
            print("--- Color Setup: Click {} times on food to setup food color".format(self.max_qt))

    def clear(self):
        self.colors = []
        self.img = self.orig.copy()
        self.done = False

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP and not self.enough_data() :
            self.add(x, y)

    def confirm(self):
        print("--- Color Setup: Press enter if you're ok with data or any other key if you want to restart setup...")
        key = cv2.waitKey(0)
        if key == 13:  # Enter
            print("--- Color Setup: " + str(self.compute()))
            self.done = True
        else:
            self.clear()
            self.help()


if __name__ == "__main__":
    main()