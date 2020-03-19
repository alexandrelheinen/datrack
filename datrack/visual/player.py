import pygame
from enum import IntEnum
import numpy as np

from ..physics.point import KinematicPoint
from ..common import Derivatives, Axis2D
from ..utils import rotate_90

class Player(pygame.Rect):
    """A player instance."""

    def __init__(self, size, color, pos, vel):
        super().__init__(pos, size)
        self.color = color
        self.physics = KinematicPoint(1, np.vstack((pos, vel * np.ones(2))))
        self.pos_shift = .5 * np.array(size)

    def update(self, parent, dt):
        """Update the player state and draw it."""
        last_pos = np.copy(self._position())
        pred_pos = self.physics.predict(dt)[Derivatives.POSITION]

        if not parent.get_rect().collidepoint(pred_pos):
            points = list()
            x = last_pos - pred_pos
            for _ in range(4):
                x = rotate_90(x)
                if not parent.get_rect().collidepoint(pred_pos + x):
                    points.append(x)

            self.physics.collide_with(np.sum(points, axis=0))

        self.physics.propagate(dt)
        self.x, self.y = (self._position() - self.pos_shift).astype('int')
        pygame.draw.rect(parent, self.color, self)

    def handle_key(self, key):
        """Handle a key pressed."""
        raise NotImplementedError("Key handling")

    def handle_players(self, players):
        """Handle interaction of with other players."""
        raise NotImplementedError("Other players handling")

    def _position(self):
        """Return player 2D position."""
        return self.physics.state[Derivatives.POSITION]

    def _velocity(self):
        """Return player 2D velocity."""
        return self.physics.state[Derivatives.VELOCITY]


class UserPlayer(Player):
    """A player that is controlled by the user."""

    COLOR = (0, 0, 200)
    SIZE = (16, 16)

    def __init__(self, pos, vel):
        super().__init__(self.SIZE, self.COLOR, pos, vel)

    def handle_key(self, key):
        if key[pygame.K_UP]:
            self._velocity()[Axis2D.Y] = -abs(self._velocity()[Axis2D.Y])
        elif key[pygame.K_DOWN]:
            self._velocity()[Axis2D.Y] = abs(self._velocity()[Axis2D.Y])
        elif key[pygame.K_LEFT]:
            self._velocity()[Axis2D.X] = -abs(self._velocity()[Axis2D.X])
        elif key[pygame.K_RIGHT]:
            self._velocity()[Axis2D.X] = abs(self._velocity()[Axis2D.X])
        elif key[pygame.K_q]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_players(self, players):
        for p in players:
            if (p is not self) and self.colliderect(p):
                pygame.event.post(pygame.event.Event(pygame.QUIT))


class CpuPlayer(Player):
    """A player that just bounces everywhere."""

    COLOR = (200, 0, 0)
    SIZE = (10, 10)

    def __init__(self, pos, vel):
        super().__init__(self.SIZE, self.COLOR, pos, vel)

    def handle_key(self, key):
        pass

    def handle_players(self, players):
        pass

    @classmethod
    def randomize(cls, pos_range, origin, vel):
        """Randomize a CPU player away from the origin."""
        pos = np.array(origin)
        while np.linalg.norm(pos - origin) < np.linalg.norm(cls.SIZE):
            pos = np.array((np.random.randint(0, pos_range[0], 1),
                            np.random.randint(0, pos_range[1], 1))).flatten()

        return CpuPlayer(pos, vel)
