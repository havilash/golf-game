import pygame

from constants import *
import game_objects


class Level(game_objects.GameObject):
    size = WIN_SIZE
    startpos = None
    endpos = None

    def __init__(self):
        self.x, self.y = (0, 0)

        self.draw_start()
        self.draw_end()

    def __iter__(self):
        return iter(self.surfaces)

    def draw(self, win: pygame.Surface):
        for obj in self.surfaces:
            obj.draw(win)

    def draw_start(self):
        pass

    def draw_end(self):
        pass


class Level1(Level):

    def __init__(self):
        self.surfaces = [
            game_objects.Obstacle((10, 550), (780, 30)),
            game_objects.Obstacle((100, 100), (30, 400)),
            game_objects.ImageObstacle((0, 0), game_objects.img.GROUND)
        ]

        super().__init__()


class Level2(Level):
    def __init__(self):
        self.surface = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
        super().__init__()


class Level3(Level):
    def __init__(self):
        self.surface = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)
        super().__init__()
