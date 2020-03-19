from enum import IntEnum


class Axis2D(IntEnum):
    X = 0
    Y = 1
    NUM_AXES = 2


class Derivatives(IntEnum):
    POSITION = 0
    VELOCITY = 1
    ACCELERATION = 2
    JERK = 3
    SNAP = 4
    CRACKLE = 5
    POP = 6
