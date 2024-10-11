import pygame
from pygame.locals import *

window_size = (960, 544)
window_icon = pygame.image.load('./sprites/miscellaneous/icon.png')
screen = pygame.display.set_mode(window_size)

##### Menu #####
base_width = screen.get_width()
base_height = screen.get_height()
xscale = 1
yscale = 1
characters = [['Kirby', 'Goku'], ['Pikachu', 'Luffy'], [
    'Marth', ''], ['Hal', ''], ['Pirate', ''], ['The_Cube', 'Random']]
stages = [['battlefield','small_battlefield','final_destination'],['vogue_merry','',''],['','','random']]

##### Game #####

# Set percent font
font_percent = []
for i in range(10):
    font_percent.append(pygame.image.load(f'font/{i}.png').convert_alpha())
font_percent.append(pygame.image.load('font/percent.png').convert_alpha())



background = pygame.image.load('./sprites/stages/background.png')
players = []
walls = pygame.sprite.Group()
platforms = pygame.sprite.Group()
attacks = pygame.sprite.Group()
explosions = pygame.sprite.Group()
clouds = pygame.sprite.Group()
ledges = pygame.sprite.Group()
dust_sprites = pygame.sprite.Group()

kamehamehas = pygame.sprite.Group()

show_hitbox = 0

global_jump_force = -7.5
global_fall_landing_lag = 5
global_horizontal_speed = 3
global_air_speed = 3.5
global_dash_window = 15
global_hitstun = 30
global_airborne = 60
global_roll_endlag = 10
global_roll_speed = 6
global_roll_duration = 20
global_stock_number = 4
global_respawn_invincibility_time = 120
global_airdodge_inv_time = 30
global_airdodge_landing_lag = 15
global_airdodge_endlag = 15
global_ledge_hitbox = (8, 8)
global_grab_lag = 15
global_ledgegrab_invincibility = 30
global_ledgegrab_lag = 25
global_ledgejump_invincibility = 5
global_ledgeroll_invincibility = 35
global_neutral_getup_invincibility = 30
global_frames_between_2_ledge_grabs = 30

global_jump_lag = 20
global_shielddrop_frames = 3
global_lag_endlag = 10
global_kamehameha_duration = 60
global_kamehameha_startup = 30

#### Hal = Fox ; Pirate = PAC-MAN ; The_Cube = Mr. Game & Watch ; Goku = Captain Falcon ; Luffy = Hero

weights = {
    'Kirby': 79,
    'Pikachu': 79,
    'Marth': 90,
    'Hal': 77,
    'Pirate': 95,
    'The_Cube': 75,
    'Goku': 104,
    'Luffy': 101,
}
running_speeds = {
    'Kirby': 1.547,
    'Pikachu': 1.839,
    'Marth': 1.764,
    'Hal': 1.902,
    'Pirate': 1.572,
    'The_Cube': 1.579,
    'Goku': 2.002,
    'Luffy': 1.64,
}
air_speeds = {
    'Kirby': 0.8,
    'Pikachu': 0.957,
    'Marth': 1.071,
    'Hal': 1.11,
    'Pirate': 1.092,
    'The_Cube': 1.176,
    'Goku': 1.218,
    'Luffy': 1.01,
}
falling_parameters = { # (falling_speed, max_falling_speed, fast_falling_speed)
    'Kirby': (0.24, 9.23, 9.968),
    'Pikachu': (0.36, 9.55, 10.48),
    'Marth': (0.28, 9.58, 10.528),
    'Hal': (0.4, 10.1, 11.36),
    'Pirate': (0.27, 9.35, 10.16),
    'The_Cube': (0.3, 9.24, 9.984),
    'Goku': (0.32, 9.865, 10.984),
    'Luffy': (0.26, 9.6, 11.04),
}
jumps = {
    'Kirby': 5,
    'Pikachu': 2,
    'Marth': 2,
    'Hal': 3,
    'Pirate': 2,
    'The_Cube': 2,
    'Goku': 2,
    'Luffy': 2,
}
jump_forces = {
    'Kirby': 0.75,
    'Pikachu': 1.05,
    'Marth': 1,
    'Hal': 1.04,
    'Pirate': 1.01,
    'The_Cube': 0.92,
    'Goku': 1.1,
    'Luffy': 0.96,
}
hitbox_dependency = {
    'Kirby': 0,
    'Pikachu': 0,
    'Marth': 0,
    'Hal': 0,
    'Pirate': 0,
    'The_Cube': 0,
    'Goku': 0,
    'Luffy': 10,
}
player_key = {
    1:{
        'up': K_z,
        'down': K_s,
        'right': K_d,
        'left': K_q,
        'attack': K_a,
        'jump': K_e,
        'shield':K_f,
        'grab': K_r,
        'special': K_t
    },
    2:{
        'up': K_UP,
        'down': K_DOWN,
        'right': K_RIGHT,
        'left': K_LEFT,
        'attack': K_RCTRL,
        'jump': K_RSHIFT,
        'shield': K_COLON,
        'grab': K_RETURN,
        'special': K_SEMICOLON
    }
}
image_var = {  
    'Kirby': {
        'hitbox': (30, 34),
        'offset': [17, 30],
    },
    'Marth': {
        'hitbox': (21, 47),
        'offset': [53, 40],
    },
    'Pirate': {
        'hitbox': (32, 33),
        'offset': [42, 35],
    },
    'Hal': {
        'hitbox': (23, 32),
        'offset': [28, 20],
    },
    'Pikachu': {
        'hitbox': (20, 34),
        'offset': [54, 48],
    },
    'Goku': {
        'hitbox': (28, 42),
        'offset': [50, 44],
    },
    'Luffy': {
        'hitbox': (20, 49),
        'offset': [113, 100],
    }
}
color_list = {
    1: (255, 0, 0),
    2: (0, 0, 255),
}
#'attack' : [startup_frame, hitbox_size, hit_location, active_frames, startup,x_eject,y_eject, hitstun, damage,end_lag,grab_attack,(depending on facing,number of pixels)]
#'projectile': [startup,x_eject,y_eject,xspeed,yspeed,hitstun,damage,image_name, endlag,projectile_lag]

# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
# Throw : [ejection, hitstun, damage]

attack_list = {
    "The_Cube":{# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
        'down_air': [(0,8), (0,24), (16,16), 1, 15, 10, 20, 8, 'sound_slap_m.ogg', 0],
        'up_tilt': [(0, -7.5), (0, -19), (16, 16), 1, 5, 10, 25, 5, 'sound_slap_m.ogg', 0],
        'f_tilt': [(5, -5), (24, 0), (16, 16), 3, 10, 20, 10, 12, 'sound_slap_m.ogg', 0],
        'grab': [(20,0), (8,8), 3, 2, 8],
        'f_throw': [(5, -6.5), 30, 3],
        'up_throw': [(0, -8), 35, 4],

        'neutral_b': [5,0,0,5,0,5,3,'fireball.png',12, 20,'sound_slap_m.ogg']
    },
    "Kirby":{# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
        'down_air': [(0, 8), (0, 34), (16, 14), 8, 4, 10, 17, 13, 'sound_slap_m.ogg', 1],
        'up_tilt': [(0, -8), (12, -23), (16, 16), 7, 5, 12, 20, 6, 'sound_slap_m.ogg', 1],
        'f_tilt': [(5, -5), (20, 6), (20, 16), 10, 10, 20, 10, 12, 'sound_slap_m.ogg', 1],
        'grab': [(20,0), (8,8), 3, 2, 8],
        'f_throw': [(5, -6.5), 30, 3],
        'up_throw': [(0, -8), 35, 4], 
   
        'neutral_b': [15,3,-1,6,0,10,6,'gordo.png',12, 30,'sound_slap_m.ogg']
    },
    "Marth":{# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
        'down_air': [(0, 8), (0, 20), (32, 14), 13, 3, 18, 20, 13, 'sound_meteor_smash.ogg', 1],
        'up_tilt': [(0, -8.5), (0, -38), (36, 30), 7, 3, 25, 28, 8, 'sound_slash_s.ogg', 1],
        'f_tilt': [(6, -4), (26, -2), (28, 34), 10, 5, 30, 18, 15, 'sound_slash_m.ogg', 0],
        'grab': [(23, -2), (12, 12), 2, 3, 25],
        'f_throw': [(6, -7), 40, 5],
        'up_throw': [(0, -10), 40, 4],
        
        'neutral_b': [4,(38,16),(0,0),2,20,8,-5,10, 20,25,0,[1,32],'sound_slash_m.ogg']
    },
    "Pikachu":{# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
        'down_air': [(0, 8), (0, 40), (16, 20), 10, 1, 10, 20, 10, 'sound_slap_m.ogg', 1],
        'up_tilt': [(0, -8), (-6, -34), (22, 14), 8, 2, 12, 20, 6, 'sound_slap_m.ogg', 1],
        'f_tilt': [(4.5, -5.5), (30, 2), (22, 24), 7, 2, 18, 19, 11, 'sound_slap_m.ogg', 1],
        'grab': [(20,0), (8,8), 3, 2, 8],
        'f_throw': [(5, -6.5), 30, 3],
        'up_throw': [(0, -8), 35, 4],

        'neutral_b': [15,1,-1,7,0,7,4,'electric_ball.png',12, 30,'sound_electric_s.ogg']
    },
    "Hal":{# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
        'down_air': [(0, 8), (0, 24), (16, 16), 15, 1, 10, 20, 8, 'sound_slap_m.ogg', 0],
        'up_tilt': [(0, -5), (0, -19), (16, 16), 5, 1, 15, 25, 5, 'sound_slap_m.ogg', 0],
        'f_tilt': [(5, -5), (24, 0), (16, 16), 10, 3, 20, 10, 12, 'sound_slap_m.ogg', 0],
        'grab': [(20,0), (8,8), 3, 2, 8],
        'f_throw': [(5, -6.5), 30, 3],
        'up_throw': [(0, -8), 35, 4],  
  
        'neutral_b': [1,0,0,5,0,5,3,'fireball.png',12,15,'sound_slap_m.ogg']
    },
    "Pirate":{# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
        'down_air': [(0, 8), (0, 24), (16, 16), 15, 1, 10, 20, 8, 'sound_slap_m.ogg', 0],
        'up_tilt': [(0, -5), (0, -19), (16, 16), 5, 1, 15, 25, 5, 'sound_slap_m.ogg', 0],
        'f_tilt': [(5, -5), (24, 0), (16, 16), 10, 3, 20, 10, 12, 'sound_slap_m.ogg', 0],
        'grab': [(20,0), (8,8), 3, 2, 8],
        'f_throw': [(5, -6.5), 30, 3],
        'up_throw': [(0, -8), 35, 4],

        'neutral_b': [5,0,0,5,0,5,3,'barrel.png',12,15, 'sound_slap_m.ogg']
    },
    "Goku":{# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
        'down_air': [(1.5, 8), (12,20), (32,32), 15, 5, 15, 20, 20, 'sound_punch_l.ogg', 4],
        'up_tilt': [(0, -8), (0, -20), (45, 40), 6, 2, 15, 25, 5, 'sound_kick_s.ogg', 3],
        'f_tilt': [(8, -6), (24, 12), (48, 28), 17, 7, 15, 15, 15, 'sound_kick_m.ogg', 6],
        'grab': [(24, -4), (12, 24), 2, 5, 5],
        'f_throw': [(6, -8), 40, 5],
        'up_throw': [(0, -10), 40, 4],

        'neutral_b': [0,(64,32),(-11,6), global_kamehameha_duration + 30, global_kamehameha_startup,-5,-5, 10, 15,60,0,[0,0],'sound_slap_m.ogg']    
    },
    "Luffy":{# [ejection, relative_position, hitbox, startup, active_frames, end_lag, hitstun, damage, sound, freezing_animation_frame]
        'down_air': [(0, 8), (-6, 76), (24, 24), 9, 2, 24, 13, 12, 'sound_meteor_smash.ogg', 3],
        'up_tilt': [(2, -8), (32, -16), (24, 36), 6, 3, 20, 13, 8, 'sound_kick_s.ogg', 2],
        'f_tilt': [(7, -6), (40, 0), (16, 16), 9, 4, 12, 14, 10, 'sound_kick_s.ogg', 3],
        'grab': [(34, 0), (12, 24), 2, 5, 5], # [relative_position, hitbox, startup, active_frames, end_lag]
        'f_throw': [(6, -7), 40, 5],
        'up_throw': [(0, -10), 40, 4],

        'neutral_b': [4,(38,16),(0,0),2,20,8,-5,10, 20,25,0,[1,32],'sound_kick_m.ogg']
    }
        #'neutral_b': [20,(64,32),(-11,6), global_kamehameha_duration , global_kamehameha_startup,-5,-5, 10, 15,30,0,[0,0],'sound_slap_m.ogg']    
}   #[4,(64,32),(-11,6),2,50,-5,-5, 10, 15,30,0,[0,0]] 
