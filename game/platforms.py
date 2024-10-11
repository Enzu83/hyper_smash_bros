import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, position, texture):
        super().__init__()
        self.image = pygame.image.load(f'sprites/stages/{texture}.png')
        self.x, self.y = position
        self.rect = pygame.Rect(
            self.x, self.y, self.image.get_width(), 1)