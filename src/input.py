MOVEMENT_SPEED = 5
DEAD_ZONE = 0.05

class SNESButton():
    """ Enum for SNES controller buttons """
    A: int = 0
    B: int = 1
    X: int = 2
    Y: int = 3
    L: int = 4
    R: int = 5
    SELECT: int = 6
    START: int = 7
    UP: int = 8
    DOWN: int = 9
    LEFT: int = 10
    RIGHT: int = 11

class N64Button():
    """ Enum for N64 controller buttons """
    A: int = 2
    B: int = 1
    Z: int = 6
    C_UP: int = 9
    C_DOWN: int = 3
    C_LEFT: int = 0
    C_RIGHT: int = 8
    L: int = 4
    R: int = 5
    START: int = 12

    # TODO: THESE AREN'T REGISTERING!!!
    UP: int = 4
    DOWN: int = 5
    LEFT: int = 6
    RIGHT: int = 7


class DragonRiseButton():
    """ Enum for DragonRise controller buttons """
    A: int = 0
    B: int = 1
    X: int = 2
    Y: int = 3
    L: int = 4
    R: int = 5
    SELECT: int = 6
    START: int = 7
    UP: int = 8
    DOWN: int = 9
    LEFT: int = 10
    RIGHT: int = 11
