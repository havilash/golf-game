import math
import sys
import time

import pygame
import numpy as np

from constants import *
from utils import *
import game_objects
import levels


def draw(win: pygame.Surface, bg_surface, game_surface, texts, level, ball, is_shooting_line):
    # reset surfaces
    bg_surface.fill("light blue")
    game_surface.fill((0, 0, 0, 0))

    # draw level, ball
    level.draw(game_surface)
    ball.draw(game_surface)

    # draw objects
    if is_shooting_line:
        mx, my = pygame.mouse.get_pos()
        pygame.draw.line(game_surface, "black", (ball.x + ball.size[0] / 2, ball.y + ball.size[1] / 2), (mx, my), 2)

    # draw window
    win.blit(bg_surface, (0, 0))
    win.blit(game_surface, (0, 0))

    # texts
    for text in texts:
        text.draw(win)

    # update
    pygame.display.update()


def game(win):
    bg_surface = pygame.Surface(WIN_SIZE)
    game_surface = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)

    frame_count = 0

    crnt_level = 0
    level_list = [
        levels.Level1(),
        levels.Level2(),
        levels.Level3(),
    ]
    shoots = 0

    texts = {
        "shoots": Text((60, 40), str(level_list[crnt_level].shoots), 50, font=FONT),
        "level": Text((880, 40), "Level: " + str(crnt_level + 1), 50, font=FONT),
    }

    ball = game_objects.physics.Ball((0, 0))
    ball.x, ball.y = (
        level_list[crnt_level].startpos[0] - ball.size[0] / 2,
        level_list[crnt_level].startpos[1] - ball.size[1])

    finishing_time = None

    update_ball_physics = False
    is_shooting = True
    is_shooting_line = False

    run = True
    clock = pygame.time.Clock()
    while run:
        time_passed = clock.tick(FPS)
        mpos = pygame.mouse.get_pos()
        fps = clock.get_fps()
        game_objects.GameObject.update_fps(fps)
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break

            if not is_shooting and ball.calculate_initial_velocity() < 50 and update_ball_physics:
                is_shooting = True
                update_ball_physics = False
            if is_shooting and level_list[crnt_level].shoots > shoots:
                if event.type == pygame.MOUSEBUTTONDOWN and frame_count > fps:
                    if event.button == 1:
                        is_shooting_line = True
                        update_ball_physics = False
                if event.type == pygame.MOUSEBUTTONUP and is_shooting_line:
                    if event.button == 1:
                        is_shooting_line = False
                        is_shooting = False
                        update_ball_physics = True
                        shoots += 1
                        texts["shoots"].set_text(str(level_list[crnt_level].shoots - shoots))

                        # distance
                        x1, y1 = (ball.x + ball.size[0] / 2, ball.y + ball.size[1] / 2)
                        x2, y2 = mpos
                        dist = calculate_distance((x1, y1), (x2, y2)) * 3

                        # alpha angle
                        alpha = np.interp(math.degrees(math.atan2((y2 - y1), (x2 - x1))), (-180, 180), (0, 360))
                        ball.shoot(dist, alpha)

        # check if ball is on end
        if level_list[crnt_level].collide_end(ball) and finishing_time is None:
            finishing_time = time.time()
            update_ball_physics = False
            print("end")

        if finishing_time:
            if time.time() > finishing_time + 1:
                finishing_time = None
                is_shooting = True
                ball.x, ball.y = level_list[crnt_level].startpos[0] - ball.size[0] / 2, \
                                 level_list[crnt_level].startpos[1] - ball.size[1]

                if crnt_level + 1 < LEVELS:
                    crnt_level += 1
                else:
                    run = False
                texts["level"].set_text("Level: " + str(crnt_level + 1))

        if update_ball_physics:
            ball.update(obstacle_list=level_list[crnt_level])

        draw(win, bg_surface, game_surface, texts.values(), level_list[crnt_level], ball, is_shooting_line)
