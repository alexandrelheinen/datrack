from enum import IntEnum


class Axis2D(IntEnum):
    """Bidimensional Cartesian axes."""
    X = 0
    Y = 1
    NUM_AXES = 2


class Derivatives(IntEnum):
    """
    Time derivatives of the position.
    By abuse of notation, the 0-th time derivative corresponds
    the position itself.
    """
    POSITION = 0
    VELOCITY = 1
    ACCELERATION = 2
    JERK = 3
    SNAP = 4
    CRACKLE = 5
    POP = 6
