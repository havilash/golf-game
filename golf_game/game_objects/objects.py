import pygame
import sys
import os

from golf_game.constants import *
from golf_game.utils import *


class GameObject:
    size: tuple = None
    fps = FPS
    surface: pygame.Surface = None
    bounciness = None
    friction = None

    def __init__(self, pos):
        self.x, self.y = pos

        self.mask = pygame.mask.from_surface(self.surface)
        self.rect = self.surface.get_rect()

    def draw(self, win: pygame.Surface):
        win.blit(self.surface, (self.x, self.y))

    @classmethod
    def update_fps(cls, fps):
        cls.fps = int(fps) if fps != 0 else FPS


class Detector(GameObject):
    size = (1, 1)
    surface = pygame.Surface(size)

    def __init__(self, pos):
        super().__init__(pos)

    def collide(self, obstacle):
        return collide(self, obstacle)

    def update_position(self, x, y):
        self.x, self.y = x, y

    @staticmethod
    def find_detector_positions(obj, amount):
        detector_positions = []

        perimeter = 2 * (obj.size[0] + obj.size[1])
        spacing = int(perimeter / amount)

        for i in range(int(obj.size[0] / 2), perimeter + int(obj.size[0] / 2), spacing):
            if i > obj.size[0] + obj.size[1] + obj.size[0]:
                val = (0, obj.size[1] - (i - (obj.size[0] + obj.size[1] + obj.size[0])))
            elif i > obj.size[0] + obj.size[1]:
                val = (obj.size[0] - (i - (obj.size[0] + obj.size[1])), obj.size[1])
            elif i > obj.size[0]:
                val = (obj.size[0], i - obj.size[0])
            else:
                val = (i, 0)

            detector_positions.append(val)

        return detector_positions


class Obstacle(GameObject):

    def __init__(self, pos, size):
        self.size = size
        self.surface = pygame.Surface(self.size)
        super().__init__(pos)


class ImageObstacle(GameObject):
    def __init__(self, pos, img, bounciness=None, friction=None):
        self.surface = img
        self.bounciness = bounciness if bounciness else self.bounciness
        self.friction = friction if friction else self.friction
        super().__init__(pos)
