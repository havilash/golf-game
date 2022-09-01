import pygame

from constants import *
import game_objects


class Level(game_objects.GameObject):
    size = WIN_SIZE
    surfaces = []
    startpos = None
    endpos = None
    # 20, 31
    img_ballpos = 20 / 40 * game_objects.img.END_IMAGE.get_size()[0], 31 / 35 * game_objects.img.END_IMAGE.get_size()[1]
    shoots = None

    def __init__(self):
        self.x, self.y = (0, 0)
        self.enddetector = game_objects.Detector(self.endpos);

    def __iter__(self):
        return iter(self.surfaces)

    @classmethod
    def get_borders(cls, thickness=10):
        borders = [
            game_objects.Obstacle((0, 0), (cls.size[0], thickness)),
            game_objects.Obstacle((cls.size[0] - thickness, 0), (thickness, cls.size[1])),
            game_objects.Obstacle((0, cls.size[1] - thickness), (cls.size[0], thickness)),
            game_objects.Obstacle((0, 0), (thickness, cls.size[1])),
        ]
        return borders

    def draw(self, win: pygame.Surface):
        for obj in self.surfaces:
            obj.draw(win)
        self.draw_start(win)
        self.draw_end(win)

    def draw_start(self, win: pygame.Surface):
        img = game_objects.img.START_IMAGE
        win.blit(img, (self.startpos[0] - self.img_ballpos[0], self.startpos[1] - self.img_ballpos[1]))

    def draw_end(self, win: pygame.Surface):
        img = game_objects.img.END_IMAGE
        win.blit(img, (self.endpos[0] - self.img_ballpos[0], self.endpos[1] - self.img_ballpos[1]))


class Level1(Level):
    startpos = 100, 590
    endpos = 900, 590
    shoots = float('inf')

    def __init__(self):
        self.surfaces = [
            *self.get_borders(),
            game_objects.Obstacle((350, 200), (20, self.size[1] - 200)),
            game_objects.Obstacle((0, 200), (200, 20)),
            game_objects.Obstacle((self.size[0] - 300, 0), (20, self.size[1] / 2 - 50)),
            game_objects.Obstacle((self.size[0] - 300, self.size[1] / 2 + 50), (20, self.size[1] / 2)),
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
