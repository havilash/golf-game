import math
import pygame
import numpy as np
import sys

sys.path.append("..")
from constants import *
from .objects import GameObject



class Physic(GameObject):
    GRAVITY = 9.81*100  # Gravity * Meter (in pixels)

    def __init__(self, pos):
        super().__init__(pos)
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": 50,  # velocity x
            "vy": 0,  # velocity y
        }

        self.frame_count = 0.0

    def update(self, obstacle=None):
        self.update_frame_count()

        if obstacle:
            collision = self.collide(obstacle)
            if collision:
                self.bounce(collision)

        # https://www.omnicalculator.com/physics/projectile-motion#:~:text=The%20equation%20for%20the%20distance,is%20acceleration%20due%20to%20gravity.
        mx = self.vel["vx"] * self.frame_count
        my = (
            self.vel["vy"] * self.frame_count - self.GRAVITY * self.frame_count**2 / 2
        )
        print(mx, my)
        print(self.vel, "\n")

        self.x = self.vel["w"] - mx
        self.y = self.vel["h"] - my

    def bounce(self, poi):  # point of intercept
        px, py = poi
        px = np.interp(px, self.size, (-1, 1))
        py = np.interp(py, self.size, (-1, 1))

        # TODO
        mx = self.vel["vx"]
        my = self.vel["vy"] - self.GRAVITY * (self.frame_count-1) ** 2 / 2

        self.set_velocity(-mx, -my)

    def collide(self, obstacle):
        mask = obstacle.get_mask()
        offset = (obstacle.x - self.x, obstacle.y - round(self.y))
        poi = self.mask.overlap(mask, offset)  # point of intercept

        if poi:
            return poi
        return False

    def set_velocity(self, vx, vy):
        self.reset_frame_count()
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": vx,  # velocity x
            "vy": vy,  # velocity y
        }

    def calculate_velocity(self, v, a):  # Initial velocity, alpha (angle), initial height
        self.reset_frame_count()
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": v * math.cos(a),  # velocity x
            "vy": v * math.sin(a),  # velocity y
        }

    def update_frame_count(self):
        self.frame_count += 1/FPS

    def reset_frame_count(self):
        self.frame_count = 1/FPS


class Ball(Physic):
    size = (12, 12)  # a golf ball is 23.5 times smaller than a meter
    surface = pygame.Surface(size, pygame.SRCALPHA, 32)
    pygame.draw.circle(surface, "red", (size[0] / 2, size[1] / 2), size[0] / 2)

    def shoot(self):
        pass


