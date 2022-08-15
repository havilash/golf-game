import pygame
import sys

from golf_game.constants import *
from golf_game.utils import *


class GameObject:
    size: tuple = None
    surface: pygame.Surface = None
    bounciness = None
    friction = None

    def __init__(self, pos):
        self.x, self.y = pos

        self.mask = pygame.mask.from_surface(self.surface)
        self.rect = self.surface.get_rect()

    def draw(self, win: pygame.Surface):
        win.blit(self.surface, (self.x, self.y))


class Detector(GameObject):
    size = (1, 1)
    surface = pygame.Surface(size)

    def __init__(self, pos):
        super().__init__(pos)

    def collide(self, obstacle):
        return collide(self, obstacle)


class Obstacle(GameObject):
    bounciness = 0

    def __init__(self, pos, size):
        self.size = size
        self.surface = pygame.Surface(self.size)
        super().__init__(pos)

