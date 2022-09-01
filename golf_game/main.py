import math
import os.path
import sys
import pygame
import numpy as np

from constants import *
from utils import *
import game_objects
import levels
import game


def main_menu():
    def draw(win: pygame.Surface, buttons, texts):
        win.fill(BG_COLOR)

        for button in buttons:
            button.draw(win)

        for text in texts:
            text.draw(win)

        pygame.display.update()

    win = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Golf Game")

    texts = [
        Text((WIN_SIZE[0] / 2, WIN_SIZE[1] / 4), "Golf Game", 100, font=FONT)
    ]
    buttons = {
        "start": Button((WIN_SIZE[0] / 2 - 200 / 2, WIN_SIZE[1] / 2 - 50 / 2), (200, 50),
                        text="Start", font=FONT, font_color=FONT_COLOR,
                        color=BG_COLOR,
                        hover_color=(150, 100, 255), func=game.game)
    }

    is_running = True
    clock = pygame.time.Clock()

    while is_running:
        time_passed = clock.tick(FPS)
        mpos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                    break

                if event.key == pygame.K_RETURN:
                    buttons["start"].call_back(win)

            for button in buttons.values():
                if button.is_over(mpos):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button == buttons["start"]:
                            button.call_back(win)

        draw(win, buttons.values(), texts)

    pygame.quit()
    sys.exit()


def main():
    main_menu()


main()
