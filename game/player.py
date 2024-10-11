import pygame
from pygame.locals import *
from math import cos

try:
    from game.variables import *
    from game.functions import *
    from game.animation import *
    from game.attack import *
    from game.cloud import *
    from game.special import *
except ImportError:
    from variables import *
    from functions import *
    from animation import *
    from attack import *
    from cloud import *
    from special import *


class Player(pygame.sprite.Sprite):
    def __init__(self, coordinates, player, character):
        super().__init__()
        self.x, self.y = coordinates

        self.xspeed = 0
        self.yspeed = 0

        #### Keys manager ####
        self.key_right, self.key_left, self.key_up, self.key_down, self.key_attack, self.key_jump, self.key_shield, self.key_grab, self.key_special = (
            False, False, False, False, False, False, False, False, False)
        self.last_key_right, self.last_key_left, self.last_key_up, self.last_key_down, self.last_key_attack, self.last_key_jump, self.last_key_shield, self.last_key_grab, self.last_key_special = (
            False, False, False, False, False, False, False, False, False)
        self.pressed_key_right, self.pressed_key_left, self.pressed_key_up, self.pressed_key_down, self.pressed_key_attack, self.pressed_key_jump, self.pressed_key_shield, self.pressed_key_grab, self.pressed_key_special = (
            False, False, False, False, False, False, False, False, False)

        #### Character parameters ####

        self.player = player
        self.character = character
        if self.player == 1:
            self.is_facing_right = True
        else:
            self.is_facing_right = False
        self.weight = weights[character]
        self.jump_force = jump_forces[character]
        self.running_speed = running_speeds[character]
        self.air_speed = air_speeds[character]
        self.falling_speed, self.max_falling_speed, self.fast_falling_speed = falling_parameters[
            character]
        self.max_jumps = jumps[character]  # Number of jumps
        self.jump_left = self.max_jumps

        self.stock = global_stock_number
        self.stock_image = pygame.image.load(
            f'sprites/stocks/stock_{character}.png')

        if self.character != 'The_Cube':
            self.hitbox = image_var[character]['hitbox']
            self.hitbox_position = image_var[character]['offset']
            self.x_hitbox, self.y_hitbox = tuple(
                add([self.x, self.y], self.hitbox_position))
            self.bottom = (
                self.x + self.hitbox_position[0], self.y + self.hitbox_position[1] + self.hitbox[1])
            self.rect = pygame.Rect(get_real_pos(self), self.hitbox)
        else:
            self.hitbox = (32, 32)
            self.hitbox_position = [0, 0]

        self.shield_max_size = self.hitbox[0] + self.hitbox[1]
        image_shield = pygame.image.load(f'sprites/miscellaneous/shield{player}.png')
        self.image_shield = pygame.transform.scale(
            image_shield, (self.shield_max_size, self.shield_max_size))
        self.shield_size = self.shield_max_size
        self.is_shielding = False

        #### Movement ####
        self.can_act = True  # Doing any actions
        self.can_move = True
        self.on_wall = False
        self.lag = 0
        self.walljump = True
        self.airborne = 0  # Number of frame in the air; = 0 if on a wall
        self.apply_gravity = True
        self.is_dashing = False
        self.dash_direction = ''
        self.dash_index = 0  # Timer for pressing the same direction
        self.is_rolling = False
        self.is_airdodging = False
        self.roll_frame = 0
        self.landing_dust = False
        self.jumping_dust = False
        self.free_fall = False
        self.grabbing_ledge = False
        self.neutral_getup = False
        self.ledgeroll = False
        self.ledge = ''

        #### Attack and hit ####
        self.percent = 0
        self.is_attacking = False
        self.attack_frame = 0
        self.startup = 0
        self.active_frames = 0
        self.end_lag = 0
        self.immune_to_attack = ('', 0)
        self.next_hit = 0
        self.hitstun = 0
        self.startup_frame = 0

        self.invincibility_frame = 0
        self.invincibility_duration = 0
        self.is_invincible = False

        self.is_grabbing = False
        self.grabbed = (False, '')
        self.grab_player = (False, '')
        self.grab_frame = 0
        self.launched = False

        self.special_attack = ''
        self.doing_special = False

        #### Image ####
        self.image_draw = True
        self.freeze_image = False
        self.dust_frame_index = 0

        self.animations = {}
        import_character_assets(self)
        self.image_index = 0
        self.animation_speed = 0.2
        self.image_strip = ''

        if character != 'The_Cube':
            self.image = self.animations['fall'][0]
        else:
            self.image = pygame.image.load('sprites/miscellaneous/player.png')

        #### Offscreen image ####
        self.cursor = pygame.image.load(
            f'sprites/miscellaneous/offscreen_cursor{player}.png').convert_alpha()
        self.draw_cursor = False
        self.x_cursor, self.y_cursor = (0, 0)

        #### Coordinates ####
        self.x = coordinates[0] - self.hitbox_position[0]
        self.y = coordinates[1] - self.hitbox_position[1]

    def movement(self):
        ###### FAST FALL ######
        if self.can_act and self.free_fall == False and self.is_airdodging == False and self.is_attacking == False and self.doing_special == False and self.airborne > int(self.fast_falling_speed) and self.key_down and 0 < self.yspeed < self.fast_falling_speed:
            self.yspeed = self.fast_falling_speed
            self.apply_gravity == False

        ###### JUMP ######
        if self.can_act and self.is_airdodging == False and self.is_attacking == False and self.doing_special == False and self.free_fall == False and self.pressed_key_jump and self.jump_left > 0:
            self.jump_left -= 1
            self.jumping_dust = True
            self.yspeed = calcul_jump_force(self.jump_force)
            if self.on_wall:
                self.y -= 1
                self.dash_index = 0
                self.on_wall = False
            self.apply_gravity = True

        ###### HORIZONTAL MOVEMENT ######
        if self.can_act:
            if self.hitstun == 0:  # Check if xpseed is too big
                if self.xspeed < -calcul_horizontal_speed(self):
                    self.xspeed = -calcul_horizontal_speed(self)
                if self.xspeed > calcul_horizontal_speed(self):
                    self.xspeed = calcul_horizontal_speed(self)

            if self.key_right:
                if self.on_wall:
                    if self.xspeed < calcul_horizontal_speed(self):
                        self.xspeed += self.running_speed*0.8
                    else:
                        self.xspeed = calcul_horizontal_speed(self)
                elif self.xspeed < calcul_horizontal_speed(self):
                    self.xspeed += self.air_speed*0.5
                else:
                    self.xspeed = calcul_horizontal_speed(self)

            elif self.key_left:
                if self.on_wall:
                    if self.xspeed > -calcul_horizontal_speed(self):
                        self.xspeed -= self.running_speed*0.8
                    else:
                        self.xspeed = -calcul_horizontal_speed(self)
                elif self.xspeed > -calcul_horizontal_speed(self):
                    self.xspeed -= self.air_speed*0.5
                else:
                    self.xspeed = -calcul_horizontal_speed(self)

    def slide(self):
        if self.is_attacking or self.is_grabbing or self.doing_special:
            if self.on_wall:
                self.xspeed /= 2.3
            else:
                self.xspeed /= 1.3
            if (0 < self.xspeed < 1 and self.key_right) or (-1 < self.xspeed < 0 and self.key_left):
                self.xspeed = sign(self.xspeed)
            elif abs(self.xspeed) < 1:
                self.xspeed = 0
        elif self.hitstun == 0:
            if self.lag > 0 or (self.lag == 0 and self.key_left == False and self.key_right == False):
                if abs(self.xspeed) >= 1:
                    self.xspeed /= 1.22
                else:
                    self.xspeed = 0

    def gravity(self):
        if self.apply_gravity:
            self.yspeed += self.falling_speed
            if self.yspeed > self.max_falling_speed and self.hitstun == 0:
                self.yspeed = self.max_falling_speed

    def dash(self):
        if self.is_dashing == False:
            if self.dash_index > 0:
                if (self.key_right and self.dash_direction == 'right') or (self.key_left and self.dash_direction == 'left'):
                    self.dash_index += 1
                    if self.dash_index > global_dash_window:
                        self.dash_index = global_dash_window
                else:
                    self.dash_index -= 1

                if (self.pressed_key_right and self.dash_direction == 'right') or (self.pressed_key_left and self.dash_direction == 'left') and self.dash_index < global_dash_window:
                    self.is_dashing = True
                    self.dash_index = global_dash_window

            if self.pressed_key_left and (self.dash_index == 0 or self.dash_direction == 'right'):
                self.dash_index = 1
                self.dash_direction = 'left'
            elif self.pressed_key_right and (self.dash_index == 0 or self.dash_direction == 'left'):
                self.dash_index = 1
                self.dash_direction = 'right'

        else:
            if (self.key_right == False and self.dash_direction == 'right') or (self.key_left == False and self.dash_direction == 'left'):
                self.dash_index -= 1
            else:
                self.dash_index = int(global_dash_window/2)

            if self.pressed_key_left and self.dash_direction == 'right' and self.dash_index <= global_dash_window:
                self.dash_direction = 'left'
                self.dash_index = int(global_dash_window/2)
            elif self.pressed_key_right and self.dash_direction == 'left' and self.dash_index <= global_dash_window:
                self.dash_direction = 'right'
                self.dash_index = int(global_dash_window/2)

            if self.dash_index == 0:
                self.is_dashing = False

    def still_on_wall(self):
        if self.on_wall:
            if solid_collision(self, (0, 1)) == False:
                self.jump_left = self.max_jumps - 1
                self.on_wall = False
                self.apply_gravity = True

        elif solid_collision(self, (0, 1)):
            self.on_wall = True
            self.lag = global_fall_landing_lag
            self.jump_left = self.max_jumps
            self.apply_gravity = False
            self.yspeed = 0
            self.walljump = True
            self.free_fall = False

    def get_off_platform(self):
        if self.key_down and self.on_wall and self.can_act and self.is_attacking == False:
            # Check if there are only collisions with platforms
            if solid_collision(self, (0, 1), 'platform') and solid_collision(self, (0, 1), 'wall') == False:
                self.on_wall = False
                self.apply_gravity = True
                self.y += 1
                self.lag = 5
                self.jump_left = self.max_jumps - 1

    def check_walljump(self):
        if self.can_act and self.pressed_key_left and solid_collision(self, (1, 0)) and self.on_wall == False and self.walljump and self.is_attacking == False and self.doing_special == False and self.free_fall == False and self.lag == 0:
            self.yspeed = calcul_jump_force(self.jump_force)*0.9
            self.xspeed = -2.5*self.air_speed
            self.x -= 1
            self.walljump = False
            if self.jump_left == 0:
                self.jump_left = 1

        if self.can_act and self.pressed_key_right and solid_collision(self, (-1, 0)) and self.on_wall == False and self.walljump and self.is_attacking == False and self.doing_special == False and self.free_fall == False and self.lag == 0:
            self.yspeed = calcul_jump_force(self.jump_force)*0.9
            self.xspeed = 2.5*self.air_speed
            self.x += 1
            self.walljump = False
            if self.jump_left == 0:
                self.jump_left = 1

    def update_position(self):
        self.x_hitbox, self.y_hitbox = tuple(
            add([self.x, self.y], self.hitbox_position))

        for _ in range(true_floor(self.xspeed)):
            if solid_collision(self, (sign(self.xspeed), 0)) == False:
                self.x += sign(self.xspeed)
            else:
                if self.hitstun > 1:  # Bounce when hit
                    self.xspeed *= -0.2
                else:
                    self.xspeed = 0
                self.is_dashing = False
                break

        for _ in range(true_floor(self.yspeed)):
            if (solid_collision(self, (0, 1)) == False and sign(self.yspeed) == 1) or (solid_collision(self, (0, -1)) == False and sign(self.yspeed) == -1):
                self.y += sign(self.yspeed)
            else:
                self.is_dashing = False
                if solid_collision(self, (0, 1)):  # Wall under the player - Landing
                    self.on_wall = True
                    self.landing_dust = True
                    self.lag = global_fall_landing_lag
                    self.apply_gravity = False
                    self.walljump = True
                    self.jump_left = self.max_jumps
                    if self.hitstun > 1:  # Bounce when hit
                        self.yspeed *= -0.2
                    else:
                        self.yspeed = 0
                    if self.xspeed != 0 and self.hitstun == 0:
                        self.dash_index = 1
                    if self.is_attacking:  # Stop horizontal movement when attacking and then landing
                        self.xspeed = 0
                if solid_collision(self, (0, -1)):  # Wall above
                    self.yspeed = 0
                break

    def update_airborne(self):
        if self.on_wall == False and self.grabbing_ledge == False and self.hitstun == 0:
            if self.airborne < 180:
                self.airborne += 1
        else:
            self.airborne = 0

    def check_attack(self):
        if self.pressed_key_attack and self.can_act and self.free_fall == False and self.is_attacking == False and self.is_shielding == False and self.doing_special == False and self.grabbing_ledge == False and self.is_grabbing == False and self.is_airdodging == False:
            self.is_attacking = True
            self.is_shielding = False
            self.is_dashing = False
            self.freeze_image = True
            attack_name = get_attack(self)
            self.image_strip = attack_name
            self.image_index = 0
            self.attack_frame = 0

            var = attack_list[self.character][attack_name]
            self.startup, self.active_frames, self.end_lag = (
                var[3], var[4], var[5])
            attacks.add(Attack(var[0], var[1], var[2], var[3],
                        var[4], var[6], var[7], self, attack_name, var[8]))
            self.startup_frame = var[9]

        if self.is_attacking:
            if self.attack_frame == self.startup + self.active_frames + self.end_lag:
                self.is_attacking = False
                self.freeze_image = False
                self.attack_frame = 0
                self.image_index = 0
            else:
                self.attack_frame += 1
                if self.attack_frame == self.startup + self.active_frames:
                    self.lag = self.end_lag

    def check_special(self):
        if self.pressed_key_special and self.can_act and self.free_fall == False and self.is_attacking == False and self.is_shielding == False and self.doing_special == False and self.grabbing_ledge == False and self.is_grabbing == False and self.is_airdodging == False and self.lag == 0:
            self.doing_special = True
            self.is_shielding = False
            self.is_dashing = False
            self.freeze_image = True
            self.special_attack = get_attack(self)
            self.image_strip = self.special_attack
            self.image_index = 0
            self.attack_frame = 0

            special_initialization(self)

        if self.doing_special == True:
            special(self)

    def update_variables(self):
        can_act_hitstun = False
        can_act_lag = False
        can_act_roll = False
        can_act_grab = False
        can_act_airdodge = False

        if self.is_attacking == False and self.is_grabbing == False and self.doing_special == False:
            if (self.xspeed > 0 and self.on_wall) or (self.xspeed > 0 and abs(self.xspeed) == calcul_horizontal_speed(self) and self.on_wall == False):
                self.is_facing_right = True
            elif (self.xspeed < 0 and self.on_wall) or (self.xspeed < 0 and abs(self.xspeed) == calcul_horizontal_speed(self) and self.on_wall == False):
                self.is_facing_right = False

        if self.hitstun > 1:
            self.hitstun -= 1
            self.can_act = False
            if self.on_wall:
                self.xspeed = 0
        elif (self.on_wall and self.hitstun == 1) or (self.key_left or self.key_right or self.key_down or self.key_up or self.key_jump or self.key_grab or self.key_special or self.key_shield):
            self.hitstun = 0

        if self.hitstun <= 1:
            can_act_hitstun = True

        if self.launched and self.hitstun <= 1:
            self.grabbed = (False, '')
            self.launched = False

        if self.free_fall and self.on_wall:
            self.free_fall = False

        if self.next_hit > 0:
            self.next_hit -= 1

        if self.lag > 0:
            self.can_act = False
            self.lag -= 1
        else:
            can_act_lag = True

        can_act_grab = not (self.grabbed[0] or self.is_grabbing)

        can_act_roll = not self.is_rolling
        can_act_airdodge = not self.is_airdodging

        if can_act_lag and can_act_hitstun and can_act_roll and can_act_grab and can_act_airdodge:
            self.can_act = True

    def check_hit_and_grab(self):
        for attack in attacks:
            if (type(attack).__name__ == 'Attack' or type(attack).__name__ == 'Electric_Ball') and (self.immune_to_attack != (attack.name, attack.player.player) or self.immune_to_attack == (attack.name, attack.player.player) and self.next_hit == 0) and self.player != attack.player.player and pygame.Rect(get_real_pos(self), self.hitbox).colliderect(attack.rect):
                if self.is_shielding:
                    self.immune_to_attack = (attack.name, attack.player.player)
                    self.next_hit = 15
                    self.shield_size -= calcul_shield_damage(attack)
                    if self.shield_size < 0:
                        self.shield_size = 0
                    if self.shield_size > self.shield_max_size/3:
                        attack.sound_move.stop()
                        pygame.mixer.Sound(
                            'sounds/sfx/sound_shield_hit.ogg').play()
                    else:
                        attack.kill()

                elif self.is_invincible == False:
                    self.is_attacking = False
                    self.attack_frame = 0

                    self.can_act = False
                    self.is_dashing = False
                    self.dash_index = 0
                    self.freeze_image = False
                    self.doing_special = False
                    self.free_fall = False
                    self.hitstun = calcul_hitstun(attack.hitstun, self.percent)
                    self.xspeed = calcul_knockback(
                        attack.x_eject, self.percent, self.weight)
                    self.yspeed = calcul_knockback(
                        attack.y_eject, self.percent, self.weight)
                    if abs(self.xspeed) < 1:
                        self.xspeed = sign(self.xspeed)
                    if abs(self.yspeed) < 1:
                        self.yspeed = sign(self.yspeed)

                    if self.on_wall and self.yspeed < 0:
                        self.y -= 1
                        self.on_wall = False
                        self.jump_left = self.max_jumps - 1
                        self.apply_gravity = True

                    if self.grabbing_ledge:
                        self.grabbing_ledge = False
                        self.apply_gravity = True
                        self.ledge.timer = global_frames_between_2_ledge_grabs

                    calcul_di(self)
                    self.percent += attack.damage
                    self.immune_to_attack = (attack.name, attack.player.player)
                    self.next_hit = 15
                    attack.sound_hit.play()
                    attack.kill()
                break
            elif type(attack).__name__ == 'Grab' and self.player != attack.player.player and pygame.Rect(get_real_pos(self), self.hitbox).colliderect(attack.rect) and self.grabbed[0] == False and self.is_invincible == False:
                other = attack.player

                self.grabbed = (True, other)
                self.can_act = False
                self.apply_gravity = False
                self.xspeed = 0

                other.grab_player = (True, self)
                other.can_act = False
                other.xspeed = 0
                other.lag = global_grab_lag
                pygame.mixer.Sound('sounds/sfx/sound_slap_m.ogg').play()

    def check_shield(self):
        if self.key_shield and self.on_wall and self.can_act and self.is_shielding == False and self.is_attacking == False and self.grabbing_ledge == False and self.doing_special == False:
            self.is_shielding = True
        if self.is_shielding and self.key_shield == False:
            self.lag = 10
            self.is_shielding = False

        if self.is_shielding:
            self.xspeed = 0
            self.shield_size -= 0.2
            if self.shield_size < self.shield_max_size/3:
                pygame.mixer.Sound(
                    'sounds/sfx/sound_shield_break.ogg').play()
                self.shield_size = self.shield_max_size
                self.hitstun = 120
                self.yspeed = -6
                self.is_shielding = False
        else:
            if self.shield_size < self.shield_max_size:
                self.shield_size += 0.25
            else:
                self.shield_size = self.shield_max_size

    def buffer(self):
        if self.lag > 0:
            self.pressed_key_jump = self.key_jump

            self.pressed_key_grab = self.key_grab

            self.pressed_key_special = self.key_special

    def check_roll(self):
        if (self.key_right or self.key_left) and self.is_shielding:
            self.is_rolling = True
            self.is_shielding = False
            self.can_act = False

            self.invincibility_duration = global_roll_duration
            self.invincibility_frame = 0
            self.is_invincible = True

            if self.key_right:
                self.is_facing_right = True
            elif self.key_left:
                self.is_facing_right = False
            self.roll_frame = global_roll_duration

        if self.is_rolling:
            if self.roll_frame > 0:
                self.xspeed = calcul_roll_speed(self)
                self.roll_frame -= 1
            else:
                self.is_rolling = False
                self.can_act = True
                self.xspeed = 0
                self.lag = global_roll_endlag

    def invincible_update(self):
        if self.invincibility_frame < self.invincibility_duration:

            if cos((2+self.invincibility_frame/8)**2) > 0:
                self.image_draw = False
            else:
                self.image_draw = True
            self.invincibility_frame += 1

        elif self.invincibility_frame > 0:
            self.invincibility_frame = 0
            self.invincibility_duration = 0
            self.is_invincible = False
            self.image_draw = True

    def check_grab(self):
        if self.grabbed[0] and self.launched == False:
            other = self.grabbed[1]
            other_y = get_real_pos(other)[1]
            self.y = other_y + other.hitbox[1] - \
                self.hitbox[1] - self.hitbox_position[1]

        if self.grab_player[0] and self.lag == 0:
            if self.key_left or self.key_right or self.key_up:
                if self.key_left or self.key_right:
                    throw = 'f_throw'
                elif self.key_up:
                    throw = 'up_throw'

                pygame.mixer.Sound('sounds/sfx/sound_launched_m.ogg').play()

                other = self.grab_player[1]
                (xspeed,
                 yspeed), hitstun, damage = attack_list[self.character][throw]

                self.grab_player = (False, '')
                self.grab_frame = self.startup + self.active_frames

                other.y -= 1
                other.on_wall = False
                other.jump_left = other.max_jumps - 1
                other.apply_gravity = True
                other.xspeed = calcul_knockback(
                    xspeed, other.percent, other.weight)
                if self.pressed_key_left:
                    other.xspeed *= -1
                other.yspeed = calcul_knockback(
                    yspeed, other.percent, other.weight)
                other.hitstun = calcul_hitstun(hitstun, other.percent)
                other.percent += damage
                other.launched = True
                calcul_di(other)

        if self.pressed_key_grab and self.can_act and self.free_fall == False and self.is_attacking == False and self.is_grabbing == False and self.grabbing_ledge == False and self.is_shielding == False and self.doing_special == False:
            self.is_shielding = False
            self.is_grabbing = True
            self.is_dashing = False
            self.freeze_image = True

            self.image_strip = 'grab'
            self.grab_frame = 0
            var = attack_list[self.character]['grab']
            self.startup, self.active_frames, self.end_lag = (
                var[2], var[3], var[4])
            attacks.add(Grab(var[0], var[1], var[2], var[3], self))

        if self.is_grabbing:
            if self.grab_frame == self.startup + self.active_frames + self.end_lag:
                self.is_grabbing = False
                self.freeze_image = False
                self.grab_frame = 0
                self.image_index = 0
            elif self.grab_player[0] == False:
                self.grab_frame += 1
                if self.grab_frame == self.startup + self.active_frames:
                    self.lag = self.end_lag

    def check_airdodge(self):
        if self.pressed_key_shield and self.on_wall == False and self.can_act and self.free_fall == False and self.is_attacking == False and self.is_shielding == False and self.doing_special == False and self.is_airdodging == False and self.grabbing_ledge == False:
            self.is_airdodging = True

            self.invincibility_duration = int(
                global_airdodge_inv_time + 5 * (self.air_speed)**0.5)
            self.invincibility_frame = 0
            self.is_invincible = True

            calcul_airdodge_direction(self)

        if self.is_airdodging:
            if self.invincibility_frame == self.invincibility_duration or self.on_wall:
                self.is_airdodging = False
                self.freeze_image = False
                self.invincibility_frame = self.invincibility_duration
                self.lag = global_airdodge_endlag

                if self.on_wall:
                    self.lag = int(global_airdodge_landing_lag /
                                   (1 + 0.2*abs(self.yspeed) + 0.2*abs(self.xspeed)))
                    self.jump_left = self.max_jumps
                    self.apply_gravity = False
                    self.yspeed = 0
                    self.walljump = True
                    self.free_fall = False

    def check_ledge(self):
        #### GRAB LEDGE ####
        if self.grabbing_ledge == False and self.is_attacking == False and self.is_airdodging == False and self.is_rolling == False and self.is_grabbing == False and self.hitstun <= 1:
            rect = pygame.Rect(get_real_pos(self), self.hitbox)
            if self.grabbing_ledge == False:
                for ledge in ledges:
                    if rect.colliderect(ledge.rect) and rect.top > ledge.y and ledge.is_available:
                        ledge.is_available = False
                        ledge.player = self.player

                        if ledge.direction == 'left':
                            self.is_facing_right = True
                        elif ledge.direction == 'right':
                            self.is_facing_right = False

                        self.grabbing_ledge = True
                        self.ledge = ledge
                        self.apply_gravity = False

                        if self.is_facing_right:
                            self.x = ledge.x + \
                                global_ledge_hitbox[0] - \
                                self.hitbox[0] - self.hitbox_position[0]
                        else:
                            self.x = ledge.x - \
                                hitbox_dependency[self.character] - \
                                self.hitbox_position[0]
                        self.y = ledge.y + \
                            global_ledge_hitbox[1] - self.hitbox_position[1]

                        self.xspeed = 0
                        self.yspeed = 0

                        self.lag = global_ledgegrab_lag
                        self.image_strip = 'ledgegrab'
                        self.freeze_image = True
                        self.doing_special = False
                        self.special_attack = ''
                        self.attack_frame = 0

                        self.invincibility_frame = 0
                        self.is_invincible = True
                        self.invincibility_duration = calcul_ledge_invincibility(
                            self)

        if self.grabbing_ledge and self.lag == 0 and self.neutral_getup == False and self.ledgeroll == False:
            #### LEDGEJUMP ####
            if self.pressed_key_jump or self.pressed_key_up:
                ledge_reset(self)

                self.jumping_dust = True
                self.yspeed = 1.2*calcul_jump_force(self.jump_force)

            #### LEDGEDROP DOWN ####
            elif self.pressed_key_down:
                ledge_reset(self)

            #### LEDGEDROP SIDE ####
            elif (self.pressed_key_right and self.ledge.direction == 'right') or (self.pressed_key_left and self.ledge.direction == 'left'):
                ledge_reset(self)

                self.xspeed = 2.5*self.air_speed
                if self.ledge.direction == 'left':
                    self.xspeed *= -1
                    self.x -= 1
                else:
                    self.x += 1

            #### NEUTRAL GETUP ####
            elif (self.pressed_key_right and self.ledge.direction == 'left') or (self.pressed_key_left and self.ledge.direction == 'right'):
                self.neutral_getup = True

            #### LEDGEROLL ####
            elif self.pressed_key_shield:
                self.ledgeroll = True

        if self.neutral_getup:
            self.image_strip = 'fall'

            self.invincibility_frame = 0
            self.is_invincible = True
            self.invincibility_duration = global_neutral_getup_invincibility

            ledge_neutral_getup(self)

        if self.ledgeroll:
            self.image_strip = 'roll'

            self.invincibility_frame = 0
            self.is_invincible = True
            self.invincibility_duration = global_ledgeroll_invincibility

            ledgeroll(self)

    def cloud(self):
        if self.hitstun > 0:
            if self.hitstun % 3 == 0 and self.on_wall == False:
                clouds.add(Cloud(self))

    def offscreen_cursor(self):
        real_x, real_y = get_real_pos(self)

        if real_x + self.hitbox[0] < -16:
            self.draw_cursor = True
            self.x_cursor, self.y_cursor = (0, real_y)

        elif real_x > window_size[0] + 16:
            self.draw_cursor = True
            self.x_cursor, self.y_cursor = (
                window_size[0] - self.cursor.get_width(), real_y)

        elif real_y > window_size[1] + 16:
            self.draw_cursor = True
            self.x_cursor, self.y_cursor = (
                real_x - self.cursor.get_width()/2 + self.hitbox[0]/2, window_size[1] - self.cursor.get_height())

        elif real_y + self.hitbox[1] < -16:
            self.draw_cursor = True
            self.x_cursor, self.y_cursor = (
                real_x - self.cursor.get_width()/2 + self.hitbox[0]/2, 0)

        else:
            self.draw_cursor = False

        if self.draw_cursor:
            if self.x_cursor - self.cursor.get_width() > window_size[0]:
                self.x_cursor = window_size[0] + self.cursor.get_width()
            if self.x_cursor < 0:
                self.x_cursor = 0
            if self.y_cursor < 0:
                self.y_cursor = 0
            if self.y_cursor + self.cursor.get_height() > window_size[1]:
                self.y_cursor = window_size[1] - self.cursor.get_height()

            ratio = 32/self.hitbox[1]
            image_cursor = pygame.transform.scale(
                self.image, (self.image.get_width()*ratio, self.image.get_height()*ratio))
            image_cursor_x = self.x_cursor + self.cursor.get_width()/2 - \
                image_cursor.get_width()/2
            image_cursor_y = self.y_cursor + self.cursor.get_height()/2 - \
                image_cursor.get_height()/2
            image_position = (image_cursor_x, image_cursor_y)

            screen.blit(image_cursor, image_position)
            screen.blit(self.cursor, (self.x_cursor, self.y_cursor))

    def draw(self):
        if self.image_draw:
            screen.blit(self.image, (self.x, self.y))

        if self.is_shielding and self.is_rolling == False:
            scale = self.shield_size/self.shield_max_size
            shield = pygame.transform.scale(self.image_shield, (self.image_shield.get_width(
            )*scale, self.image_shield.get_height()*scale))
            screen.blit(shield, (self.x_hitbox+self.hitbox[0]/2 - shield.get_width(
            )/2, self.y_hitbox+self.hitbox[1]/2 - shield.get_height()/2))

        if show_hitbox >= 2:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(
                get_real_pos(self), self.hitbox))

    def update(self):
        update_last_keys(self)
        get_key(self)
        get_pressed_key(self)
        self.buffer()
        self.update_variables()

        if self.on_wall:
            self.dash()
        self.check_shield()
        self.check_roll()
        self.check_airdodge()
        self.check_ledge()
        self.invincible_update()

        if self.hitstun <= 1 and self.is_shielding == False and self.lag == 0 and self.grabbed[0] == False and self.grabbing_ledge == False:
            self.movement()

        if self.is_rolling == False and self.grabbing_ledge == False:
            self.slide()
            self.check_walljump()

        self.get_off_platform()
        self.gravity()
        if self.grabbed[0] == False and self.doing_special == False:
            self.still_on_wall()

        self.check_attack()
        self.check_special()
        self.check_grab()
        self.check_hit_and_grab()
        self.cloud()

        self.update_airborne()
        self.update_position()

        create_jump_particles(self)
        create_landing_dust(self)
        run_dust_animation(self)
        for particle in dust_sprites:
            particle.update(2)
            draw(particle)

        if self.character != 'The_Cube':
            animate(self)

        self.draw()
        self.offscreen_cursor()
