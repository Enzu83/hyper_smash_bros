import pygame

try:
    from game.functions import get_real_pos
    from game.animation import import_folder
    from game.variables import screen
except ImportError:
    from functions import get_real_pos
    from animation import import_folder
    from variables import screen


class Cloud(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.animation = import_folder('animations/cloud')
        self.image_index = 0
        self.image = self.animation[int(self.image_index)]

        self.x, self.y = get_real_pos(player)
        self.x += player.hitbox[0]/2
        self.y += player.hitbox[1]/2

    def draw(self):
        screen.blit(self.image,(self.x - self.image.get_width()/2, self.y - self.image.get_height()/2))
    
    def update(self):
        if self.image_index < len(self.animation) - 1:
            self.image_index += 0.2
        else:
            self.kill()
        
        self.image = self.animation[int(self.image_index)]
        
        self.draw()