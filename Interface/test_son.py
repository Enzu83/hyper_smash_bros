import pygame
from pygame import *
import sys

#Constantes globales
res = (720,720)

white = (255,255,255) 
color_light = (170,170,170)
color_dark = (100,100,100)
black=(0,0,0)

#Variables globales
grid_size=0
theme=0

#Fonctions auxiliaires

def text_to_screen(text,color):
    smallfont = pygame.font.SysFont('Corbel',35) 
    screen_text = smallfont.render(text , True , color)

    width_text = pygame.Surface.get_width(screen_text)
    height_text = pygame.Surface.get_height(screen_text)

    return screen_text, width_text, height_text

def buton(screen, text, n, color):
    font.init()

    screen_text, width_text, height_text=text_to_screen(text,color)

    width_screen = screen.get_width()
    height_screen = screen.get_height()

    mouse = pygame.mouse.get_pos()

    if width_screen/2-5*width_text/8 <= mouse[0] <= width_screen/2+5*width_text/8 and height_screen/1.5-(80-(n-1)*60) <= mouse[1] <= height_screen/1.5-(80-(n-1)*60)+height_text+4: 
        pygame.draw.rect(screen,color_light,[width_screen/2-5*width_text/8,height_screen/1.5-(80-(n-1)*60)-1,5*width_text/4,height_text+4]) 
            
    else: 
        pygame.draw.rect(screen,color_dark,[width_screen/2-5*width_text/8,height_screen/1.5-(80-(n-1)*60)-1,5*width_text/4,height_text+4]) 
        
    screen.blit(screen_text , (width_screen/2-width_text/2,height_screen/1.5-(80-(n-1)*60)))

def input(screen):
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.   
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def antibuton(screen, text, n,color):
    font.init()

    screen_text, width_text, height_text=text_to_screen(text,color)

    width_screen = screen.get_width()
    height_screen = screen.get_height()

    pygame.draw.rect(screen,color_dark,[width_screen/2-5*width_text/8,height_screen/1.5-(80-(n-1)*60)-1,5*width_text/4,height_text+4]) 
        
    screen.blit(screen_text , (width_screen/2-width_text/2,height_screen/1.5-(80-(n-1)*60)))

#Fonction principale

def main():

    pygame.init()
     
    screen = pygame.display.set_mode(res) 
    fond = pygame.image.load("menu_2048.png").convert()
    screen.blit(fond, (0,0))

    pygame.display.update()

    width_screen = screen.get_width() 
    height_screen = screen.get_height() 
    
    while True: 
        
        for ev in pygame.event.get(): 
            
            if ev.type == pygame.QUIT: 
                pygame.quit() 
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                color=white
                screen_text, width_text, height_text=text_to_screen("jouer",color)
                if width_screen/2-5*width_text/8 <= mouse[0] <= width_screen/2+5*width_text/8 and height_screen/1.5-(80-(1-1)*60) <= mouse[1] <= height_screen/1.5-(80-(1-1)*60)+height_text+4 :
                    play()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                color=white
                screen_text, width_text, height_text=text_to_screen("quitter",color)
                if width_screen/2-5*width_text/8 <= mouse[0] <= width_screen/2+5*width_text/8 and height_screen/1.5-(80-(3-1)*60) <= mouse[1] <= height_screen/1.5-(80-(3-1)*60)+height_text+4 :
                    pygame.quit() 
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                color=white
                screen_text, width_text, height_text=text_to_screen("options",color)
                if width_screen/2-5*width_text/8 <= mouse[0] <= width_screen/2+5*width_text/8 and height_screen/1.5-(80-(2-1)*60) <= mouse[1] <= height_screen/1.5-(80-(2-1)*60)+height_text+4 :
                    options()
                    
        
        mouse = pygame.mouse.get_pos()

        buton(screen, "jouer", 1, white)
        buton(screen, "options", 2, white)
        buton(screen, "quitter", 3, white)
        
        pygame.display.update()

def options():
    pygame.init()
  
    screen = pygame.display.set_mode(res) 
    fond = pygame.image.load("menu_2048.png").convert()
    screen.blit(fond, (0,0))

    pygame.display.update()

    width_screen = screen.get_width() 
    height_screen = screen.get_height()

    smallfont = pygame.font.SysFont('Corbel',35)
    screen_text = smallfont.render("Taille de la grille : " , True , white)

    width_text = pygame.Surface.get_width(screen_text)
    height_text = pygame.Surface.get_height(screen_text)

    screen.blit(screen_text , (width_screen/2-5*width_text/5,height_screen/1.5-40-80))
    
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(width_screen/2,height_screen/1.5-40-80, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
  
    while not done: 
      
        for ev in pygame.event.get(): 
          
            if ev.type == pygame.QUIT: 
                pygame.quit()
        
            if ev.type == pygame.MOUSEBUTTONDOWN: 
                color=white
                screen_text, width_text, height_text=text_to_screen("quitter",color)
                if width_screen/2-5*width_text/8 <= mouse[0] <= width_screen/2+5*width_text/8 and height_screen/1.5-(80-(3-1)*60) <= mouse[1] <= height_screen/1.5-(80-(3-1)*60)+height_text+4 : 
                    main()
            
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(ev.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if ev.type == pygame.KEYDOWN:
                if active:
                    if ev.key == pygame.K_RETURN:
                        grid_size=int(text)
                        print(grid_size)
                    elif ev.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += ev.unicode
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(40, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+15, input_box.y+6))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
    
        mouse = pygame.mouse.get_pos()

        buton(screen, "Thème du jeu", 2, white)
        buton(screen, "Retour", 3, white)

        pygame.display.update()

def play():
    pygame.display.init()
     
    screen = pygame.display.set_mode(res) 

    pygame.draw.rect(screen,color_dark,[0,0,720,720]) 
    screen.blit(screen, (0, 0))

    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    screen.fill((30, 30, 30))
    # Render the current text.
    txt_surface = font.render("blabla", True, color)
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width()+10)

    input_box = pygame.Rect(100, 100, 140, 32)
    input_box.w = width
    # Blit the text.
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(30)


    pygame.display.update()

main()