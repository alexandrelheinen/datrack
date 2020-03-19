from enum import IntEnum

import numpy as np
import math

from ..utils import reflect_vector
from ..common import Axis2D


class Point:
    """General point class."""

    def __init__(self):
        self.state = None  # Point state in any convenable unity

    def predict(self, timestep, input):
        """
        Predict the model behaviour during a timestep and return it (but
        do not update model state).
        """
        raise NotImplementedError("Propagation method is not implemented")

    def propagate(self, timestep, input):
        """
        Propagate the point state from a set of inputs throughout a timestep.
        """
        raise NotImplementedError("Propagation method is not implemented")


    def collide_with(self, obj):
        """Update the point state after a collision."""
        raise NotImplementedError("Collision method is not implemented")


class KinematicPoint(Point):
    """
    Kinematic point whose state is decribed by its position [pxl] on the screen
    along with its n-1 first time derivatives.

    The propagation is performed by applying the a constant n-th order time
    derivative [pxl/s^2] throughout the timestep [s]
    """

    def __init__(self, order, initial_state=None):
        """
        Create a point with given Kinematic order. The initial_state must
        be a numpy array.
        """
        super().__init__()
        self.n = order + 1
        self.state = np.zeros((self.n, Axis2D.NUM_AXES))

        self.set_state(initial_state)
        self.evolution_matrix = np.eye(self.n)

    def predict(self, timestep):
        A = np.array([[timestep**(j - i) * self._factor(j - i)
                       for j in range(self.n)]
                      for i in range(self.n)])
        return A @ self.state

    def propagate(self, timestep):
        self.state = self.predict(timestep)

    def collide_with(self, normal):
        if self.n == 0:
            return
        # TODO: enhance this definition
        for i in range(1, self.n):
            self.state[i] = reflect_vector(self.state[i], normal)

    def set_derivative(self, order, val):
        self.state[order] = val

    def set_state(self, state):
        if state is not None:
            if np.array_equal(self.state.shape, state.shape):
                np.copyto(self.state, state)
            else:
                raise TypeError("Initial state must have shape (%d, %d)"
                                % self.state.shape)

    def get_state(self):
        return np.copy(self.state)

    @staticmethod
    def _factor(k):
        return (1./math.factorial(k)) if k >= 0 else 0
