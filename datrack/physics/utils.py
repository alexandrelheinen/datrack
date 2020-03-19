import numpy as np

from .common import Axis2D

def reflect_vector(v, n):
    """Reflect the vector v wrt a surface of normal vector n."""
    return v - 2. * np.dot(v, n) / np.dot(n, n) * n

def rotation_matrix_from_angle(angle):
    """Return the rotation matrix associated to an angle."""
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array(((c, -s), (s, c)))

def rotate_vector(v, angle):
    """Rotate a vector for a given angle."""
    return rotation_matrix_from_angle(angle) @ v

def rotate_90(v):
    """Rotate a vector of 90 degrees (fast implementation)."""
    return np.array((v[Axis2D.Y], -v[Axis2D.X]))

# TODO: test me
