import pygame
try:
    from game.variables import *
    from game.functions import *
except ImportError:
    from variables import *
    from functions import *

class Attack(pygame.sprite.Sprite):
    def __init__(self, ejection, relative_position, hitbox, startup, active_frames, hitstun, damage, player, name, sound_hit='sound_slap_m.ogg'):
        super().__init__()

        self.x_eject, self.y_eject = ejection
        self.size = hitbox
        self.x_location, self.y_location = relative_position
        if player.is_facing_right == False:
            self.x_eject *= -1
            self.x_location *= -1

        self.startup = startup
        self.active_frames = active_frames
        self.frame_index = 0
        self.name = name

        self.hitstun = hitstun
        self.damage = damage
        self.rect = pygame.Rect(window_size[0]+50,window_size[1]+50,1,1)
        self.player = player
        self.sound_hit = pygame.mixer.Sound(f'./Sound_effects/{sound_hit}')
        self.sound_move = pygame.mixer.Sound('./Sound_effects/sound_attack_movement.ogg')


    def draw_and_collision(self):
        real_x, real_y = get_real_pos(self.player)
        self.rect = pygame.Rect((real_x + self.player.hitbox[0]/2 + self.x_location - self.size[0]/2, real_y + self.player.hitbox[1]/2 + self.y_location - self.size[1]/2), self.size)
        if self.player.character == 'The_Cube' or show_hitbox:
            pygame.draw.rect(screen,(255,0,0),self.rect)
    
    def update(self):
        if self.frame_index < self.startup + self.active_frames:
            self.frame_index += 1
        else:
            self.kill()

        if self.player.hitstun > 0:
            self.kill()

        if self.frame_index >= self.startup:
            self.draw_and_collision()
            if self.frame_index == self.startup:
                self.sound_move.play()


class Grab(pygame.sprite.Sprite):
    def __init__(self, relative_position, hitbox, startup, active_frames, player):
        super().__init__()

        self.size = hitbox
        self.x_location, self.y_location = relative_position
        if player.is_facing_right == False:
            self.x_location *= -1

        self.frame_index = 0
        self.active_frames = active_frames
        self.startup = startup
        self.player = player

        self.rect = pygame.Rect((0, 0), (0, 0))
        self.sound_move = pygame.mixer.Sound('./Sound_effects/sound_attack_movement.ogg')


    def draw_and_collision(self):
        real_x, real_y = get_real_pos(self.player)
        self.rect = pygame.Rect((real_x + self.player.hitbox[0]/2 + self.x_location - self.size[0]/2, real_y + self.player.hitbox[1]/2 + self.y_location - self.size[1]/2), self.size)
        if self.player.character == 'The_Cube' or show_hitbox >= 1:
            pygame.draw.rect(screen,(255,0,0),self.rect)
    
    def update(self):
        if self.frame_index < self.startup + self.active_frames:
            self.frame_index += 1
        else:
            self.kill()

        if self.player.hitstun > 0 or self.player.grabbed[0]:
            self.kill()

        if self.frame_index >= self.startup:
            self.draw_and_collision()
            if self.frame_index == self.startup:
                self.sound_move.play()