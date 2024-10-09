import pygame
import sys
from pygame.locals import *
from game.variables import *
from game.player import *
from game.attack import *
from game.wall import *
from game.platforms import *
from game.instruction import *


def buton(x, y, l, h, screen, text, color, n):
    list = ["quit", "skip"]
    smallfont = pygame.font.SysFont('Corbel', 35)
    screen_text = smallfont.render(text, True, color)
    width_text = pygame.Surface.get_width(screen_text)
    heigth_text = pygame.Surface.get_height(screen_text)
    mouse = pygame.mouse.get_pos()

    if n == 0 and x <= mouse[0] <= x+l and y <= mouse[1] <= y + h:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
    if n == 1 and x <= mouse[0] <= x+l and y <= mouse[1] <= y + h:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                instruction.succeed = 1
                instruction.frame_index = instruction.time + 1

     #   pygame.draw.rect(screen,(150,150,150),(x,y,l,h))
    # else:
      #  pygame.draw.rect(screen,(90,90,90),(x,y,l,h))
    path = './tutorial/' + list[n] + ".png"
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (l, h))
    screen.blit(image, (x, y))
    #pygame.draw.rect(screen, color,(x,y,l,h))


def game_initialisation(character1, character2, stage):
    # Initiate the game
    global clock
    clock = pygame.time.Clock()
    pygame.init()  # Initialize the game
    pygame.display.set_caption('Hyper Smash Bros.')
    pygame.display.set_icon(window_icon)

    # Create instances
    global player1
    global player2
    player1 = Player((256, 20), 1, character1)
    player2 = Player((672, 20), 2, character2)
    walls.add(Wall(224, window_size[1] - 160))
    while stage == [1, 1]:
        stage[0] = randint(0, 1)
        stage[1] = randint(0, 1)

    if stage == [0, 0]:
        platforms.add(Platform(322, 306))
        platforms.add(Platform(558, 306))
        pygame.mixer.music.load("Music\music_bf.ogg")
    elif stage == [1, 0]:
        platforms.add(Platform(302, 306))
        platforms.add(Platform(578, 306))
        platforms.add(Platform(440, 228))
        pygame.mixer.music.load("Music\music_bf.ogg")
    else:
        pygame.mixer.music.load("Music\music_fd.ogg")

    pygame.mixer.music.play(loops=-1)

    players.append(player1)
    players.append(player2)
    global instruction
    instruction = Instruction(0)


# Game loop
def game_loop():
    global player1
    global player2
    global game
    global instruction
    screen = pygame.display.set_mode(window_size)  # Create the screen

    # Variables
    space = 0
    pause = 0
    key_k = 0
    winner = 0
    quit_game = 0
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == QUIT:  # Close the window
                pygame.quit()
                sys.exit()
        screen.fill((98, 198, 222))  # Refresh screen
        screen.blit(background, (0, 0))
        quit = buton(840,430,90,90,screen,"a",(255,25,255),0)
        skip = buton(770,430,90,90,screen,"a",(255,25,255),1)
        if pause == 0:
            for wall in walls:
                screen.blit(wall.image, (wall.x, wall.y))
            for platform in platforms:
                screen.blit(platform.image, (platform.x, platform.y))
            for cloud in clouds:
                cloud.update()

            for kamehameha in kamehamehas:
                for player in players:
                    if player.character == 'Goku':
                        kamehameha.update(player)
                        kamehameha.animate_kamehameha(player)

            for ledge in ledges:
                ledge.update_ledge_timer()

                if not (ledge.player_to_ledge(player2)):
                    ledge.update_ledge_actions(player1)
                if not (ledge.player_to_ledge(player1)):
                    ledge.update_ledge_actions(player2)

            player1.update()
            player2.update()
            instruction.update(player1.get_key(), screen, player1, player2)

            for attack in attacks:
                attack.update()
            for explosion in explosions:
                explosion.update()

            # pygame.draw.rect(screen,(0,255,0),player1.rect)
            # pygame.draw.rect(screen,(0,255,0),player2.rect)

        else:
            for wall in walls:
                screen.blit(wall.image, (wall.x, wall.y))
            for platform in platforms:
                screen.blit(platform.image, (platform.x, platform.y))
            for attack in attacks:
                attack.draw_and_collision()
            for cloud in clouds:
                cloud.draw()
            for explosion in explosions:
                explosion.draw()

            player1.draw()
            player2.draw()
            # pygame.draw.rect(screen,(0,255,0),player1.rect)
            # pygame.draw.rect(screen,(0,255,0),player2.rect)
            screen.blit(pygame.image.load('./sprites/pause.png'), (0, 0))

            if keys[K_ESCAPE]:
                quit_game = 1
                game == False

        # Player 1 percent
        screen.blit(pygame.image.load(
            'sprites/percent_hud.png').convert_alpha(), (226, 450))
        player_image = pygame.image.load(
            './icon/icon_hud/icon_' + str(player1.character) + '.png').convert_alpha()
        screen.blit(player_image, (46-player_image.get_width() /
                    2+226, 46-player_image.get_height()/2+450))
        percent = str(player1.percent)
        for i in range(len(percent)):
            screen.blit(font_percent[int(percent[i])],
                        (379-30*(len(percent)-i), 466))
        screen.blit(font_percent[10], (387, 466))

        # Player 2 percent
        screen.blit(pygame.image.load('sprites/percent_hud2.png'), (542, 450))
        if player2.character != 'default':
            player_image = pygame.image.load(
                './icon/icon_hud/icon_' + str(player2.character) + '.png').convert_alpha()
        else:
            player_image = pygame.image.load(
                './sprites/player2.png').convert_alpha()
        screen.blit(player_image, (46-player_image.get_width() /
                    2+542, 46-player_image.get_height()/2+450))
        percent = str(player2.percent)
        percent_index = 0
        for i in range(len(percent)):
            screen.blit(font_percent[int(percent[i])],
                        (695-30*(len(percent)-i), 466))
        screen.blit(font_percent[10], (703, 466))

        pygame.display.update()  # Update the screen
        clock.tick(60)  # 60 fps

        keys = pygame.key.get_pressed()

        if keys[K_SPACE]:  # Check pause
            if space == 0:
                space = 1
                if pause:
                    pause = 0
                else:
                    pause = 1
        else:
            space = 0
        if keys[K_k]:  # Display all variables
            if key_k == 0:
                key_k = 1
                print('==== Player 1 ====')
                for variables in player1.__dict__:
                    print(str(variables) + ' : ' +
                          str(player1.__dict__[variables]))
                print('==== Player 2 ====')
                for variables in player2.__dict__:
                    print(str(variables) + ' : ' +
                          str(player2.__dict__[variables]))
            key_k = 0

if __name__ == '__main__':
    game_initialisation('Kirby', 'Marth', [1, 0])
    game_loop()
