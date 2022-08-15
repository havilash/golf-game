import math
import sys
import pygame
import numpy as np

from constants import *
from utils import *
import game_objects
import levels


def draw(win: pygame.Surface, bg_surface, game_surface, level, ball, is_shooting_line):
    # reset surfaces
    bg_surface.fill("light blue")
    game_surface.fill((0, 0, 0, 0))

    # draw level, ball
    level.draw(game_surface)
    ball.draw(game_surface)

    # draw objects
    if is_shooting_line:
        mx, my = pygame.mouse.get_pos()
        pygame.draw.line(game_surface, "black", (ball.x + ball.size[0]/2, ball.y + ball.size[1]/2), (mx, my), 2)

    # cx, cy = ball.x + int(ball.size[0] / 2), ball.y + int(ball.size[1] / 2)
    # points = [(cx, ball.y), (cx, ball.y + ball.size[1]), (ball.x, cy), (ball.x + ball.size[0], cy)]
    # for point in points:
    #     pygame.draw.rect(game_surface, "black", pygame.Rect(point[0], point[1], 5, 5))

    # draw window
    win.blit(bg_surface, (0, 0))
    win.blit(game_surface, (0, 0))

    # update
    pygame.display.update()


def main():
    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Golf Game")

    bg_surface = pygame.Surface(WIN_SIZE)
    game_surface = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)

    crnt_level = 0
    levels_list = [
        levels.Level1(),
        levels.Level2(),
        levels.Level3(),
    ]

    ball = game_objects.physics.Ball((700, 100))
    ball.calculate_velocity_data(500, 0)

    is_shooting = True
    is_shooting_line = False

    is_running = True
    clock = pygame.time.Clock()

    while is_running:
        time_passed = clock.tick(FPS)
        game_objects.physics.Physic.update_fps(clock.get_fps())
        mpos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.x, ball.y = mpos
                is_shooting = True
            if is_shooting:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    is_shooting_line = True
                if event.type == pygame.MOUSEBUTTONUP:
                    is_shooting_line = False
                    is_shooting = False

                    # distance
                    x1, y1 = (ball.x + ball.size[0]/2, ball.y + ball.size[1]/2)
                    x2, y2 = mpos
                    dist = calculate_distance((x1, y1), (x2, y2))*5

                    # alpha angle
                    alpha = np.interp(math.degrees(math.atan2((y2-y1),(x2-x1))), (-180, 180), (0, 360))
                    ball.calculate_velocity_data(dist, alpha)

        if is_shooting is False:
            ball.update(levels_list[crnt_level])

        draw(win, bg_surface, game_surface, levels_list[crnt_level], ball, is_shooting_line)

    pygame.quit()
    sys.exit()


main()
