import pygame
from math import exp
from os import listdir
from os.path import isfile, join, splitext
from game.variables import *

################# GAME #################

def commands(player):
    pygame.event.pump()
    keys = pygame.key.get_pressed()

    up = keys[player_key[player]['up']]
    down = keys[player_key[player]['down']]
    right = keys[player_key[player]['right']]
    left = keys[player_key[player]['left']]
    attack = keys[player_key[player]['attack']]
    jump = keys[player_key[player]['jump']]
    shield = keys[player_key[player]['shield']]
    grab = keys[player_key[player]['grab']]
    special = keys[player_key[player]['special']]

    return (right, left, up, down, attack, jump, shield, grab, special)

def get_key(self):
    self.key_right, self.key_left, self.key_up, self.key_down, self.key_attack, self.key_jump, self.key_shield, self.key_grab,self.key_special = commands(self.player)

def update_last_keys(self):
    self.last_key_right, self.last_key_left, self.last_key_up, self.last_key_down, self.last_key_attack, self.last_key_jump, self.last_key_shield, self.last_key_grab,self.last_key_special = (self.key_right, self.key_left, self.key_up, self.key_down, self.key_attack, self.key_jump, self.key_shield, self.key_grab,self.key_special)

def get_pressed_key(self):
    #### right ####
    if self.last_key_right == False and self.key_right:
        self.pressed_key_right = True
    else:
        self.pressed_key_right = False
    
    #### left ####
    if self.last_key_left == False and self.key_left:
        self.pressed_key_left = True
    else:
        self.pressed_key_left = False
    
    #### up ####
    if self.last_key_up == False and self.key_up:
        self.pressed_key_up = True
    else:
        self.pressed_key_up = False
    
    #### down ####
    if self.last_key_down == False and self.key_down:
        self.pressed_key_down = True
    else:
        self.pressed_key_down = False
    
    #### attack ####
    if self.last_key_attack == False and self.key_attack:
        self.pressed_key_attack = True
    else:
        self.pressed_key_attack = False
    
    #### jump ####
    if self.last_key_jump == False and self.key_jump:
        self.pressed_key_jump = True
    else:
        self.pressed_key_jump = False
    
    #### shield ####
    if self.last_key_shield == False and self.key_shield:
        self.pressed_key_shield = True
    else:
        self.pressed_key_shield = False
    
    #### grab ####
    if self.last_key_grab == False and self.key_grab:
        self.pressed_key_grab = True
    else:
        self.pressed_key_grab = False
    
    #### special ####
    if self.last_key_special == False and self.key_special:
        self.pressed_key_special = True
    else:
        self.pressed_key_special = False

def calcul_knockback(base_knockback, percent, weight):
    knockback = base_knockback*(1 + percent/85)
    knockback *= 120/(100 + weight)
    return knockback

def calcul_hitstun(base_hitstun, percent):
    hitstun = int(base_hitstun + global_hitstun*(1-exp(-percent/33)))
    return hitstun

def calcul_di(self):
    if self.key_left:
        self.xspeed -= abs(self.xspeed*0.15)
        if self.xspeed == 0:
            self.xspeed = -1
    if self.key_right:
        self.xspeed += abs(self.xspeed*0.15)
        if self.xspeed == 0:
            self.xspeed = 1
    if self.key_up:
        self.yspeed -= abs(self.yspeed*0.15)
    if self.key_down:
        self.yspeed += abs(self.yspeed*0.15)
    self.xspeed = int(self.xspeed)
    self.yspeed = int(self.yspeed)

def calcul_jump_force(jump_force):
    return global_jump_force*jump_force

def calcul_horizontal_speed(self):
    if self.on_wall:
        speed = global_horizontal_speed*self.running_speed
        if self.is_dashing == True:
            speed *= 1.5
    else:
        speed = global_air_speed*self.air_speed
        if self.is_dashing == True:
            speed *= 1.2
    
    return speed

def calcul_roll_speed(self):
    speed = (1 + self.running_speed/8) * global_roll_speed * exp(-(global_roll_duration - self.roll_frame)/20) 

    if self.is_facing_right == False:
        speed *= -1
    return speed

def calcul_shield_damage(attack):
    return int(0.8*abs(attack.x_eject) + 0.5*abs(attack.y_eject) + 0.5*attack.damage)

def calcul_airdodge_direction(self):
    xspeed = 0
    yspeed = 0

    if self.key_left:
        xspeed = -4
    elif self.key_right:
        xspeed = 4
    if self.key_up:
        yspeed = -5
    elif self.key_down:
        yspeed = 4
    
    if xspeed != 0:
        self.xspeed = xspeed * self.air_speed**0.5
    if yspeed != 0:
        self.yspeed = yspeed * self.air_speed**0.5

def calcul_ledge_invincibility(self):
    return int(global_ledgegrab_invincibility + self.airborne/3)

def calcul_distance(point_1, point_2):
    return ((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**0.5

def check_collision(self, position, collide_object):
    real_x, real_y = get_real_pos(self)
    x_offset = sign(position[0])
    y_offset = sign(position[1])
    rect = pygame.Rect((real_x + x_offset, real_y + y_offset), self.hitbox)

    if type(collide_object).__name__ == 'Wall':
        if rect.colliderect(collide_object.rect):
            return True
    elif type(collide_object).__name__ == 'Platform':
        if rect.colliderect(collide_object.rect) and real_y + self.hitbox[1] == collide_object.y and self.yspeed >= 0:
            return True
    
    return False

def solid_collision(self, position, type='all'):
    collision = False
    if type == 'wall' or type == 'all':
        for wall in walls:
            if check_collision(self, position, wall):
                collision = True
    if type == 'platform' or type == 'all':
        for platform in platforms:
            if check_collision(self, position, platform):
                collision = True
    return collision

def rect_collision(initial_rect, position):
    x_offset = position[0]
    y_offset = position[1]
    rect = pygame.Rect((initial_rect.x + x_offset, initial_rect.y + y_offset), initial_rect.size)
    for wall in walls:
        if type(wall).__name__ == 'Wall':
            if rect.colliderect(wall.rect):
                return True
    return False

def get_real_pos(self):
    real_x = self.x + self.hitbox_position[0]
    real_y = self.y + self.hitbox_position[1]

    if self.is_facing_right == False:
        real_x += hitbox_dependency[self.character]
    
    return real_x, real_y

def get_center_pos(self):
    x, y = get_real_pos(self)
    return (x + self.hitbox[0]/2, y + self.hitbox[1]/2)

def get_attack(self):
    if self.key_attack and self.key_down and self.on_wall == False:
        return 'down_air'
    elif self.key_attack and self.key_up:
        return 'up_tilt'
    elif self.key_special and self.key_up:
        return 'up_special'
    #elif self.key_special and (self.key_right or self.key_left):
    #    return 'side_special'
    elif self.key_special:
        return 'neutral_special'
    elif self.key_grab:
        return 'grab'
    else:
        return 'f_tilt'

def ledge_reset(self):
    self.invincibility_frame = 0
    self.is_invincible = True
    self.invincibility_duration = global_ledgejump_invincibility
    self.lag = 1
    self.apply_gravity = True
    self.freeze_image = False
    self.walljump = True
    self.free_fall = False
    self.jump_left = self.max_jumps - 1
    self.ledge.timer = global_frames_between_2_ledge_grabs
    self.grabbing_ledge = False

def ledge_neutral_getup(self):
    real_x, real_y = get_real_pos(self)

    if real_y > self.ledge.y - self.hitbox[1]:
        self.y -= int((self.hitbox[1] + global_ledge_hitbox[1])/10)
    else:
        if self.ledge.direction == 'right' and real_x > self.ledge.x - self.hitbox[0]:
            self.x -= int(self.hitbox[0]/10)
        
        elif self.ledge.direction == 'left' and real_x < self.ledge.x + global_ledge_hitbox[0]:
            self.x += int(self.hitbox[0]/10)
        
        else:
            self.neutral_getup = False

            ledge_reset(self)

def ledgeroll(self):
    real_x, real_y = get_real_pos(self)

    if real_y > self.ledge.y - self.hitbox[1]:
        self.y -= int((self.hitbox[1] + global_ledge_hitbox[1])/5)
    else:

        if self.ledge.direction == 'right' and real_x > self.ledge.x - self.hitbox[0] - 80:
            self.x -= 5
        
        elif self.ledge.direction == 'left' and real_x < self.ledge.x + global_ledge_hitbox[0] + 80:
            self.x += 5
        
        else:
            self.ledgeroll = False

            ledge_reset(self)

def get_triangle(self):
    x_pos, y_pos = get_real_pos(self)
    x_pos += self.hitbox[0]/2
    y_pos += self.hitbox[1]/2

    direction = ['', '']

    if self.key_left:
        x_pos -= self.hitbox[0]/2 + 12
        direction[0] = 'left'
    elif self.key_right:
        x_pos += self.hitbox[0]/2 + 12
        direction[0] = 'right'
    
    if self.key_up:
        y_pos -= self.hitbox[1]/2 + 4
        direction[1] = 'up'
    elif self.key_down:
        y_pos += self.hitbox[1]/2 + 4
        direction[1] = 'down'
    
    if direction == ['left','up']:
        return [(x_pos - 4, y_pos + 4), (x_pos + 4, y_pos - 4), (x_pos - 8, y_pos - 8)]
    elif direction == ['right','up']:
        return [(x_pos - 4, y_pos - 4), (x_pos + 4, y_pos + 4), (x_pos + 8, y_pos - 8)]
    if direction == ['left','down']:
        return [(x_pos - 4, y_pos - 4), (x_pos + 4, y_pos + 4), (x_pos - 8, y_pos + 8)]
    if direction == ['right','down']:
        return [(x_pos - 4, y_pos + 4), (x_pos + 4, y_pos - 4), (x_pos + 8, y_pos + 8)]
    elif direction == ['left','']:
        return [(x_pos, y_pos - 4), (x_pos, y_pos + 4), (x_pos - 8, y_pos)]
    elif direction == ['right','']:
        return [(x_pos, y_pos - 4), (x_pos, y_pos + 4), (x_pos + 8, y_pos)]
    elif direction == ['','up']:
        return [(x_pos - 4, y_pos), (x_pos + 4, y_pos), (x_pos, y_pos - 8)]
    elif direction == ['','down']:
        return [(x_pos - 4, y_pos), (x_pos + 4, y_pos), (x_pos, y_pos + 8)]
    else:
        return [(x_pos, y_pos), (x_pos, y_pos), (x_pos, y_pos)]

def check_tp_wall(self, direction):
    tp_pos = [self.tp_rect.x + self.tp_rect.size[0]/2, self.tp_rect.y + self.tp_rect.size[1]/2]          
    center = get_center_pos(self)
    
    if direction == 'left':
        if center[0] - tp_pos[0] < 100:
            return True
        else:
            return False
    elif direction == 'right':
        if tp_pos[0] - center[0] < 100:
            return True
        else:
            return False
    
    elif direction == 'up':
        if center[1] - tp_pos[1] < 100:
            return True
        else:
            return False
    elif direction == 'down':
        if center[1] - tp_pos[1] > -100:
            return True
        else:
            return False
    return True

def respawn(self):
        self.x = int(window_size[0]/2 - self.hitbox_position[0] - self.hitbox[0]/2)
        self.y = 48 + int(window_size[1]/11 - self.hitbox_position[1] - self.hitbox[1]/2)
        self.xspeed = 0
        self.yspeed = 0
        self.percent = 0
        self.is_dashing = False
        self.is_attacking = False
        self.special_attack = ''
        self.doing_special = False
        self.freefall = False
        self.freeze_image = False
        self.on_wall = False
        self.hitstun = 0
        self.airborne = 0
        self.jump_left = self.max_jumps - 1
        self.invincibility_duration = global_respawn_invincibility_time
        self.invincibility_frame = 0
        self.is_invincible = True
        self.lag = 10

################# SCREEN AND IMAGES #################

def best_ratio(new_res):
    
    h = new_res[1]
    w = int(h*960/544)
    while w > new_res[0]:
        h -= 1
        w -= 1
    res_1 = (w,h)

    w = new_res[0]
    h = int(w*544/960)
    while h > new_res[1]:
        w -= 1
        h -= 1
    res_2 = (w,h)

    if res_2[1] > res_1[1]:
        return res_2
    else:
        return res_1

def add_images_from_dir(images_list, image_path):
    images =  [file for file in listdir(image_path) if isfile(join(image_path, file)) and file.endswith('png')]
    for filename in images:
        images_list[splitext(filename)[0]] = pygame.image.load(
        join(image_path, filename))

def add_path(images_list, image_path):
    for path in image_path:
        if path not in images_list['load_path']:
            add_images_from_dir(images_list, path)
            images_list['load_path'].add(path)

def cursor_width(xscale,yscale):
    if xscale >= 1 and yscale >= 1:
        width = int(8*(1 + ((xscale - 1)**2+(yscale - 1)**2)**(0.5)))
    else:
        width = int(8*((xscale)**2+(yscale)**2)**(0.5))
    return width

################# MISCELLANEOUS #################

def add(liste1,liste2):
    res = []
    for i in range(len(liste1)):
        res.append(liste1[i]+liste2[i])
    return res

def true_floor(number):
    return int(abs(number))

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0