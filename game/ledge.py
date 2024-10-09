import pygame
try:
    from game.variables import *
except ImportError:
    from variables import *

class Ledge(pygame.sprite.Sprite):
    def __init__(self, coordinates, direction):
        super().__init__()
        self.x, self.y = coordinates
        if direction == 'left':
            self.x -= global_ledge_hitbox[0]
        self.direction = direction
        self.is_available = True
        self.timer = 0
        self.rect = pygame.Rect((self.x, self.y), global_ledge_hitbox)

        self.upper_rect =  pygame.Rect((self.x, self.y - global_ledge_hitbox[1]), global_ledge_hitbox)

    def draw(self):
        if show_hitbox >= 1:
            pygame.draw.rect(screen,(0,0,255),self.rect)

    def update(self):
        self.draw()
        
        if self.timer > 1:
            self.timer -= 1
        elif self.timer == 1:
            self.timer = 0
            self.is_available = True
