import pygame
import math
import re

from constants import *

pygame.font.init()


class Text:
    color = "black"

    def __init__(self, center_pos, text, size=10, font="helvetica", color=color):
        self.center_pos = center_pos
        self.size = size
        self.text = text
        if re.match(r".+\.ttf$", font):
            self.font = pygame.font.Font(font, self.size)
        elif type(font) == pygame.font.Font:
            self.font = font
        else:
            self.font = pygame.font.SysFont(font, self.size)
        self.color = color

    def draw(self, win):
        self.surface = self.font.render(self.text, False, self.color)
        self.font_size = self.surface.get_size()
        self.pos = self.center_pos[0] - self.font_size[0] / 2, self.center_pos[1] - self.font_size[1] / 2
        self.x, self.y = self.pos

        win.blit(self.surface, self.pos)

    def set_text(self, text):
        self.text = text


class Button:
    color = "black"

    def __init__(self, pos, size, color=color, hover_color=color, text=None, text_color="white", font="helvetica",
                 font_size=None, font_color=None, func=None):
        self.pos = pos
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.font_size = font_size if font_size else int(self.size[1] * 0.7)
        self.font_color = font_color
        self.func = func

        if text: self.text_surface = Text((self.size[0] / 2 + self.pos[0], self.size[1] / 2 + self.pos[1]), self.text,
                                          self.font_size, color=self.font_color, font=self.font)

        self.crnt_color = color
        self.surface = pygame.Rect(*self.pos, *self.size)

    def draw(self, win):
        pygame.draw.rect(win, self.crnt_color, self.surface)
        self.text_surface.draw(win)

    def is_over(self, mpos):
        if self.surface.collidepoint(*mpos):
            self.crnt_color = self.hover_color
            return True
        self.crnt_color = self.color
        return False

    def call_back(self, *args, **kwargs):
        if self.func:
            self.func(*args, **kwargs)


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
