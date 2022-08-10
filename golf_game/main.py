import sys

from utils import *
from game_objects import physics
from game_objects import objects



def draw(win: pygame.Surface, bg_surface, game_surface, ball, test_obstacle):
    bg_surface.fill("light blue")
    game_surface.fill((0, 0, 0, 0))

    test_obstacle.draw(game_surface)
    ball.draw(game_surface)

    win.blit(bg_surface, (0, 0))
    win.blit(game_surface, (0, 0))

    pygame.display.update()


def main():
    WIN = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Golf Game")

    BG_SURFACE = pygame.Surface(WIN_SIZE)
    GAME_SURFACE = pygame.Surface(WIN_SIZE, pygame.SRCALPHA)

    crnt_level = 0

    test_obstacle = objects.test_obstacle((10, 550), (780, 30))
    # test_obstacle = objects.test_obstacle((100, 100), (10, 400))
    ball = physics.Ball((700, 100))

    is_running = True
    clock = pygame.time.Clock()

    while is_running:
        time_passed = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break

        ball.update(test_obstacle)

        draw(WIN, BG_SURFACE, GAME_SURFACE, ball, test_obstacle)

    pygame.quit()
    sys.exit()


main()
