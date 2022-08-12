import sys

from constants import *
from utils import *
import game_objects


def draw(win: pygame.Surface, bg_surface, game_surface, level_surface, ball, test_obstacles):
    # reset surfaces
    bg_surface.fill("light blue")
    game_surface.fill((0, 0, 0, 0))
    level_surface.fill((0, 0, 0, 0))

    # draw objects
    for test_obstacle in test_obstacles:
        test_obstacle.draw(level_surface)

    # draw level, ball
    game_surface.blit(level_surface, (0, 0))
    ball.draw(game_surface)

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
    level_surface = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)

    test_obstacles = [
        game_objects.test_obstacle((10, 550), (780, 30)),
        game_objects.test_obstacle((100, 100), (10, 400))
    ]
    ball = game_objects.physics.Ball((700, 100))

    is_running = True
    clock = pygame.time.Clock()

    while is_running:
        time_passed = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

        ball.update(clock.get_fps(), test_obstacles)

        draw(win, bg_surface, game_surface, level_surface, ball, test_obstacles)

    pygame.quit()
    sys.exit()


main()
