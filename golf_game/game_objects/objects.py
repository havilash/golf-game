import pygame
import sys

sys.path.append("..")
from constants import *


class GameObject:
    size: tuple = None
    surface: pygame.Surface = None

    def __init__(self, pos):
        self.x, self.y = pos

        self.mask = pygame.mask.from_surface(self.surface)
        self.rect = self.surface.get_rect()

    def draw(self, win: pygame.Surface):
        win.blit(self.surface, (self.x, self.y))


class test_obstacle(GameObject):

    def __init__(self, pos, size):
        self.size = size
        self.surface = pygame.Surface(self.size)
        super().__init__(pos)

