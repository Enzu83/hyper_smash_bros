import pygame
from pygame import *
from pygame.locals import *
import sys
import random

from variables import *
from attack import *
from wall import *
from platforms import *
from player import *

#Constantes globales
res = (960,544)

white = (255,255,255) 
color_light = (170,170,170)
color_dark = (100,100,100)
black=(0,0,0)
red=(225,0,0)
blue=(0,0,225)
title_screen_color=(249,248,249)

global character_1
global character_2

pygame.init()

sound_menu = pygame.mixer.Sound("sound_effects\sound_menu.wav")
sound_buton = pygame.mixer.Sound("sound_effects\sound_buton.wav")
sound_back = pygame.mixer.Sound("sound_effects\sound_back.wav")
sound_start = pygame.mixer.Sound("sound_effects\sound_start.wav")

def text_to_screen(text,color):
    smallfont = pygame.font.SysFont('Corbel',35) 
    screen_text = smallfont.render(text , True , color)

    width_text = pygame.Surface.get_width(screen_text)
    height_text = pygame.Surface.get_height(screen_text)

    return screen_text, width_text, height_text

def buton():
    font.init()


def main():

	screen = pygame.display.set_mode(res)
	pygame.draw.rect(screen, black,[0,0,960,544])

	pygame.display.update()
	time.wait(10)
	pygame.mixer.music.load("Music\music_menu_b.wav")
	pygame.mixer.music.play()

	bouton=1
	continuer=1

	matrice=[[1,2],[3,4]]
	
	while continuer:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			if event.type == KEYDOWN:
				if event.key == K_RIGHT and (bouton == 1 or bouton == 3):
					sound_buton.play()
					bouton=matrice[bouton//2][1]
				if event.key == K_LEFT and (bouton == 2 or bouton == 4):
					sound_buton.play()
					bouton=matrice[-1+bouton//2][0]
				if event.key == K_UP and (bouton == 3 or bouton == 4):
					sound_buton.play()
					bouton=matrice[0][bouton-3]
				if event.key == K_DOWN and (bouton == 1 or bouton == 2):
					sound_buton.play()
					bouton=matrice[1][bouton-1]

				if event.key == K_RETURN:
					if bouton==1:
						sound_menu.play()
						selection_character_combat()
					if bouton==2:
						options()
					if bouton==3:
						selection_character_training()
					if bouton==4:
						pygame.mixer.music.stop()
						sound_back.play()
						time.wait(100)
						intro()
		coordonnées=[[50,34,405,221],[2*50+405,34,405,221],[50,2*34+221,405,221],[2*50+405,2*34+221,405,221]]
		color=[(222,35,4),(0,100,214),(0,141,45),(224,144,21)]
		text=["Smash","Options","Entraînement","Retour"]
		images=["interface\images\swords2.png","interface\images\option_e.png","interface\images\sandbag.png","interface\images\start.png"]
	
		for i in range(4):
			if i+1==bouton:
				pygame.draw.rect(screen,color[i],coordonnées[i])
				smallfont = pygame.font.SysFont('Source Sans Pro SemiBold',80) 
				screen_text = smallfont.render(text[i] , True , white)
				width_text = pygame.Surface.get_width(screen_text)
				height_text = pygame.Surface.get_height(screen_text)

				image= pygame.image.load(images[i]).convert_alpha()

				if bouton==1:
					screen.blit(screen_text, (coordonnées[i][0]+coordonnées[i][2]/2-2*width_text/3, coordonnées[i][1]+coordonnées[i][3]/2+4*height_text/6))
					screen.blit(image,(coordonnées[i][0]+coordonnées[i][2]/5+10,coordonnées[i][1]+10))
				elif bouton==2:
					screen.blit(screen_text, (coordonnées[i][0]+coordonnées[i][2]/2-width_text/3, coordonnées[i][1]+coordonnées[i][3]/2+4*height_text/6))
					screen.blit(image,(coordonnées[i][0]+2*coordonnées[i][2]/5,coordonnées[i][1]+10))
				elif bouton==3:
					screen.blit(screen_text, (coordonnées[i][0]+coordonnées[i][2]/2-width_text/2, coordonnées[i][1]+coordonnées[i][3]/2+4*height_text/6+10))
					screen.blit(image,(coordonnées[i][0]+2*coordonnées[i][2]/5+10,coordonnées[i][1]+15))
				elif bouton==4:
					screen.blit(screen_text, (coordonnées[i][0]+coordonnées[i][2]/2-width_text/3, coordonnées[i][1]+coordonnées[i][3]/2+4*height_text/6))
					screen.blit(image,(coordonnées[i][0]+2*coordonnées[i][2]/5+10,coordonnées[i][1]+25))
				
			else:
				pygame.draw.rect(screen,color_dark,coordonnées[i])
				smallfont = pygame.font.SysFont('Corbel',60) 
				screen_text = smallfont.render(text[i] , True , color[i])
				width_text = pygame.Surface.get_width(screen_text)
				height_text = pygame.Surface.get_height(screen_text)
				screen.blit(screen_text, (coordonnées[i][0]+coordonnées[i][2]/2-width_text/2, coordonnées[i][1]+coordonnées[i][3]/2-height_text/2))

		logo_centre= pygame.image.load("interface\images\logo_centre_"+str(bouton)+str(bouton)+".png").convert_alpha()
		screen.blit(logo_centre,(355,148))

		pygame.display.update()

def menu_principal():
	res = (960,544)

	title_screen_color=(249,248,249)


#Ouverture de la fenêtre Pygame
	screen = pygame.display.set_mode(res)
	pygame.draw.rect(screen,title_screen_color,[0,0,960,544])
#Chargement et collage du fond


	title_screen = pygame.image.load("interface\images\ecran_titre.jpg").convert()
	screen.blit(title_screen, (180,40))

	up1= pygame.image.load("interface\ecran_titre_dessus_part1.png").convert_alpha()
	screen.blit(up1,(0,0))
	up2= pygame.image.load("interface\ecran_titre_dessus_part2.png").convert_alpha()
	screen.blit(up2,(0,0))

def intro():
	pygame.init()
	pygame.display.set_caption("Hyper Smash Bros.")

	screen = pygame.display.set_mode(res)
	pygame.draw.rect(screen,title_screen_color,[0,0,960,544])

	icon=pygame.image.load("icon.png").convert_alpha()
	pygame.display.set_icon(icon)

	up1= pygame.image.load("interface\ecran_titre_dessus_part1.png").convert_alpha()

	for i in range(101):
		pygame.draw.rect(screen,title_screen_color,[0,0,960,544])
		screen.blit(up1,(47-0.47*i,-544+5.44*i))
		pygame.display.flip()
		time.wait(3)
	
	up2= pygame.image.load("interface\ecran_titre_dessus_part2.png").convert_alpha()

	for i in range(101):
		pygame.draw.rect(screen,title_screen_color,[0,0,960,544])
		screen.blit(up2,(-1024+10.24*i,-86+0.86*i))
		screen.blit(up1,(0,0))
		pygame.display.flip()
		time.wait(3)
	
	
	#Ouverture de la fenêtre Pygame
	screen = pygame.display.set_mode(res)
	pygame.draw.rect(screen,title_screen_color,[0,0,960,544])
	#Chargement et collage du fond


	title_screen = pygame.image.load("interface\images\ecran_titre.jpg").convert()
	screen.blit(title_screen, (180,40))


	up1= pygame.image.load("interface\ecran_titre_dessus_part1.png").convert_alpha()
	screen.blit(up1,(0,0))
	up2= pygame.image.load("interface\ecran_titre_dessus_part2.png").convert_alpha()
	screen.blit(up2,(0,0))

	#Rafraîchissement de l'écran

	pygame.display.flip()

	time.wait(300)

	continuer=1

	while continuer:

		for i in range(0,249,4):
			menu_principal()
			up_i= pygame.image.load("interface\press_any_buton\press_any_buton_" + str(i) + ".png").convert_alpha()
			screen.blit(up_i,(269,414))
			time.wait(3)
			display.flip()
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					pygame.quit()      #On arrête la boucle
				if event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
					sound_menu.play()
					main()

		for i in range(248,-1,-4):
			menu_principal()
			up_i= pygame.image.load("interface\press_any_buton\press_any_buton_" + str(i) + ".png").convert_alpha()
			screen.blit(up_i,(269,414))
			time.wait(3)
			display.flip()
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					pygame.quit()      #On arrête la boucle
				if event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:

					sound_menu.play()
					main()


def selection_character_combat():
	global character_1
	global character_2
	screen = pygame.display.set_mode(res)
	pygame.draw.rect(screen,black,[0,0,960,544])

	pygame.display.update()
	time.wait(10)

	character_1=1
	character_2=2
	continuer=1

	matrice=[[1,2,3,4],[5,6,7,8]]
	color_selection=[[color_dark,red],[color_dark,blue]]
	selection_1=0
	selection_2=0


	while continuer:
		for event in pygame.event.get():
			screen = pygame.display.set_mode(res)
			pygame.draw.rect(screen,black,[0,0,960,544])
			if event.type == QUIT:
				pygame.quit()
			#Character 1
			if event.type == KEYDOWN:
				if event.key == K_RIGHT and selection_1==0:
					if character_1 in [1,2,3]:
						sound_buton.play()
						character_1=matrice[0][character_1]
					if character_1 in [5,6,7]:
						sound_buton.play()
						character_1=matrice[1][character_1-4]
				if event.key == K_LEFT and selection_1==0:
					if character_1 in [2,3,4]:
						sound_buton.play()
						character_1=matrice[0][character_1-2]
					if character_1 in [6,7,8]:
						sound_buton.play()
						character_1=matrice[1][character_1-6]
				if event.key == K_UP and character_1 in matrice[1] and selection_1==0:
					sound_buton.play()
					character_1=matrice[0][character_1-5]
				if event.key == K_DOWN and character_1 in matrice[0] and selection_1==0:
					sound_buton.play()
					character_1=matrice[1][character_1-1]
				if event.key == K_RETURN and selection_1==0:
					sound_menu.play()
					selection_1=1
				if event.key == K_RETURN and selection_1==1 and selection_2==1:
					jouer()
				if event.key == K_RCTRL and selection_1==1:
					sound_back.play()
					selection_1=0

				#Character 2

				if event.key == K_d and selection_2==0:
					if character_2 in [1,2,3]:
						sound_buton.play()
						character_2=matrice[0][character_2]
					if character_2 in [5,6,7]:
						sound_buton.play()
						character_2=matrice[1][character_2-4]
				if event.key == K_q and selection_2==0:
					if character_2 in [2,3,4]:
						sound_buton.play()
						character_2=matrice[0][character_2-2]
					if character_2 in [6,7,8]:
						sound_buton.play()
						character_2=matrice[1][character_2-6]
				if event.key == K_z and character_2 in matrice[1] and selection_2==0:
					sound_buton.play()
					character_2=matrice[0][character_2-5]
				if event.key == K_s and character_2 in matrice[0] and selection_2==0:
					sound_buton.play()
					character_2=matrice[1][character_2-1]
				if event.key == K_a and selection_2==0:
					sound_menu.play()
					selection_2=1
				if event.key == K_r and selection_2==1:
					sound_back.play()
					selection_2=0

		coordonnées=[[160,72],[160+180,72],[160+2*180,72],[160+3*180,72],[160,72+120],[160+180,72+120],[160+2*180,72+120],[160+3*180,72+120]]
		text=["Kirby","Pikachu","Marth","Hal","Goku","Pirate","The Cube","Aléatoire"]
		images=["interface\images\Kirby.png","interface\images\Pikachu.png","interface\images\Marth.png","interface\images\Hal.png","interface\images\Goku.png","interface\images\Pirate.png","interface\images\Cube.png","interface\images\Aléatoire.png"]
		images_selection=["interface\images\Kirby2.png","interface\images\Pikachu2.png","interface\images\Marth2.png","interface\images\Hal2.png","interface\images\Goku2.png","interface\images\Pirate2.png","interface\images\Cube2.png","images\Aléatoire2.png"]
		

		for i in range(1,9):
			if i==character_1 and character_1 in [1,2,3,4]:
				pygame.draw.rect(screen,red,[160+(character_1-1)*180-10,72-10,80,80])
			elif i==character_1 and character_1 in [5,6,7,8]:
				pygame.draw.rect(screen,red,[160+(character_1-5)*180-10,72+120-10,80,80])
			elif i==character_2 and character_2 in [1,2,3,4]:
				pygame.draw.rect(screen,blue,[160+(character_2-1)*180-10,72-10,80,80])
			elif i==character_2 and character_2 in [5,6,7,8]:
				pygame.draw.rect(screen,blue,[160+(character_2-5)*180-10,72+120-10,80,80])

		for i in range(1,9):
			if i in [1,2,3,4]:
				pygame.draw.rect(screen,color_dark,[160+(i-1)*180-5,72-5,70,70])
			else:
				pygame.draw.rect(screen,color_dark,[160+(i-5)*180-5,72+120-5,70,70])
		
		for j in range(1,9):
			smallfont = pygame.font.SysFont('Papyrus',20) 
			screen_text = smallfont.render(text[j-1] , True , white)

			width_text = pygame.Surface.get_width(screen_text)
			height_text = pygame.Surface.get_height(screen_text)

			if j in [1,2,3,4]:
				screen.blit(screen_text, (160+(j-1)*180-5+70/2-width_text/2,72-12+70+height_text/3))
			else:
				screen.blit(screen_text, (160+(j-5)*180-5+70/2-width_text/2,72+120-12+70+height_text/3))
		
		up_1= pygame.image.load(images[0]).convert_alpha()
		screen.blit(up_1,(162+12-5,74+27-5))

		up_2= pygame.image.load(images[1]).convert_alpha()
		screen.blit(up_2,(162+180+5-5,74+17-5))

		up_3= pygame.image.load(images[2]).convert_alpha()
		screen.blit(up_3,(162+2*180+8,74-5))

		up_4= pygame.image.load(images[3]).convert_alpha()
		screen.blit(up_4,(162+3*180-6,74+14))

		up_5= pygame.image.load(images[4]).convert_alpha()
		screen.blit(up_5,(162-4,74+120+5))

		up_6= pygame.image.load(images[5]).convert_alpha()
		#If pirate
		#screen.blit(up_6,(162+180-9,74+120+7))

		#If pirate2 ou 3
		screen.blit(up_6,(162+180,74+120-4))

		up_7= pygame.image.load(images[6]).convert_alpha()
		screen.blit(up_7,(162+2*180+2,74+120+12))

		up_8= pygame.image.load(images[7]).convert_alpha()
		screen.blit(up_8,(162+3*180+7,74+120+3))

		pygame.draw.rect(screen,color_selection[0][selection_1],[20,302,450,172])
		pygame.draw.rect(screen,color_selection[1][selection_2],[20+480,302,450,172])

		smallfont = pygame.font.SysFont('Source Sans Pro SemiBold',40) 
		screen_text = smallfont.render("Joueur 1" , True , white)
		width_text = pygame.Surface.get_width(screen_text)
		height_text = pygame.Surface.get_height(screen_text)
		screen.blit(screen_text, (20+450/2-width_text/2-5,302+172+35-height_text/2))

		screen_text = smallfont.render("Joueur 2" , True , white)
		width_text = pygame.Surface.get_width(screen_text)
		height_text = pygame.Surface.get_height(screen_text)
		screen.blit(screen_text, (20+480+450/2-width_text/2+10,302+172+35-height_text/2))

		pixels_selection=[[5,25],[0,0],[0,-38],[0,0],[-5,-15],[0,-33],[0,0],[0,-20]]

		if selection_1==1:
			up=pygame.image.load(images_selection[character_1-1]).convert_alpha()
			screen.blit(up,(50+pixels_selection[character_1-1][0],355+pixels_selection[character_1-1][1]))

			smallfont = pygame.font.SysFont('Source Sans Pro SemiBold',80) 
			screen_text = smallfont.render(text[character_1-1] , True , white)
			width_text = pygame.Surface.get_width(screen_text)
			height_text = pygame.Surface.get_height(screen_text)
			screen.blit(screen_text, (20+450/2-width_text/5,302+172/2-height_text/2))
		
		if selection_2==1:
			up=pygame.image.load(images_selection[character_2-1]).convert_alpha()
			screen.blit(up,(50+480+pixels_selection[character_2-1][0],355+pixels_selection[character_2-1][1]))

			smallfont = pygame.font.SysFont('Source Sans Pro SemiBold',80) 
			screen_text = smallfont.render(text[character_2-1] , True , white)
			width_text = pygame.Surface.get_width(screen_text)
			height_text = pygame.Surface.get_height(screen_text)
			screen.blit(screen_text, (480+20+450/2-width_text/5,302+172/2-height_text/2))


		if selection_1==1 and selection_2==1:
			up=pygame.image.load("interface\images\start.png").convert_alpha()
			screen.blit(up,(100,50))

		pygame.display.update()


def selection_character_training():
	global character_1
	global character_2

	screen = pygame.display.set_mode(res)
	pygame.draw.rect(screen,black,[0,0,960,544])

	pygame.display.update()
	time.wait(10)

	character_1=1
	continuer=1

	matrice=[[1,2,3,4],[5,6,7,8]]
	color_selection=[[color_dark,red],[color_dark,blue]]
	selection_1=0

	while continuer:
		for event in pygame.event.get():
			screen = pygame.display.set_mode(res)
			pygame.draw.rect(screen,black,[0,0,960,544])
			if event.type == QUIT:
				pygame.quit()
			#Character 1
			if event.type == KEYDOWN:
				if event.key == K_RIGHT and selection_1==0:
					if character_1 in [1,2,3]:
						sound_buton.play()
						character_1=matrice[0][character_1]
					if character_1 in [5,6,7]:
						sound_buton.play()
						character_1=matrice[1][character_1-4]
				if event.key == K_LEFT and selection_1==0:
					if character_1 in [2,3,4]:
						sound_buton.play()
						character_1=matrice[0][character_1-2]
					if character_1 in [6,7,8]:
						sound_buton.play()
						character_1=matrice[1][character_1-6]
				if event.key == K_UP and character_1 in matrice[1] and selection_1==0:
					sound_buton.play()
					character_1=matrice[0][character_1-5]
				if event.key == K_DOWN and character_1 in matrice[0] and selection_1==0:
					sound_buton.play()
					character_1=matrice[1][character_1-1]
				if event.key == K_RETURN and selection_1==0:
					sound_menu.play()
					selection_1=1
				if event.key == K_RCTRL and selection_1==1:
					sound_back.play()
					selection_1=0

				
		coordonnées=[[160,72],[160+180,72],[160+2*180,72],[160+3*180,72],[160,72+120],[160+180,72+120],[160+2*180,72+120],[160+3*180,72+120]]
		text=["Kirby","Pikachu","Marth","Hal","Goku","Pirate","The Cube","Aléatoire"]
		images=["interface\images\Kirby.png","interface\images\Pikachu.png","interface\images\Marth.png","interface\images\Hal.png","interface\images\Goku.png","interface\images\Pirate.png","interface\images\Cube.png","interface\images\Aléatoire.png"]
		images_selection=["interface\images\Kirby2.png","interface\images\Pikachu2.png","interface\images\Marth2.png","interface\images\Hal2.png","interface\images\Goku2.png","interface\images\Pirate2.png","interface\images\Cube2.png","interface\images\Aléatoire2.png"]
		

		for i in range(1,9):
			if i==character_1 and character_1 in [1,2,3,4]:
				pygame.draw.rect(screen,red,[160+(character_1-1)*180-10,72-10,80,80])
			elif i==character_1 and character_1 in [5,6,7,8]:
				pygame.draw.rect(screen,red,[160+(character_1-5)*180-10,72+120-10,80,80])

		for i in range(1,9):
			if i in [1,2,3,4]:
				pygame.draw.rect(screen,color_dark,[160+(i-1)*180-5,72-5,70,70])
			else:
				pygame.draw.rect(screen,color_dark,[160+(i-5)*180-5,72+120-5,70,70])
		
		for j in range(1,9):
			smallfont = pygame.font.SysFont('Papyrus',20) 
			screen_text = smallfont.render(text[j-1] , True , white)

			width_text = pygame.Surface.get_width(screen_text)
			height_text = pygame.Surface.get_height(screen_text)

			if j in [1,2,3,4]:
				screen.blit(screen_text, (160+(j-1)*180-5+70/2-width_text/2,72-12+70+height_text/3))
			else:
				screen.blit(screen_text, (160+(j-5)*180-5+70/2-width_text/2,72+120-12+70+height_text/3))
		
		up_1= pygame.image.load(images[0]).convert_alpha()
		screen.blit(up_1,(162+12-5,74+27-5))

		up_2= pygame.image.load(images[1]).convert_alpha()
		screen.blit(up_2,(162+180+5-5,74+17-5))

		up_3= pygame.image.load(images[2]).convert_alpha()
		screen.blit(up_3,(162+2*180+8,74-5))

		up_4= pygame.image.load(images[3]).convert_alpha()
		screen.blit(up_4,(162+3*180-6,74+14))

		up_5= pygame.image.load(images[4]).convert_alpha()
		screen.blit(up_5,(162-4,74+120+5))

		up_6= pygame.image.load(images[5]).convert_alpha()
		#If pirate
		#screen.blit(up_6,(162+180-9,74+120+7))

		#If pirate2 ou 3
		screen.blit(up_6,(162+180,74+120-4))

		up_7= pygame.image.load(images[6]).convert_alpha()
		screen.blit(up_7,(162+2*180+2,74+120+12))

		up_8= pygame.image.load(images[7]).convert_alpha()
		screen.blit(up_8,(162+3*180+7,74+120+3))

		pygame.draw.rect(screen,color_selection[0][selection_1],[20+240,302,450,172])


		smallfont = pygame.font.SysFont('Source Sans Pro SemiBold',40) 
		screen_text = smallfont.render("Joueur 1" , True , white)
		width_text = pygame.Surface.get_width(screen_text)
		height_text = pygame.Surface.get_height(screen_text)
		screen.blit(screen_text, (20+450-width_text/2-5,302+172+35-height_text/2))

		pixels_selection=[[5,25],[0,0],[0,-38],[0,0],[-5,-15],[0,-33],[0,0],[0,-20]]

		if selection_1==1:
			up=pygame.image.load(images_selection[character_1-1]).convert_alpha()
			screen.blit(up,(50+240+pixels_selection[character_1-1][0],355+pixels_selection[character_1-1][1]))

			smallfont = pygame.font.SysFont('Source Sans Pro SemiBold',80) 
			screen_text = smallfont.render(text[character_1-1] , True , white)
			width_text = pygame.Surface.get_width(screen_text)
			height_text = pygame.Surface.get_height(screen_text)
			screen.blit(screen_text, (20+240+450/2-width_text/5,302+172/2-height_text/2))
		
			up=pygame.image.load("interface\images\start.png").convert_alpha()
			screen.blit(up,(100,50))

		pygame.display.update()


def random_character():
	a=random.randint(1,7)
	return a

def options():
	pygame.quit()

def jouer():
	global character_1
	global character_2
		# Initiate the game
	clock = pygame.time.Clock()
	pygame.init()  # Initialize the game
	pygame.display.set_caption('Hyper Smash Bros.')
	pygame.display.set_icon("icon.png")

	# Create instances
	text=['Kirby','Pikachu','Marth','Hal','Goku','Pirate','The Cube']
	if character_1==8:
		character_1=random_character()
	if character_2==8:
		character_2=random_character()
	player1 = Player((256, 20), 1, text[character_1-1])
	player2 = Player((672, 20), 2, text[character_2-1])
	walls.add(Wall(224, window_size[1] - 160))
	platforms.add(Platform(322, 306))
	platforms.add(Platform(558, 306))
	players.append(player1)
	players.append(player2)


	# Variables
	space = 0
	pause = 0
	key_k = 0
	percent_index = 0
	f11 = 0

	# Game loop
	if __name__ == "__main__":
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:  # Close the window
					pygame.quit()
					sys.exit()

			screen.fill((98, 198, 222))  # Refresh screen
			screen.blit(background, (0, 0))

			if pause == 0:
				for wall in walls:
					screen.blit(wall.image, (wall.x, wall.y))
				for platform in platforms:
					screen.blit(platform.image, (platform.x, platform.y))
				for cloud in clouds:
					cloud.update()
				for attack in attacks:
					attack.update()
				for explosion in explosions:
					explosion.update()

				player1.update()
				player2.update()
				#pygame.draw.rect(screen,(0,255,0),player1.rect)
				#pygame.draw.rect(screen,(0,255,0),player2.rect)
				for ledge in ledges:
					ledge.update_ledge_timer()

					if not (ledge.player_to_ledge(player2)):
						ledge.update_ledge_actions(player1)
					if not (ledge.player_to_ledge(player1)):
						ledge.update_ledge_actions(player2)

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

			# Player 1 percent
			screen.blit(pygame.image.load(
				'sprites/percent_hud.png').convert_alpha(), (226, 450))
			player_image = pygame.image.load(
				'./icon/icon_hud/icon_' + str(player1.character) + '.png').convert_alpha()
			screen.blit(player_image, (46-player_image.get_width() /
						2+226, 46-player_image.get_height()/2+450))
			percent = str(player1.percent)
			percent_index = 0
			for i in range(len(percent)):
				screen.blit(font_percent[int(percent[i])],
							(379-30*(len(percent)-i), 466))
			screen.blit(font_percent[10], (387, 466))

			# Player 2 percent
			screen.blit(pygame.image.load('sprites/percent_hud2.png'), (542, 450))
			player_image = pygame.image.load(
				'./icon/icon_hud/icon_' + str(player2.character) + '.png').convert_alpha()
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

intro()
