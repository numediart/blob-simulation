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


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", default='data/_MG_0133.JPG', help="input image")
    ap.add_argument("-s", "--scale", type=float, default=0.25, help="based on the image shapes, scale the results by this factor")
    ap.add_argument("-f", "--file", type=str, default="setup.json", help="name file to save setup")

    args = vars(ap.parse_args())

    img = cv2.imread(args["input"])
    height, width, _ = img.shape
    scale = args["scale"]

    window_name = "Setup"
    cv2.namedWindow(window_name)
    show_menu()

    food_color = FoodColor(img, scale, window_name)
    board_setup = BoardLimits(img, scale, window_name)

    done = False
    state = 0
    while not done:
        key = cv2.waitKey(10)

        if state == 0:
            if key == ord("q"):
                done = True

            elif key == ord("1"):
                state = 1
                board_setup.clear()
                board_setup.help()
                cv2.setMouseCallback(window_name, board_setup.on_mouse)

            elif key == ord("2"):
                state = 2
                food_color.clear()
                food_color.help()
                cv2.setMouseCallback(window_name, food_color.on_mouse)

            elif key == ord("s"):
                with open(args["file"], "w") as file:
                    json.dump({**board_setup.toJSON(), **food_color.toJSON()}, file)
                done = True

        if state == 1:
            board_setup.draw()
            if board_setup.done:
                state = 0
                show_menu()

        elif state == 2:
            food_color.draw()
            if food_color.done:
                state = 0
                show_menu()

        else:
            cv2.imshow(window_name, cv2.resize(img, (0, 0), fx=scale, fy=scale))
            cv2.setMouseCallback(window_name, null_callback)


def show_menu():
    print("\nCommands : ")
    print("\tPress '1' to setup board limits")
    print("\tPress '2' to setup food color")
    print("\tPress 's' to save & quit")
    print("\tPress 'q' to quit without saving")


def null_callback(event, x, y, flags, param):
    return


class BoardLimits:

    def __init__(self, img, scale, window_name):
        self.limits = []
        self.max_limits = 4
        self.middle = []
        self.max_middle = 2
        self.adjusted_middle = []
        self.orig = img
        self.img = img.copy()
        self.scale = scale
        self.window_name = window_name
        self.done = False
        self.limits_drawn = False
        self.middle_drawn = False

    def add_limit(self, x, y):
        x_img = int(x / self.scale)
        y_img = int(y / self.scale)
        self.limits.append((x_img, y_img))
        cv2.drawMarker(self.img, (x_img, y_img), (0, 0, 255), thickness=5)

    def add_middle(self, x, y):
        x_img = int(x / self.scale)
        y_img = int(y / self.scale)
        self.middle.append((x_img, y_img))
        cv2.drawMarker(self.img, (x_img, y_img), (0, 255, 0), thickness=5)

    def draw(self):
        if len(self.limits) == self.max_limits and not self.limits_drawn:
            for i, limit in enumerate(self.limits):
                cv2.line(self.img, self.limits[i-1], limit, (0, 0, 255), thickness=3)
            self.limits_drawn = True

        if len(self.middle) == self.max_middle and not self.middle_drawn:
            cv2.line(self.img, self.middle[0], self.middle[1], (0, 255, 0), thickness=3)

            self.adjusted_middle.append(self.project_point(self.limits[0], self.limits[-1], self.middle[0]))
            self.adjusted_middle.append(self.project_point(self.limits[1], self.limits[2], self.middle[1]))
            cv2.drawMarker(self.img, self.adjusted_middle[0], (255, 0, 0), thickness=5)
            cv2.drawMarker(self.img, self.adjusted_middle[1], (255, 0, 0), thickness=5)
            cv2.line(self.img, self.adjusted_middle[0], self.adjusted_middle[1], (255, 0, 0), thickness=3)

            self.middle_drawn = True

        cv2.imshow(self.window_name, cv2.resize(self.img, (0, 0), fx=self.scale, fy=self.scale))

        if self.enough_data():
            self.confirm()

    def enough_data(self):
        return len(self.limits) == self.max_limits and len(self.middle) == self.max_middle

    def compute(self):
        return self.limits, self.middle

    def toJSON(self):
        return {'Limits': self.limits, 'Middle': self.middle, 'Adjusted': self.adjusted_middle}

    def project_point(self, v1, v2, p):
        e1 = (v2[0] - v1[0], v2[1] - v1[1])
        e2 = (p[0] - v1[0], p[1] - v1[1])
        dp = e1[0] * e2[0] + e1[1] * e2[1]
        dist = e1[0]**2 + e1[1]**2
        px = int(v1[0] + (dp * e1[0] / dist))
        py = int(v1[1] + (dp * e1[1] / dist))
        return px, py

    def help(self):
        print("--- Board Setup: Click on the {} corners of the board and "
              "then on each side of the half board separation".format(self.max_limits))
        print("--- Board Setup: Please start from left corner and do it in the right order ")

    def clear(self):
        self.limits = []
        self.limits_drawn = False
        self.middle = []
        self.middle_drawn = False
        self.adjusted_middle = []
        self.img = self.orig.copy()
        self.done = False

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP and not self.enough_data() :
            if len(self.limits) < self.max_limits:
                self.add_limit(x, y)
            else:
                self.add_middle(x, y)

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