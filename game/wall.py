import pygame
try:
    from game.variables import *
    from game.functions import *
except ImportError:
    from variables import *
    from functions import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, position, texture):
        super().__init__()
        self.image = pygame.image.load(f'stage_sprites/{texture}.png')
        self.x, self.y = position
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())