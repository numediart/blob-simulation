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
import numpy as np


class FoodColors:
    """
    Setup color range for foods by getting min and max values for r,g,b channels
    """
    def __init__(self, img, scale, window_name):
        self.colors = []
        self.orig = img
        self.img = img.copy()
        self.scale = scale
        self.window_name = window_name
        self.done = False

    def add(self, x, y):
        """
        Add the color pixel at the given position in the food range
        :param x: x value in the img
        :param y: y value in the img
        """
        x_img = int(x / self.scale)
        y_img = int(y / self.scale)
        self.colors.append(self.orig[y_img, x_img])
        self.show_selected()

    def show_selected(self):
        """
        Adapt img pixels concerned by the actual range to red
        """
        if len(self.colors) >= 2:
            low, high = self.compute()
            mask = cv2.inRange(self.img, np.array(low, dtype=np.uint8), np.array(high, dtype=np.uint8))
            maskrgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

            selected = np.zeros(self.img.shape, dtype=np.uint8)
            selected[:, :, 2] = mask

            self.img = cv2.add(cv2.subtract(self.img, maskrgb), selected)

    def draw(self):
        cv2.imshow(self.window_name, cv2.resize(self.img, (0, 0), fx=self.scale, fy=self.scale))
        self.confirm()

    def compute(self):
        """
        Compute color range
        :return: first tuple is the lowest values found in colors for rgb channels, second tuple is for highest values
        """
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
        print("--- Color Setup: Click several times on foods to setup food color and then press enter.")

    def clear(self):
        self.colors = []
        self.img = self.orig.copy()
        self.done = False

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            self.add(x, y)

    def confirm(self):
        """
        Wait input key for clearing last color or ending food color setup
        """
        key = cv2.waitKey(10) & 0xFF
        if key == 13:  # Enter
            print("--- Color Setup: " + str(self.compute()))
            self.done = True
        elif len(self.colors) > 0 and key == 8:  # Backspace
            del self.colors[len(self.colors)-1]
            self.img = self.orig.copy()
            self.show_selected()
            print("Last color removed. {} remaining(s).".format(len(self.colors)))
