import pygame
import numpy as np

from .player import Player

class MainWindow:
    """Application main window"""

    BLACK = (0, 0, 0)

    PLAYER_SIZE = (10, 10)
    CPU_SIZE = (7, 7)

    def __init__(self, args):
        npass, nfails = pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(args.size)
        self.players = [Player((0, 0), self.PLAYER_SIZE, args.speed, True)]
        self.players += [Player(np.random.randint(0, 300, 2),
                                self.CPU_SIZE,
                                args.speed,
                                False)
                         for _ in range(args.nplayers)]
        self.rate = 60

    def run(self):
        while not self._has_quit_event():
            self._reset_screen()

            key = pygame.key.get_pressed()
            for p in self.players:
                p.handle_collision(self.players)
                p.handle_key(key)
                p.update(self.screen, 1. / self.rate)

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(self.rate)

    def _reset_screen(self):
        self.screen.fill(self.BLACK)

    def _has_quit_event(self):
        return pygame.QUIT in [event.type for event in pygame.event.get()]
