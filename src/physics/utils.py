import numpy as np

from .common import Axis2D

def reflect_vector(v, n):
    """Reflect the vector v wrt a surface of normal vector n."""
    return v - 2. * np.dot(v, n) / np.dot(n, n) * n

def rotate_90(v):
    return np.array((v[Axis2D.Y], -v[Axis2D.X]))

# TODO: test me
