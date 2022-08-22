import math
import pygame
import numpy as np
import sys

from golf_game.constants import *
from golf_game.utils import *
from . import objects


class Physic(objects.GameObject):
    GRAVITY = 9.81 * 100  # gravity * meter (in pixels)
    AIR_RESISTANCE = 0.99

    def __init__(self, pos):
        super().__init__(pos)
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": 0,  # velocity x
            "vy": 0,  # velocity y
        }

        self.detectors = [
            objects.Detector((0, 0)) for i in range(4)  # divisible by 4
        ]
        self.detector_positions = objects.Detector.find_detector_positions(self, len(self.detectors))

        self.frame_count = 0.0

    def update(self, obstacle=None, obstacle_list=None):
        self.frame_count += 1 / self.fps

        if obstacle:
            if collide(self, obstacle):
                kwargs = {"bounciness": obstacle.bounciness, "friction": obstacle.friction}
                self.bounce(obstacle, **{k: v for k, v in kwargs.items() if v is not None})  # kwargs without None
        elif obstacle_list:
            for obj in obstacle_list:
                if collide(self, obj):
                    kwargs = {"bounciness": obj.bounciness, "friction": obj.friction}
                    self.bounce(obj, **{k: v for k, v in kwargs.items() if v is not None})  # kwargs without None
                    break

        # https://www.omnicalculator.com/physics/projectile-motion#:~:text=The%20equation%20for%20the%20distance,is%20acceleration%20due%20to%20gravity.
        mx = (self.vel["vx"] * self.frame_count) * self.AIR_RESISTANCE
        my = (self.vel["vy"] * self.frame_count - self.GRAVITY * self.frame_count ** 2 / 2) * self.AIR_RESISTANCE

        self.x = int(self.vel["w"] - mx)
        self.y = int(self.vel["h"] - my)

    def bounce(self, obstacle, bounciness=0.8, friction=0.9):
        cx, cy = self.x + int(self.size[0] / 2), self.y + int(self.size[1] / 2)

        is_collided = []
        for i, detector in enumerate(self.detectors):
            detector.update_position(self.x + self.detector_positions[i][0], self.y + self.detector_positions[i][1])
            poi = detector.collide(obstacle)
            is_collided.append(poi)

        dirnx, dirny = 1, 1
        if is_collided[0]:
            dirnx, dirny = 1, -1
            self.y += 1
        elif is_collided[1]:
            dirnx, dirny = -1, 1
            self.x += -1
        elif is_collided[2]:
            dirnx, dirny = 1, -1
            self.y += -1
        elif is_collided[3]:
            dirnx, dirny = -1, 1
            self.x += 1

        mx = self.vel["vx"] * bounciness * friction
        my = (self.vel["vy"] - self.GRAVITY * (self.frame_count - 1 / self.fps)) * bounciness * friction

        self.set_velocity_data(mx * dirnx, my * dirny)

    def set_velocity_data(self, vx, vy):
        self.frame_count = 1 / self.fps
        self.vel = {
            "h": self.y,  # initial height
            "w": self.x,  # initial width
            "vx": vx,  # velocity x
            "vy": vy,  # velocity y
        }

    def calculate_velocity_data(self, v, a):  # initial velocity, alpha (angle), initial height
        self.frame_count = 1 / self.fps
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
