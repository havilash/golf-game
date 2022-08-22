import pygame
import math

from constants import *


def calculate_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    dx, dy = math.pow((x2 - x1), 2), math.pow((y2 - y1), 2)
    d = math.sqrt(dx + dy)
    return d


def collide(obj1, obj2):
    offset = (obj2.x - obj1.x, obj2.y - obj1.y)
    poi = obj1.mask.overlap(obj2.mask, offset)  # point of intercept

    if poi:
        return poi
    return False


def load_image(path):  # scale 4 times bigger
    return pygame.transform.scale2x(pygame.transform.scale2x(pygame.image.load(path)))
