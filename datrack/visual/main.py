import pygame
import numpy as np

from .player import UserPlayer, CpuPlayer

class MainWindow:
    """Application main window"""

    BLACK = (0, 0, 0)

    def __init__(self, args):
        npass, nfails = pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(args.size)
        self.players = [UserPlayer((0, 0), args.speed)]
        self.players += [CpuPlayer.randomize(args.size, (0, 0), args.speed)
                         for _ in range(args.nplayers)]
        self.rate = 60

    def run(self):
        while not self._has_quit_event():
            self._reset_screen()

            key = pygame.key.get_pressed()
            for p in self.players:
                p.handle_players(self.players)
                p.handle_key(key)
                p.update(self.screen, 1. / self.rate)

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(self.rate)

    def _reset_screen(self):
        self.screen.fill(self.BLACK)

    def _has_quit_event(self):
        return pygame.QUIT in [event.type for event in pygame.event.get()]
