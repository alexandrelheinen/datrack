import pygame
import numpy as np
from enum import IntEnum

from ..physics.point import KinematicPoint
from ..physics.common import Derivatives, Axis2D
from ..physics.utils import rotate_90

class Player(pygame.Rect):

    COLOR_STEP = 8

    def __init__(self, pos, size, vel, ctrlb):
        super().__init__(pos, size)
        self.ctrlb = ctrlb
        self.color = (0, 0, 128) if ctrlb else (128, 0, 0)
        state = np.vstack((pos, vel * np.ones(2)))
        self.physics = KinematicPoint(1, state)
        self.pos_shift = .5 * np.array(size)

    def update(self, parent, dt):
        last_pos = np.copy(self._pos())
        pred_pos = self.physics.predict(dt)[Derivatives.POSITION]

        if not parent.get_rect().collidepoint(pred_pos):
            points = list()
            x = last_pos - pred_pos
            for _ in range(4):
                x = rotate_90(x)
                if not parent.get_rect().collidepoint(pred_pos + x):
                    points.append(x)

            if len(points) != 2:
                raise RuntimeWarning("Collision with more than 2 points")

            self.physics.collide_with(np.sum(points, axis=0))

        self.physics.propagate(dt)
        self.x, self.y = (self._pos() - self.pos_shift).astype('int')
        pygame.draw.rect(parent, self.color, self)

    def _pos(self):
        return self.physics.state[Derivatives.POSITION]

    def _vel(self):
        return self.physics.state[Derivatives.VELOCITY]

    def handle_key(self, key):
        if not self.ctrlb:
            return

        if key[pygame.K_UP]:
            self._vel()[Axis2D.Y] = -abs(self._vel()[Axis2D.Y])
        elif key[pygame.K_DOWN]:
            self._vel()[Axis2D.Y] = abs(self._vel()[Axis2D.Y])
        elif key[pygame.K_LEFT]:
            self._vel()[Axis2D.X] = -abs(self._vel()[Axis2D.X])
        elif key[pygame.K_RIGHT]:
            self._vel()[Axis2D.X] = abs(self._vel()[Axis2D.X])
        elif key[pygame.K_q]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_collision(self, players):
        if not self.ctrlb:
            return

        for p in players:
            if p is not self and self.colliderect(p):
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def position(self):
        return np.array((self.x, self.y))
