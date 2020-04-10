#!/usr/bin/env python3
########################################################################
# Filename    : Tank_partie01.py
# Description : création jeux TANK avec Pygame - Partie 01
# auther      : papsdroid.fr
# modification: 2020/04/09
########################################################################

import pygame                   # PYGAME package
from pygame.locals import *     # PYGAME constant & functions
from sys import exit            # exit script 

class Game():
    """
    classe principale du jeux
    """

    def __init__(self, size_factor_X=18, size_factor_Y=12):
        """
        constructeur de la classe
        size_factor_X et size_factor_Y représentent la taille du plateau de jeux en nombre de tuiles 64*64 pixels
        """
    
        self.size_X, self.size_Y = 64,64                                      # taille des tuiles 64*64 pixels
        self.background_image_filename = 'Media/Ground_Tile_01_A_64x64.png'   # image backgound
        self.tank_image_filename = 'Media/Hull_02_64x64.png'                  # image tank
        
        self.size_factor_X, self.size_factor_Y = size_factor_X, size_factor_Y # taille de la fenêtre en nombre de tuiles
        #taille de l'écran basé sur le nb de tuiles, couleurs 32bits

        pygame.init()                                                         # initialisation Pygame
        self.screen = pygame.display.set_mode((self.size_X*self.size_factor_X, self.size_Y*self.size_factor_Y),0,32)
        pygame.display.set_caption("TANK - Pygame Tutorial PARTIE 01")                  # titre
        self.background = pygame.image.load(self.background_image_filename).convert()   # tuile pour le background
        self.tank_tile = pygame.image.load(self.tank_image_filename).convert_alpha()    # tuile pour le tank

    def loop(self):
        """
        boucle de lecture infinie événementielles du jeux
        """
        while True:
            #lecture des événements Pygame 
            for event in pygame.event.get():  
                if event.type == QUIT:  # evènement click sur fermeture de fenêtre
                    self.destroy()      # dans ce cas on appelle le destructeur de la classe           

            #affichage répété de la tuile de background en parcourant la fenêtre par pas de la taille des tuiles: 
            for x in range(0, self.size_X*self.size_factor_X, self.size_X):
                for y in range(0, self.size_Y*self.size_factor_Y, self.size_Y):
                    self.screen.blit(self.background,(x,y))  # tuile "background" en position (x,y)

            #affichage du tank positionné par la souris
            x,y = pygame.mouse.get_pos()             # récupère la position de la souris
            x-= self.tank_tile.get_width() / 2       # recadrage sur le milieu du tank 
            y-= self.tank_tile.get_height() / 2         
            self.screen.blit(self.tank_tile, (x,y))  # tuile tank en position (x,y)

            pygame.display.update()                  # rafraîchi l'écran


    def destroy(self):
        """
        destructeur de la classe
        """
        print('Bye!')
        pygame.quit() # ferme la fenêtre principale
        exit()        # termine tous les process en cours
            
if __name__ == '__main__':
    appl=Game()
    try:
        appl.loop()
    except KeyboardInterrupt:  # interruption clavier CTRL-C: appel à la méthode destroy() de appl.
        appl.destroy()
