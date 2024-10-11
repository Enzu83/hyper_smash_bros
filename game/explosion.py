import pygame
try:
    from game.variables import *
except ImportError:
    from variables import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('sprites/miscellaneous/explosion.png')
        pygame.mixer.Sound('sounds/sfx/sound_explosion.ogg').play()
        self.frame = 20
        self.x, self.y = position
        while self.x < 0:
            self.x += 1
        while self.x > window_size[0]:
            self.x -= 1
        while self.y < 0:
            self.y += 1
        while self.y > window_size[1]:
            self.y -= 1

    def draw(self):
        screen.blit(self.image,(self.x - self.image.get_width()/2, self.y - self.image.get_height()/2))
    
    def update(self):
        if self.frame > 0:
            self.frame -= 1
        else:
            self.kill()
        
        self.draw()