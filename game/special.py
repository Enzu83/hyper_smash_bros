import pygame
try:
    from game.variables import attacks
    from game.attack import *
except ImportError:
    from variables import attacks
    from attack import *

class Electric_Ball(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.name = 'electric_ball'
        self.image = pygame.image.load(f'sprites/{self.name}.png').convert_alpha()

        self.x = player.x + player.hitbox_position[0] + player.hitbox[0]/2 - self.image.get_width()/2
        self.y = player.y + player.hitbox_position[1] + player.hitbox[1]/2 - self.image.get_height()/2
        self.hitbox = self.image.get_size()

        self.xspeed, self.yspeed = (5, 4)
        self.x_eject, self.y_eject = (1, 0)
        if player.is_facing_right == False:
            self.xspeed *= -1
            self.x_eject *= -1
        
        self.hitstun = 5
        self.damage = 4
        self.player = player
        self.on_wall = False
        self.rect = pygame.Rect((self.x , self.y), self.hitbox)
        self.sound_hit = pygame.mixer.Sound('Sound_effects/sound_electric_s.ogg')

    def collision(self, offset):
        collide = False
        self.rect = pygame.Rect((self.x + offset[0], self.y + offset[1]), self.hitbox)

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                collide = True
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.y + self.hitbox[1] == platform.y and self.yspeed >= 0:
                collide = True
        
        return collide

    def position(self):
        for _ in range (true_floor(self.xspeed)):
            if self.collision((sign(self.xspeed), 0)) == False:
                self.x += sign(self.xspeed)
            else:
                self.kill()
                break

        for _ in range(true_floor(self.yspeed)):
            if self.collision((0, 1)) == False:
                self.y += sign(self.yspeed)
            else:
                self.on_wall = True
                self.yspeed = -2
                self.y -= 1
                break

    def check_wall(self):
        if self.on_wall:
            self.yspeed += 0.2

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def update(self):
        if self.x + self.image.get_width() < - 192 or self.x > window_size[0] + 256 or self.y > window_size[1] + 192 or self.y + self.image.get_height() < - 192:
            self.kill()
        
        self.check_wall()
        self.position()

        self.draw()

def special_initialization(self):
    ############### LUFFY ###############
    if self.character == 'Luffy':
        #### UP SPECIAL ####
        if self.special_attack == 'up_special':
            pass
        
        #### SIDE SPECIAL ####
        elif self.special_attack == 'side_special':
            self.apply_gravity = False
            if self.xspeed >= 0:
                self.is_facing_right = True
            else:
                self.is_facing_right = False
        
        #### NEUTRAL SPECIAL ####
        elif self.special_attack == 'neutral_special':
            pass
    
    ############### GOKU ###############
    elif self.character == 'Goku':
        #### UP SPECIAL ####
        if self.special_attack == 'up_special':
            self.tp_rect = pygame.rect.Rect(get_real_pos(self), self.hitbox)
        
        #### SIDE SPECIAL ####
        elif self.special_attack == 'side_special':
            pass

    ############### PIKACHU ###############
    if self.character == 'Pikachu':
        #### UP SPECIAL ####
        if self.special_attack == 'up_special':
            self.direction = ['','']
            self.tp_rect = pygame.rect.Rect(get_real_pos(self), self.hitbox)
            self.freeze_image = True
        
        #### SIDE SPECIAL ####
        elif self.special_attack == 'side_special':
            pass
        
        #### NEUTRAL SPECIAL ####
        elif self.special_attack == 'neutral_special':
            pass

def special(self):
    ############### LUFFY ###############
    if self.character == 'Luffy':
        #### UP SPECIAL ####
        if self.special_attack == 'up_special':
            self.still_on_wall()
            self.attack_frame += 1
            if self.attack_frame < 25:
                self.yspeed /= 1.07
            if self.attack_frame == 25:
                self.yspeed = -10
                self.y -= 1
                pygame.mixer.Sound('./Sound_effects/sound_attack_movement.ogg').play()
                attacks.add(Attack((0, 3), (6, 50), (32, 32), 0, 2, 10, 8, self, ''))
            
            if self.attack_frame == 65:
                self.doing_special = False
                if self.on_wall == False:
                    self.free_fall = True
                self.freeze_image = False
                self.attack_frame = 0
                self.image_index = 0
        
        #### SIDE SPECIAL ####
        elif self.special_attack == 'side_special':
            if self.attack_frame <= 3:
                if self.xspeed >= 0:
                    self.is_facing_right = True
                else:
                    self.is_facing_right = False
            else:
                self.yspeed = 0

            if self.attack_frame == 35:
                attacks.add(Attack((1, -6), (14,0), (28, 49), 0, 13, 8, 6, self, '', 'sound_kick_s.ogg'))
            if self.attack_frame >= 20:
                self.image_index = 4
                self.xspeed = -24*((self.attack_frame - 5)/25) * (1 - (self.attack_frame - 5)/25)
                if self.is_facing_right == False:
                    self.xspeed *= -1
            else:
                self.xspeed /= 1.1
                if abs(self.xspeed) < 1:
                    self.xspeed = 0

            if self.attack_frame < 45:
                self.attack_frame += 1
            else:
                self.doing_special = False
                if solid_collision(self,(0,1)) == False:
                    self.free_fall = True
                    self.on_wall = False
                    self.apply_gravity = True
                self.freeze_image = False
                self.attack_frame = 0
                self.image_index = 0
                self.lag = 25
            
        #### NO ATTACK ####
        else:
            self.doing_special = False
            if self.on_wall == False:
                self.free_fall = True
            self.freeze_image = False
            self.attack_frame = 0
            self.image_index = 0
    ############### MARTH ###############
    elif self.character == 'Marth':
        #### UP SPECIAL ####
        if self.special_attack == 'up_special':
            self.attack_frame += 1
            if self.attack_frame < 7:
                self.yspeed /= 1.04
            if self.attack_frame == 7:
                pygame.mixer.Sound('./Sound_effects/sound_slash_m.ogg').play()
                attacks.add(Attack((0, 3), (6, 50), (32, 32), 0, 2, 10, 8, self, ''))
                self.y -= 1
            if self.attack_frame > 7:
                self.yspeed = -35 + 4.3*(self.attack_frame - 7)
                self.xspeed = (self.attack_frame - 7)/1.5
                if self.is_facing_right == False:
                    self.xspeed *= -1
                self.on_wall = False

            
            if self.yspeed > 0 and self.attack_frame > 7:
                self.xspeed = 0
                self.yspeed = 0
                self.doing_special = False
                self.free_fall = True
                self.apply_gravity = True
                self.freeze_image = False
                self.attack_frame = 0
                self.image_index = 0
                self.lag = 5
        
        #### SIDE SPECIAL ####
        elif self.special_attack == 'side_special':
            self.doing_special = False
            if self.on_wall == False:
                self.free_fall = True
            self.freeze_image = False
            self.attack_frame = 0
            self.image_index = 0
        
        #### NEUTRAL SPECIAL ####
        elif self.special_attack == 'neutral_special':
            self.doing_special = False
            if self.on_wall == False:
                self.free_fall = True
            self.freeze_image = False
            self.attack_frame = 0
            self.image_index = 0
        #### NO ATTACK ####
        else:

            self.doing_special = False
            if self.on_wall == False:
                self.free_fall = True
            self.freeze_image = False
            self.attack_frame = 0
            self.image_index = 0
    ############### GOKU ###############
    elif self.character == 'Goku':
        #### UP SPECIAL ####
        if self.special_attack == 'up_special':
            if self.attack_frame < 40:
                pygame.draw.polygon(screen, color_list[self.player], get_triangle(self))
                self.yspeed /= 1.04
                self.attack_frame += 1

                tp_pos = [self.tp_rect.x + self.tp_rect.size[0]/2, self.tp_rect.y + self.tp_rect.size[1]/2]          
                center = get_center_pos(self)

                direction = ['', '']

                if self.key_left:
                    if center[0] - tp_pos[0] < 120:
                        direction[0] = 'left'
                if self.key_right:
                    if tp_pos[0] - center[0] < 120:
                        direction[0] = 'right'
    
                if self.key_up:
                    if center[1] - tp_pos[1] < 120:
                        direction[1] = 'up'
                if self.key_down:
                    if center[1] - tp_pos[1] > -120:
                        direction[1] = 'down'


                for _ in range(8):
                    if direction[0] == 'left' and not rect_collision(self.tp_rect, (-1, 0)):
                        self.tp_rect.x -= 1
                    if direction[0] == 'right' and not rect_collision(self.tp_rect, (1, 0)):
                        self.tp_rect.x += 1
                    
                    if direction[1] == 'up' and not rect_collision(self.tp_rect, (0, -1)):
                        self.tp_rect.y -= 1
                    if direction[1] == 'down' and not rect_collision(self.tp_rect, (0, 1)):
                        self.tp_rect.y += 1
                    
                #pygame.draw.rect(screen, (255, 0, 255), self.tp_rect)
            else:
                self.invincibility_frame = 0
                self.is_invincible = True
                self.invincibility_duration = 5

                self.xspeed = 0
                self.yspeed = 0
                
                self.x = int(self.tp_rect.x - self.hitbox_position[0])
                self.y = int(self.tp_rect.y - self.hitbox_position[1])
                self.doing_special = False
                
                if solid_collision(self,(0,1)) == False:
                    self.free_fall = True
                    self.on_wall = False
                    self.apply_gravity = True
                    self.lag = 5
                else:
                    self.lag = 10
                self.freeze_image = False
                self.attack_frame = 0
                self.image_index = 0

                pygame.mixer.Sound('Sound_effects/sound_instant_transmission.ogg').play()
        
        #### SIDE SPECIAL ####
        elif self.special_attack == 'side_special':
            self.doing_special = False
            if self.on_wall == False:
                self.free_fall = True
            self.freeze_image = False
            self.attack_frame = 0
            self.image_index = 0
        
        #### NEUTRAL SPECIAL ####
        elif self.special_attack == 'neutral_special':
            self.doing_special = False
            if self.on_wall == False:
                self.free_fall = True
            self.freeze_image = False
            self.attack_frame = 0
            self.image_index = 0
        #### NO ATTACK ####
        else:

            self.doing_special = False
            if self.on_wall == False:
                self.free_fall = True
            self.freeze_image = False
            self.attack_frame = 0
            self.image_index = 0
    ############### PIKACHU ###############
    elif self.character == 'Pikachu':
        #### UP SPECIAL ####
        if self.special_attack == 'up_special':
            if 5 < self.attack_frame < 35:
                if self.attack_frame < 30:
                    self.image_index = 0
                pygame.draw.polygon(screen, color_list[self.player], get_triangle(self))
                self.yspeed /= 1.04
                self.attack_frame += 1

                tp_pos = [self.tp_rect.x + self.tp_rect.size[0]/2, self.tp_rect.y + self.tp_rect.size[1]/2]          
                center = get_center_pos(self)

                if self.key_left:
                    if center[0] - tp_pos[0] < 100:
                        self.direction[0] = 'left'
                if self.key_right:
                    if tp_pos[0] - center[0] < 100:
                        self.direction[0] = 'right'
    
                if self.key_up:
                    if center[1] - tp_pos[1] < 100:
                        self.direction[1] = 'up'
                if self.key_down:
                    if center[1] - tp_pos[1] > -100:
                        self.direction[1] = 'down'

                for _ in range(80):
                    if self.direction[0] == 'left' and not rect_collision(self.tp_rect, (-1, 0)):
                        if check_tp_wall(self, 'left'):
                            self.tp_rect.x -= 1
                        else:
                            break
                    if self.direction[0] == 'right' and not rect_collision(self.tp_rect, (1, 0)):
                        if check_tp_wall(self, 'right'):
                            self.tp_rect.x += 1
                        else:
                            break
                    
                    if self.direction[1] == 'up' and not rect_collision(self.tp_rect, (0, -1)):
                        if check_tp_wall(self, 'up'):
                            self.tp_rect.y -= 1
                        else:
                            break
                    if self.direction[1] == 'down' and not rect_collision(self.tp_rect, (0, 1)):
                        if check_tp_wall(self, 'down'):
                            self.tp_rect.y += 1
                        else:
                            break
                    
                pygame.draw.rect(screen, (255, 0, 255), self.tp_rect)
            if self.attack_frame == 25:
                self.invincibility_frame = 0
                self.is_invincible = True
                self.invincibility_duration = 2
                
                self.x = int(self.tp_rect.x - self.hitbox_position[0])
                self.y = int(self.tp_rect.y - self.hitbox_position[1])
                self.tp_rect = pygame.rect.Rect(get_real_pos(self), self.hitbox)

                self.image = pygame.image.load(f'animations/Pikachu/up_special/up_b_{self.direction[1]}_{self.direction[0]}.png').convert_alpha()

            if self.attack_frame == 35:
                self.invincibility_frame = 0
                self.is_invincible = True
                self.invincibility_duration = 2

                self.xspeed = 0
                self.yspeed = 0
                
                self.x = int(self.tp_rect.x - self.hitbox_position[0])
                self.y = int(self.tp_rect.y - self.hitbox_position[1])

                self.image = pygame.image.load(f'animations/Pikachu/up_special/up_b_{self.direction[1]}_{self.direction[0]}.png').convert_alpha()

                self.doing_special = False
                
                if solid_collision(self,(0,1)) == False:
                    self.free_fall = True
                    self.on_wall = False
                    self.apply_gravity = True
                    self.lag = 5
                else:
                    self.lag = 10
                self.freeze_image = False
                self.attack_frame = 0
                self.image_index = 0
        #### NEUTRAL SPECIAL ####
        elif self.special_attack == 'neutral_special':
            if self.attack_frame == 12:
                attacks.add(Electric_Ball(self))

            if self.attack_frame < 30:
                self.yspeed /= 1.04
                self.attack_frame += 1
            else:
                self.doing_special = False
                self.freeze_image = False
                self.attack_frame = 0
                self.image_index = 0
                self.lag = 10
        #### NO ATTACK ####
        else:
            self.doing_special = False
            self.freeze_image = False
            self.attack_frame = 0
            self.image_index = 0