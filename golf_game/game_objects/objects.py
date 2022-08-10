import pygame
import sys

sys.path.append("..")
from constants import *


class GameObject:
    size = None
    surface = None

    def __init__(self, pos):
        self.x, self.y = pos

        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, win: pygame.Surface):
        win.blit(self.surface, (self.x, self.y))

    def get_mask(self):
        return self.mask

class test_obstacle(GameObject):

    def __init__(self, pos, size):
        self.size = size
        self.surface = pygame.Surface(self.size)
        super().__init__(pos)

