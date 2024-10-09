import pygame
from pygame.locals import *
from os import walk

try:
    from game.functions import *
    from game.variables import *
except ImportError:
    from functions import *
    from variables import *

###################### ANIMATION ######################

def get_player_state(self, previous_state):
    if self.freeze_image == False:
        if self.hitstun > 0:
            return 'hit'
        if self.is_airdodging:
            return 'airdodge'
        if self.is_rolling:
            return 'roll'
        elif self.is_shielding:
            return 'shield'
        elif self.is_attacking:
            if self.key_down:
                return 'down_air'
        else:
            if self.on_wall:
                if self.xspeed != 0:
                    if self.is_dashing:
                        return 'dash'
                    else:
                        return 'walk'
            else:
                if self.yspeed < 0:
                    return 'jump'
                else:
                    return 'fall'
        return 'idle'
    else:
        return previous_state

def animate(self):
    new_image_strip = get_player_state(self, self.image_strip)
    if new_image_strip != self.image_strip:
        self.image_index = 0
    self.image_strip =  new_image_strip
    self.animation = self.animations[self.image_strip]

    if self.is_attacking == False and self.doing_special == False:
        if self.image_index < len(self.animation) - 1:
            self.image_index += self.animation_speed
        else:
            self.image_index = 0
    else:
        if self.attack_frame < self.startup:
            if self.image_index < self.startup_frame/self.animation_speed:
                self.image_index += self.animation_speed
        else:
            if self.image_index < len(self.animation) - 1:
                self.image_index += self.animation_speed
            else:
                self.image_index = len(self.animation) - 1

    #### Set image
    if self.image_index > len(self.animation) - 1:
        self.image_index = len(self.animation) - 1
    self.image = self.animation[int(self.image_index)]

    if self.is_facing_right == False:
        self.image = pygame.transform.flip(self.image,True,False)

###################### GET IMAGES ######################

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def import_character_assets(self):
    name = self.character
    character_path = './animations/' + name + '/'
    self.animations = {'idle':[], 'walk':[],'dash':[], 'jump':[], 'fall':[], 'hit':[], 'f_tilt':[], 'down_air':[], 'up_tilt':[], 'neutral_special': [], 'up_special':[], 'side_special':[], 'ledgegrab': [], 'roll' :[], 'airdodge': [], 'shield':[],'grab':[] , 'boomerang': []}

    for animation in self.animations.keys():
        full_path = character_path + animation
        self.animations[animation] = import_folder(full_path)

###################### DUST PARTICLES ######################

run_particles = import_folder('./animations/dust_particles/run')
jump_particles = import_folder('./animations/dust_particles/jump')
land_particles = import_folder('./animations/dust_particles/land')

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,type, orientation):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.3
        if type == 'jump':
            self.frames = jump_particles
        if type == 'land':
            self.frames = land_particles
        self.image = self.frames[self.frame_index]
        self.pos = pos
        self.orientation = orientation
        
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self,x_shift):
        self.animate()
        self.pos = (self.pos[0] + x_shift, self.pos[1])

def run_dust_animation(self):
    x_hitbox, y_hitbox = get_real_pos(self)
    pos = (x_hitbox, y_hitbox)
    if abs(self.xspeed) > global_horizontal_speed and self.on_wall:
        self.dust_frame_index += 0.3 ### Dust animation speed
        if self.dust_frame_index >= len(run_particles):
            self.dust_frame_index = 0
        
        particle = run_particles[int(self.dust_frame_index)]
        
        if self.is_facing_right:
            pos = (x_hitbox - 32, y_hitbox + self.hitbox[1] - 10)
            
        else:
            pos = (x_hitbox + self.hitbox[0] + 12, y_hitbox + self.hitbox[1] - 10)
            particle = pygame.transform.flip(particle, True, False)
        
        screen.blit(particle, pos)

def draw(particle):
    if particle.orientation == 0 :
        particle.image = pygame.transform.flip(particle.image, True, False)
    screen.blit(particle.image, particle.pos)
        
def create_jump_particles(self):
    x_hitbox, y_hitbox = get_real_pos(self)
    pos = (x_hitbox, y_hitbox)

    if self.jumping_dust:
        self.jumping_dust = False
        if self.is_facing_right:
            pos = (x_hitbox - 40, y_hitbox + self.hitbox[1] - 32)
            orientation = 1 
        else:
            pos = (x_hitbox + self.hitbox[0] -40, y_hitbox + self.hitbox[1] - 32)
            orientation = 0

        jump_particle_sprite = ParticleEffect(pos,'jump', orientation)
        dust_sprites.add(jump_particle_sprite)

def create_landing_dust(self):
    x_hitbox, y_hitbox = get_real_pos(self)
    pos = (x_hitbox, y_hitbox)
    if self.landing_dust:
        self.landing_dust = False
        if self.is_facing_right:
            pos = (x_hitbox - 55, y_hitbox + self.hitbox[1] - 40)
            orientation = 1
        else:
            pos = (x_hitbox + self.hitbox[0] -75, y_hitbox + self.hitbox[1] - 40)
            orientation = 0

        fall_dust_particle = ParticleEffect( pos ,'land', orientation)
        dust_sprites.add(fall_dust_particle)