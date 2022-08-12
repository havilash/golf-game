import math
import pygame
import numpy as np
import sys

sys.path.append("../")
from constants import *
from .objects import GameObject



class Physic(GameObject):
    GRAVITY = 9.81*100  # gravity * meter (in pixels)

    def __init__(self, pos):
        super().__init__(pos)
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": 600,  # velocity x
            "vy": 300,  # velocity y
        }

        self.fps = 1
        self.frame_count = 0.0

    def update(self, fps, obstacle=None):
        self.fps = int(fps) if fps != 0 else FPS
        print(self.fps)
        self.frame_count += 1/self.fps

        if obstacle:
            for o in obstacle:
                collision = self.collide(o)
                if collision:
                    print(collision)
                    self.bounce(collision)

        # https://www.omnicalculator.com/physics/projectile-motion#:~:text=The%20equation%20for%20the%20distance,is%20acceleration%20due%20to%20gravity.
        mx = self.vel["vx"] * self.frame_count
        my = (
            self.vel["vy"] * self.frame_count - self.GRAVITY * self.frame_count**2 / 2
        )
        # print(mx, my)
        # print(self.vel, "\n")

        self.x = self.vel["w"] - mx
        self.y = self.vel["h"] - my

    def bounce(self, poi):
        px, py = poi
        px = np.interp(px, (0, self.size[0]), (-1, 1))
        py = np.interp(py, (0, self.size[1]), (-1, 1))

        px = abs(px)/px if px != 0 else 0
        py = abs(py)/py if py != 0 else 0

        print(px, py)

        # self.x -= 1*-px
        # self.y -= 1*-py
        # TODO  https://stackoverflow.com/questions/66744421/pygame-vector2-reflect-not-working-when-i-pass-an-argument
        mx = self.vel["vx"]
        my = self.vel["vy"] - self.GRAVITY * self.frame_count ** 2 / 2

        print("----------------------------------------------------", mx*px, my*py)

        self.set_velocity(mx*-px, my*-py)

    def collide(self, obstacle):
        mask = obstacle.mask
        offset = (obstacle.x - self.x, obstacle.y - round(self.y))
        poi = self.mask.overlap(mask, offset)  # point of intercept

        if poi:
            return poi
        return False

    def set_velocity(self, vx, vy):
        self.frame_count = 1/self.fps
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": vx,  # velocity x
            "vy": vy,  # velocity y
        }

    def calculate_velocity(self, v, a):  # initial velocity, alpha (angle), initial height
        self.frame_count = 1/self.fps
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": v * math.cos(a),  # velocity x
            "vy": v * math.sin(a),  # velocity y
        }


class Ball(Physic):
    size = (12, 12)  # a golf ball is 23.5 times smaller than a meter
    surface = pygame.Surface(size, pygame.SRCALPHA, 32)
    pygame.draw.circle(surface, "red", (size[0] / 2, size[1] / 2), size[0] / 2)

    def shoot(self, v, a):
        self.calculate_velocity(v, a)


