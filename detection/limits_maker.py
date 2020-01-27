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


class LimitsMaker:
    """
    Setup 4 points to define limits and returns them
    """

    def __init__(self, img, scale, window_name, name):
        self.limits = []
        self.max_limits = 4
        self.orig = img
        self.img = img.copy()
        self.scale = scale
        self.window_name = window_name
        self.done = False
        self.limits_drawn = False
        self.name = name

    def add_limit(self, x, y):
        """
        Add the pixel at the given position in the limits
        :param x: x value in the img
        :param y: y value in the img
        """
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
        print("--- " + self.name + ": Click on the {} corners.".format(self.max_limits))
        print("--- " + self.name + ": Please start from left corner and do it in the right order")

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP and not self.enough_data():
            if len(self.limits) < self.max_limits:
                self.add_limit(x, y)

    def clear(self):
        self.limits = []
        self.limits_drawn = False
        self.img = self.orig.copy()
        self.done = False

    def confirm(self):
        """
        Wait input key for clearing last color or ending food color setup
        """
        print("--- " + self.name + ": Press enter if you're ok with data or any other key if you want to restart "
                                   "setup...")
        key = cv2.waitKey(0) & 0xFF
        if key == 13:  # Enter
            print("--- " + self.name + ": " + str(self.compute()))
            self.done = True
        else:
            self.clear()
            self.help()
