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

from detection.limits_maker import LimitsMaker
from math import sqrt


class FoodLimits(LimitsMaker):
    """
    Based on LimitsMaker, modify displayed names and record config as a minimal distance
    (and not 4 points as in LimitsMaker)
    """

    def __init__(self, img, scale, window_name):
        LimitsMaker.__init__(self, img, scale, window_name, "Food Setup")
        self.min_dist = 5

    def compute(self):
        # TODO Improve with warp perspective
        self.min_dist = self.img.shape[0]
        for i, (x,y) in enumerate(self.limits):
            dist = sqrt((x - self.limits[i-1][0])**2 + (y - self.limits[i-1][1])**2)
            self.min_dist = dist if dist < self.min_dist else self.min_dist
        return self.min_dist

    def toJSON(self):
        return {'Min Food Size': self.min_dist}

    def help(self):
        print("--- " + self.name + ": Click on the {} corners of the tiniest food".format(self.max_limits))
