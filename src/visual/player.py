import pygame
import numpy as np
from enum import IntEnum

class Player(pygame.Rect):

    COLOR_STEP = 8

    class Axis(IntEnum):
        X = 0
        Y = 1

    def __init__(self, pos, size, vel, ctrlb):
        super().__init__(pos, size)
        self.color = (0, 0, 128) if ctrlb else (128, 0, 0)
        self.vel = np.ones(2) * vel  # [pixels/s]
        self.ctrlb = ctrlb
        self.corners = np.array(((0, 0), (0, size[1]), (size[0], 0), size))

    def draw(self, parent, dt):
        self.x, self.y = self.position() + self.vel * dt
        pygame.draw.rect(parent, self.color, self)

    def handle_key(self, key):
        if not self.ctrlb:
            return

        if key[pygame.K_UP]:
            self.vel[self.Axis.Y] = -abs(self.vel[self.Axis.Y])
        elif key[pygame.K_DOWN]:
            self.vel[self.Axis.Y] = abs(self.vel[self.Axis.Y])
        elif key[pygame.K_LEFT]:
            self.vel[self.Axis.X] = -abs(self.vel[self.Axis.X])
        elif key[pygame.K_RIGHT]:
            self.vel[self.Axis.X] = abs(self.vel[self.Axis.X])

    def handle_collision(self, screen, players):
        ret, points = self.check_collision(screen.get_rect())

        if ret and len(points) == 2:
            spax = (points[1] - points[0]) == 0
            self.vel[spax] *= -1

            print("col", spax)

        if self.ctrlb:
            for p in players:
                if p is not self and self.colliderect(p):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def position(self):
        return np.array((self.x, self.y))

    def check_collision(self, obj):
        is_outside = not obj.colliderect(self)

        if not is_outside:
            return False, None

        points = (self.position())[None, :] + self.corners
        col_points = [x for x in points if not obj.collidepoint(*x)]

        return True, col_points
