
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