import pygame
import sys
from random import randint
from pygame.locals import *

try:
    from game.variables import *
    from game.wall import *
    from game.ledge import *
    from game.player import *
    from game.platforms import *
    from game.explosion import *
    from game.victory import *
except ImportError:
    from variables import *
    from wall import *
    from player import *
    from platforms import *
    from explosion import *
    from ledge import *
    from victory import *

def game_training_options():
    for player in players:
        player.stock_number = -1
    pygame.mixer.music.load("sounds/musics/music_training.ogg")


def game_loop(character1, character2, stages, stage):
    global players, screen

    #### Initiate the game ####
    if __name__ == '__main__':
        pygame.init()
        pygame.display.set_caption('Hyper Smash Bros.')
        pygame.display.set_icon(window_icon)
        screen = pygame.display.set_mode(window_size)

    clock = pygame.time.Clock()

    #### Stage parameters ####
    while stage == 'random' or stage == '':
        stage = stages[randint(0, 2)][randint(0, 2)]

    if stage == 'small_battlefield':
        walls.add(Wall((224, 384), 'wall'))
        platforms.add(Platform((322, 306), 'platform'))
        platforms.add(Platform((558, 306), 'platform'))
        ledges.add(Ledge((224, 384), 'left'))
        ledges.add(Ledge((224 + 512, 384), 'right'))
        pygame.mixer.music.load("sounds/musics/music_bf.ogg")
        background = pygame.image.load('sprites/stages/background.png')

    elif stage == 'battlefield':
        walls.add(Wall((224, 384), 'wall'))
        platforms.add(Platform((302, 306), 'platform'))
        platforms.add(Platform((578, 306), 'platform'))
        platforms.add(Platform((440, 228), 'platform'))
        ledges.add(Ledge((224, 384), 'left'))
        ledges.add(Ledge((224 + 512, 384), 'right'))
        pygame.mixer.music.load("sounds/musics/music_bf.ogg")
        background = pygame.image.load('sprites/stages/background.png')

    elif stage == 'final_destination':
        walls.add(Wall((224, 384), 'wall'))
        ledges.add(Ledge((224, 384), 'left'))
        ledges.add(Ledge((224 + 512, 384), 'right'))
        pygame.mixer.music.load("sounds/musics/music_fd.ogg")
        background = pygame.image.load('sprites/stages/background.png')

    elif stage == 'vogue_merry':
        walls.add(Wall((236, 384), 'platform_large'))
        ledges.add(Ledge((236, 384), 'left'))
        ledges.add(Ledge((236 + 488, 384), 'right'))
        pygame.mixer.music.load("sounds/musics/music_vogue_merry.ogg")
        background = pygame.image.load('sprites/stages/vogue_merry.png')

    pygame.mixer.music.play(loops=-1)
    #pygame.mixer.music.stop()

    #### Create players ####
    while character1 == 'Random' or character1 == '':
        character1 = characters[randint(0, 5)][randint(0, 1)]

    while character2 == 'Random' or character2 == '':
        character2 = characters[randint(0, 5)][randint(0, 1)]

    player1 = Player((256, 20), 1, character1)
    player2 = Player((672, 20), 2, character2)
    players.append(player1)
    players.append(player2)

    #### Variables ####
    space = 0
    pause = 0
    key_k = 0
    winner = 0
    quit_game = 0
    game = True
    loose = []

    while game:
        ########### REQUIRED ###########
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            ## TO DELETE ##
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    for player in players:
                        player.y = 30
                        player.x = 500

            if event.type == MOUSEBUTTONDOWN:
                left, _, right = pygame.mouse.get_pressed()
                if left:
                    walls.add(Wall(pygame.mouse.get_pos(), 'wall_no_texture'))
                elif right:
                    for wall in walls:
                        x, y = pygame.mouse.get_pos()
                        if 0 < x - wall.x < 32 and 0 < y - wall.y < 32:
                            wall.kill()
                            break
            ###############

        pygame.draw.rect(screen, (98, 198, 222), ((0, 0), window_size))
        screen.blit(background, (0, 0))
        ############################################

        for wall in walls:
            screen.blit(wall.image, (wall.x, wall.y))
        for platform in platforms:
            screen.blit(platform.image, (platform.x, platform.y))

        for attack in attacks:
            attack.update()

        for ledge in ledges:
            ledge.update()

        for cloud in clouds:
            cloud.update()

        for player in players:
            player.update()
            #### Respawn ####
            real_x, real_y = get_real_pos(player)
            if real_x < - 192 - player.hitbox[0] or real_x > window_size[0] + 256 or real_y > window_size[1] + 192 or (player.hitstun > 0 and real_y < - 192 - player.hitbox[1]):
                explosions.add(
                    Explosion((real_x + player.hitbox[0]/2, real_y + player.hitbox[1]/2)))
                player.stock -= 1
                if player.stock > 0:
                    respawn(player)

            #### Display stock and end game ####
            if player.stock > 0:
                for i in range(player.stock):
                    if player.player == 1:
                        screen.blit(player.stock_image, (306 + 14*i, 454))
                    if player.player == 2:
                        screen.blit(player.stock_image, (622 + 14*i, 454))
            else:
                if player.player not in loose:
                    loose.append(player.player)
                
                if __name__ == '__main__':
                    sys.exit()

        for explosion in explosions:
            explosion.update()

        ########### PLAYER 1 PERCENT ###########
        screen.blit(pygame.image.load(
            'sprites/miscellaneous/percent_hud.png').convert_alpha(), (226, 450))
        player_image = pygame.image.load(
            f'sprites/hud_icons/icon_{player1.character}.png').convert_alpha()
        screen.blit(player_image, (226, 450))
        percent = str(player1.percent)
        for i in range(len(percent)):
            screen.blit(font_percent[int(percent[i])],
                        (379-30*(len(percent)-i), 466))
        screen.blit(font_percent[10], (387, 466))

        ########### PLAYER 2 PERCENT ###########
        screen.blit(pygame.image.load('sprites/miscellaneous/percent_hud2.png'), (542, 450))
        player_image = pygame.image.load(
            f'sprites/hud_icons/icon_{player2.character}.png').convert_alpha()
        screen.blit(player_image, (542, 450))
        percent = str(player2.percent)
        for i in range(len(percent)):
            screen.blit(font_percent[int(percent[i])],
                        (695-30*(len(percent)-i), 466))
        screen.blit(font_percent[10], (703, 466))
        ############################################
        pygame.display.update()
        clock.tick(60)

        if len(loose) == len(players) - 1: # 1 Player left
            for player in players:
                if player.player not in loose:
                    winner = player
                    break
            victory(winner, [player for player in players if player != winner])

        """
        if player1.stock_number == 0:
            winner = 2
            game = False
        elif player2.stock_number == 0:
            winner = 1
            game = False

        if pause == 0:
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

            for explosion in explosions:
                explosion.update()

            #pygame.draw.rect(screen,(0,255,0),player1.rect)
            #pygame.draw.rect(screen,(0,255,0),player2.rect)

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
            screen.blit(pygame.image.load('./sprites/pause.png'),(0,0))

            if keys[K_ESCAPE]:
                quit_game = 1
                game = False

        

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
    
    if __name__ != '__main__':
        pygame.time.wait(50)
        name1 = player1.character
        name2 = player2.character
        for player in players:
            player.kill()
        players = []
        for attack in attacks:
            attack.kill()
        for explosion in explosions:
            explosion.kill()
        for kamehameha in kamehamehas:
            kamehameha.kill()
        for cloud in clouds:
            cloud.kill()
        for platform in platforms:
            platform.kill()
        if quit_game == 0:
            pass
            #victory(winner,name1,name2)
        """


if __name__ == '__main__':
    game_loop('Goku', 'Luffy', stages, 'vogue_merry')
    pygame.quit()
    sys.exit()
