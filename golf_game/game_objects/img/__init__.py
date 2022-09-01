import os
import pygame

START_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("game_objects", "img", "start.png")), (120, 105))
END_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("game_objects", "img", "end.png")), (120, 105))
