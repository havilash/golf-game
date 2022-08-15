import math
import pygame
import numpy as np
import sys

from golf_game.constants import *
from golf_game.utils import *
from . import objects


class Physic(objects.GameObject):
    GRAVITY = 9.81*100  # gravity * meter (in pixels)
    AIR_RESISTANCE = 0.99
    fps = FPS

    def __init__(self, pos):
        super().__init__(pos)
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": 0,  # velocity x
            "vy": 0,  # velocity y
        }

        self.detectors = {
            "n": objects.Detector((0, 0)),
            "e": objects.Detector((0, 0)),
            "s": objects.Detector((0, 0)),
            "w": objects.Detector((0, 0)),
        }

        self.frame_count = 0.0

    @classmethod
    def update_fps(cls, fps):
        cls.fps = int(fps) if fps != 0 else FPS

    def update(self, obstacle=None):
        self.frame_count += 1/self.fps

        if obstacle:
            collision = collide(self, obstacle)
            if collision:
                kwargs = {"bounciness": obstacle.bounciness, "friction": obstacle.friction}
                self.bounce(obstacle, **{k: v for k, v in kwargs.items() if v is not None})  # kwargs without None

        # https://www.omnicalculator.com/physics/projectile-motion#:~:text=The%20equation%20for%20the%20distance,is%20acceleration%20due%20to%20gravity.
        mx = (self.vel["vx"] * self.frame_count) * self.AIR_RESISTANCE
        my = (self.vel["vy"] * self.frame_count - self.GRAVITY * self.frame_count**2 / 2) * self.AIR_RESISTANCE
        if collision:
            print(mx, my)

        self.x = int(self.vel["w"] - mx)
        self.y = int(self.vel["h"] - my)
        if collision:
            print()

    def bounce(self, obstacle, bounciness=0.8, friction=0.9):
        cx, cy = self.x + int(self.size[0]/2), self.y + int(self.size[1]/2)

        points = [(cx, self.y), (self.x + self.size[0], cy), (cx, self.y + self.size[1]), (self.x, cy)]
        points_collided = []
        for i, val in enumerate(self.detectors.items()):
            key, detector = val
            detector.x, detector.y = points[i]
            poi = detector.collide(obstacle)
            points_collided.append(poi)

        dirnx, dirny = 1, 1
        if points_collided[0]:
            dirnx, dirny = 1, -1
            self.y += 1
        elif points_collided[1]:
            dirnx, dirny = -1, 1
            self.x += -1
        elif points_collided[2]:
            dirnx, dirny = 1, -1
            self.y += -1
        elif points_collided[3]:
            dirnx, dirny = -1, 1
            self.x += 1

        mx = self.vel["vx"] * bounciness * friction
        my = (self.vel["vy"] - self.GRAVITY * (self.frame_count-1/self.fps)) * bounciness * friction

        self.set_velocity_data(mx*dirnx, my*dirny)

        print(self.vel)

    def set_velocity_data(self, vx, vy):
        self.frame_count = 1/self.fps
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": vx,  # velocity x
            "vy": vy,  # velocity y
        }

    def calculate_velocity_data(self, v, a):  # initial velocity, alpha (angle), initial height
        self.frame_count = 1/self.fps
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": v * math.cos(math.radians(a)),  # velocity x
            "vy": v * math.sin(math.radians(a)),  # velocity y
        }


class Ball(Physic):
    size = (12, 12)  # a golf ball is 23.5 times smaller than a meter
    surface = pygame.Surface(size, pygame.SRCALPHA, 32)
    pygame.draw.circle(surface, "red", (size[0] / 2, size[1] / 2), size[0] / 2)

    def shoot(self, v, a):
        self.calculate_velocity_data(v, a)


