from random import randint
import pygame
import sys
from math import cos
from pygame.locals import *
try:
    from game.variables import *
    from game.functions import best_ratio, add_path, cursor_width
    from game.main import game_loop
except ImportError:
    from variables import *
    from functions import best_ratio, add_path, cursor_width
    from main import game_loop

###########################
# Initialization
pygame.init()
pygame.display.set_caption('Hyper Smash Bros.')
pygame.display.set_icon(window_icon)
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
clock = pygame.time.Clock()
###########################
# Images
images_list = dict()
images_list['load_path'] = set()
image_paths = ['menu', 'menu/select_screen']
add_path(images_list, image_paths)


###########################
# Sound
sound_title = pygame.mixer.Sound("sound_effects/sound_title.ogg")
sound_button = pygame.mixer.Sound("sound_effects/sound_button.ogg")
sound_back = pygame.mixer.Sound("sound_effects/sound_back.ogg")
sound_start_fight = pygame.mixer.Sound("sound_effects/sound_start_fight.ogg")
sound_select_menu = pygame.mixer.Sound("sound_effects/sound_select_menu.ogg")

###########################
# Variables
count = 0
state = 0
color_list = [(160, 0, 5), (1, 171, 214), (2, 162, 58), (254, 242, 0)]
color = [0, 0, 255]

while True:
    events = pygame.event.get()
    screen.fill((255, 255, 255))
    for event in events:
        if event.type == QUIT:  # Close the window
            pygame.quit()
            sys.exit()
        if event.type == VIDEORESIZE:
            window_size = (event.w, event.h)
            window_size = best_ratio(window_size)
            xscale, yscale = window_size
            xscale /= base_width
            yscale /= base_height

            images_list = dict()
            images_list['load_path'] = set()
            add_path(images_list, image_paths)
            for key in images_list:
                if key != 'load_path':
                    image = images_list[key]
                    images_list[key] = pygame.transform.scale(
                        image, (image.get_width()*xscale, image.get_height()*yscale))
    ######################

    ######################## TITLE SCREEN ########################
    if state == 0:  # Title screen loading
        if count < 60:
            count += 1
        else:
            count = 0
            state = 1

        if count >= 30:  # Horizontal line
            screen.blit(images_list['horizontal_line'], ((-1024+34.13*(count-30))
                        * xscale, (-86+2.87*(count-30))*yscale))

        if count < 30:  # Vertical line
            screen.blit(images_list['vertical_line'], ((47-1.57*count) *
                        xscale, (-544+18.13*count)*yscale))
        else:
            screen.blit(images_list['vertical_line'], (0, 0))

    if state == 1 or state == 1.5:  # Press Any Button and logo
        if count < 100:
            count += 1
        else:
            count = 0

        screen.blit(images_list['vertical_line'], (0, 0))
        screen.blit(images_list['horizontal_line'], (0, 0))
        screen.blit(images_list['smash_logo'], (180*xscale, 40*yscale))
        images_list['press_any_button'].set_alpha(255*cos(count*3.14/60)+255)
        screen.blit(images_list['press_any_button'], (269*xscale, 414*yscale))

        for event in events:
            if event.type == KEYUP and state == 1:  # Skip title screen
                count = 0
                sound_title.play()
                state = 1.5

    if state == 1.5:  # Transition
        if count < sound_title.get_length():
            count += 1
        else:

            # Play music
            pygame.mixer.music.load("Music/music_menu_b.ogg")
            pygame.mixer.music.play(loops=-1)

            count = 0
            left = 0
            up = 0
            state = 2

    ######################## MAIN MENU ########################
    if state == 2:
        pygame.draw.rect(screen, (10, 10, 10),
                         (0, 0, window_size[0], window_size[1]))

        pygame.draw.rect(screen, color_list[left + 2*up], [
                         (50 + 445*left)*xscale, (19 + 268*up)*yscale, 415*xscale, 238*yscale])

        # Mode menu backgrounds
        if count < 60:
            count += 1
        else:
            count = 0

        red_bg = images_list['red_background']
        green_bg = images_list['green_background']
        blue_bg = images_list['blue_background']
        yellow_bg = images_list['yellow_background']

        # Blur effect
        size = images_list['red_background'].get_size()

        if not (left == 0 and up == 0) or count == 0:
            red_bg = images_list['red_background']
        else:
            if count < 30:
                red_bg = pygame.transform.scale(
                    red_bg, (size[0]/(count/10+1), size[1]/(count/10+1)))
            else:
                red_bg = pygame.transform.scale(
                    red_bg, (size[0]/((60 - count)/10+1), size[1]/((60 - count)/10+1)))
            red_bg = pygame.transform.scale(red_bg, size)
        if not (left == 0 and up == 1) or count == 0:
            green_bg = images_list['green_background']
        else:
            if count < 30:
                green_bg = pygame.transform.scale(
                    green_bg, (size[0]/(count/10+1), size[1]/(count/10+1)))
            else:
                green_bg = pygame.transform.scale(
                    green_bg, (size[0]/((60 - count)/10+1), size[1]/((60 - count)/10+1)))
            green_bg = pygame.transform.scale(green_bg, size)
        if not (left == 1 and up == 0) or count == 0:
            blue_bg = images_list['blue_background']
        else:
            if count < 30:
                blue_bg = pygame.transform.scale(
                    blue_bg, (size[0]/(count/10+1), size[1]/(count/10+1)))
            else:
                blue_bg = pygame.transform.scale(
                    blue_bg, (size[0]/((60 - count)/10+1), size[1]/((60 - count)/10+1)))
            blue_bg = pygame.transform.scale(blue_bg, size)
        if not (left == 1 and up == 1) or count == 0:
            yellow_bg = images_list['yellow_background']
        else:
            if count < 30:
                yellow_bg = pygame.transform.scale(
                    yellow_bg, (size[0]/(count/10+1), size[1]/(count/10+1)))
            else:
                yellow_bg = pygame.transform.scale(
                    yellow_bg, (size[0]/((60 - count)/10+1), size[1]/((60 - count)/10+1)))
            yellow_bg = pygame.transform.scale(yellow_bg, size)

        screen.blit(red_bg, (55*xscale, 24*yscale))
        screen.blit(green_bg, (55*xscale, 292*yscale))
        screen.blit(blue_bg, (500*xscale, 24*yscale))
        screen.blit(yellow_bg, (500*xscale, 292*yscale))

        #### Texts and icons
        screen.blit(images_list['smash_text'], (55*xscale, 24*yscale))
        screen.blit(images_list['training_text'], (55*xscale, 292*yscale))
        screen.blit(images_list['tutorial_text'], (500*xscale, 24*yscale))
        screen.blit(images_list['options_text'], (500*xscale, 292*yscale))
        screen.blit(images_list['smash_icon'], (55*xscale, 24*yscale))
        screen.blit(images_list['training_icon'], (55*xscale, 292*yscale))
        screen.blit(images_list['tutorial_icon'], (500*xscale, 24*yscale))
        screen.blit(images_list['options_icon'], (500*xscale, 292*yscale))

        # Smash ball
        pygame.draw.ellipse(screen, color_list[left + 2*up], (window_size[0] /
                                                              2 - 125*xscale, window_size[1]/2 - 125*yscale, 250*xscale, 250*yscale))
        screen.blit(images_list['smash_ball'], (window_size[0] /
                    2 - 125*xscale, window_size[1]/2 - 125*yscale))

        # Navigate in main menu and select
        for event in events:
            if event.type == KEYDOWN:  # Navigate
                if (event.key == K_LEFT or event.key == K_q) and left == 1:
                    left = 0
                    count = 0
                    sound_button.play()
                if (event.key == K_RIGHT or event.key == K_d) and left == 0:
                    left = 1
                    count = 0
                    sound_button.play()
                if (event.key == K_UP or event.key == K_z) and up == 1:
                    up = 0
                    count = 0
                    sound_button.play()
                if (event.key == K_DOWN or event.key == K_s) and up == 0:
                    up = 1
                    count = 0
                    sound_button.play()
            if event.type == KEYUP:  # Select
                if event.key == K_a or event.key == K_RCTRL:
                    state = 3 + (left + 2*up)
                    count = 0
                    count1 = 0
                    count2 = 0

                    key_left_1 = False
                    key_up_1 = False
                    key_right_1 = False
                    key_down_1 = False

                    key_left_2 = False
                    key_up_2 = False
                    key_right_2 = False
                    key_down_2 = False

                    left_1 = 0
                    up_1 = 0
                    left_2 = 1
                    up_2 = 0

                    ready_1 = False
                    ready_2 = False

                    sound_select_menu.play()

    ######################## CHARACTER SELECT SCREEN ########################
    if state == 3:
        # Background color gradient
        if count < 767:
            count += 1
        else:
            count = 0
            color = [0, 0, 255]

        if count < 255:
            color[0] += 1
            color[1] += 1
            color[2] -= 2
        elif count < 511:
            color[0] += 1
            color[1] -= 1
        else:
            color[0] -= 1
            color[2] += 1

        for i in range(len(color)):
            if color[i] < 0:
                color[i] = 0
            if color[i] > 220:
                color[i] = 220
        pygame.draw.rect(screen, tuple(color),
                         (0, 0, window_size[0], window_size[1]))

        # Draw
        screen.blit(images_list['character_select_foreground'], (0, 0))

        # Player 1
        character_1 = characters[left_1][up_1]
        if character_1 == '' or left_1 < 0:
            character_1 = 'empty'
        image_1 = images_list[character_1].copy()
        if count1 < 30:
            count1 += 2*xscale
        if count1 > 30:
            count1 = 30
        image_1.set_alpha(255*(count1/30)**2)
        screen.blit(image_1, ((162 - (30 - int(count1)))*xscale, 317*yscale))

        if ready_1:
            screen.blit(images_list['ready_text'], (246*xscale, 511*yscale))

        # Player 2
        character_2 = characters[left_2][up_2]
        if character_2 == '' or left_2 < 0:
            character_2 = 'empty'
        image_2 = images_list[character_2].copy()
        if count2 < 30:
            count2 += 2*xscale
        if count2 > 30:
            count2 = 30
        image_2.set_alpha(255*(count2/30)**2)
        screen.blit(image_2, ((563 - (30 - int(count2)))*xscale, 317*yscale))
        if ready_2:
            screen.blit(images_list['ready_text'], (649*xscale, 511*yscale))

        # Players cursors
        pygame.draw.rect(screen, (77, 0, 168), ((162 + 76 * left_2)*xscale,
                         (72 + 76 * up_2)*yscale, 76*xscale, 76*yscale), width=2)
        pygame.draw.rect(screen, (168, 0, 0), ((162 + 76 * left_1)*xscale,
                         (72 + 76 * up_1)*yscale, 76*xscale, 76*yscale), width=2)

        # Ready to fight
        if ready_1 and ready_2:
            screen.blit(images_list['ready_to_fight'], (0, 0))

        # Get input
        for event in events:
            if event.type == KEYUP:
                if (event.key == K_a and left_1 == -2) or (event.key == K_RCTRL and left_2 == -2):  # Return to menu
                    sound_select_menu.play()
                    state = 2
                if (event.key == K_RETURN or event.key == K_SPACE) and ready_1 and ready_2:  # Confirm selection
                    sound_select_menu.play()
                    state = 7
                    left = 0
                    up = 0
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        # Player 1
        if keys[K_a]:  # Select an option
            if character_1 != 'empty' and ready_1 == False:
                sound_select_menu.play()
                ready_1 = True
                if character_1 != 'Random':
                    pygame.mixer.Sound(
                        f'Announcer/announcer_{character_1}.ogg').play()
        if keys[K_t] and ready_1:  # Deselect a character
            sound_back.play()
            ready_1 = False

        if ready_1 == False:
            if keys[K_z]:
                if key_up_1 == False:
                    key_up_1 = True
                    # Player 1 - UP
                    if up_1 > 0:
                        up_1 -= 1
                        sound_button.play()
                        count1 = 0
            else:
                key_up_1 = False
            if keys[K_q]:
                if key_left_1 == False:
                    key_left_1 = True
                    # Player 1 - LEFT
                    if left_1 > 0:
                        left_1 -= 1
                        sound_button.play()
                        count1 = 0
                    elif left_1 == 0 and up_1 == 0:
                        left_1 = -2
                        sound_button.play()
            else:
                key_left_1 = False
            if keys[K_s]:
                if key_down_1 == False:
                    key_down_1 = True
                    # Player 1 - DOWN
                    if up_1 < 1 and left_1 != -2:
                        up_1 += 1
                        sound_button.play()
                        count1 = 0
            else:
                key_down_1 = False
            if keys[K_d]:
                if key_right_1 == False:
                    key_right_1 = True
                    # Player 1 - RIGHT
                    if left_1 == -2:
                        left_1 = 0
                        sound_button.play()
                        count1 = 0
                    elif left_1 < 5:
                        left_1 += 1
                        sound_button.play()
                        count1 = 0
            else:
                key_right_1 = False

        # Player 2
        if keys[K_RCTRL]:  # Select an option
            if character_2 != 'empty' and ready_2 == False:
                sound_select_menu.play()
                ready_2 = True
                if character_2 != 'Random':
                    pygame.mixer.Sound(
                        f'Announcer/announcer_{character_2}.ogg').play()
        if keys[K_SEMICOLON] and ready_2:  # Deselect a character
            sound_back.play()
            ready_2 = False

        if ready_2 == False:
            if keys[K_UP]:
                if key_up_2 == False:
                    key_up_2 = True
                    # Player 2 - UP
                    if up_2 > 0:
                        up_2 -= 1
                        sound_button.play()
                        count2 = 0
            else:
                key_up_2 = False
            if keys[K_LEFT]:
                if key_left_2 == False:
                    key_left_2 = True
                    # Player 2 - LEFT
                    if left_2 > 0:
                        left_2 -= 1
                        sound_button.play()
                        count2 = 0
                    elif left_2 == 0 and up_2 == 0:
                        left_2 = -2
                        sound_button.play()
            else:
                key_left_2 = False
            if keys[K_DOWN]:
                if key_down_2 == False:
                    key_down_2 = True
                    # Player 2 - DOWN
                    if up_2 < 1 and left_2 != -2:
                        up_2 += 1
                        sound_button.play()
                        count2 = 0
            else:
                key_down_2 = False
            if keys[K_RIGHT]:
                if key_right_2 == False:
                    key_right_2 = True
                    # Player 2 - RIGHT
                    if left_2 == -2:
                        left_2 = 0
                        sound_button.play()
                        count2 = 0
                    elif left_2 < 5:
                        left_2 += 1
                        sound_button.play()
                        count2 = 0
            else:
                key_right_2 = False

    ######################## STAGE SELECTION ########################
    if state == 7:
        # Selection inputs
        for event in events:
            if event.type == KEYUP:
                if event.key == K_t or event.key == K_SEMICOLON:  # Back to select screen
                    state = 3
                    count = 0
                    count1 = 0
                    count2 = 0

                    key_left_1 = False
                    key_up_1 = False
                    key_right_1 = False
                    key_down_1 = False

                    key_left_2 = False
                    key_up_2 = False
                    key_right_2 = False
                    key_down_2 = False

                    left_1 = 0
                    up_1 = 0
                    left_2 = 1
                    up_2 = 0

                    ready_1 = False
                    ready_2 = False

                    sound_back.play()

                if (event.key == K_a or event.key == K_RCTRL):  # Stage selected
                    stage = stages[up][left]
                    if stage != '':
                        sound_select_menu.play()
                        count = 0
                        ready_1 = 0
                        ready_2 = 0
                        state = 10
                        pygame.mixer.music.stop()

            # Move cursor
            if event.type == KEYDOWN:
                if (event.key == K_q or event.key == K_LEFT) and left > 0:
                    left -= 1
                    sound_button.play()
                elif (event.key == K_z or event.key == K_UP) and up > 0:
                    up -= 1
                    sound_button.play()
                elif (event.key == K_d or event.key == K_RIGHT) and left < 2:
                    left += 1
                    sound_button.play()
                elif (event.key == K_s or event.key == K_DOWN) and up < 2:
                    up += 1
                    sound_button.play()

        # Draw
        screen.blit(images_list['stage_selection_background'], (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), ((99 + 265*left)*xscale, (36 + 145*up)
                         * yscale, 233*xscale, 128*yscale), width=cursor_width(xscale, yscale), border_radius=-1)

    ######################## BEGINNING OF FIGHT ########################
    if state == 10:
        if count < 60*sound_select_menu.get_length():
            count += 1
        else:
            state = 3
            count = 0

            game_loop(character_1, character_2, stages, stage)  # Start game

        screen.blit(images_list['stage_selection_background'], (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), ((99 + 265*left)*xscale, (36 + 145*up)
                         * yscale, 233*xscale, 128*yscale), width=cursor_width(xscale, yscale), border_radius=-1)
    ######################
    pygame.display.update()  # Update the screen
    clock.tick(60)  # 60 fps
