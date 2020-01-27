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


class Actions:

    UP = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, 1)

    LEFT_UP = (-1, -1)
    LEFT_DOWN = (-1, 1)
    RIGHT_UP = (1, -1)
    RIGHT_DOWN = (1, 1)

    ACTIONS_SIMPLE = [LEFT, RIGHT, DOWN, UP]
    ACTIONS_DIAG = [LEFT_UP, LEFT_DOWN, RIGHT_UP, RIGHT_DOWN]
    ACTIONS_ALL = ACTIONS_SIMPLE + ACTIONS_DIAG