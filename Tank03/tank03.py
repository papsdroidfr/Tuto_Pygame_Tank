#!/usr/bin/env python3
########################################################################
# Description : création jeux TANK avec Pygame - Partie 3
# auther      : papsdroid.fr
# modification: 2020/04/10
########################################################################

import pygame                     # PYGAME package
from pygame.locals import *       # PYGAME constant & functions
from sys import exit              # exit script
from PIL import Image             # bilbiothèque pour traitement d'image
from class_Terrain import Terrain  # classe Terrain() du fichier tank_Terrain.py
from class_Tank import Tank        # classe Tank() du fichier tank_Tank.py              

class Game():
    """
    classe principale du jeux
    """

    def __init__(self, size_spriteX=64, size_spriteY=64, nb_spritesX=18, nb_spritesY=12):
        """
        constructeur de la classe
            size_spriteX=64, size_spriteY=64 représentent la taille d'une tuile (64*64 pixels par défaut)
            nb_spritesX=18, nb_spritesY=12 représentent la taille du plateau de jeux en nombre de tuiles (18*12 tuiles par défaut) 
        """
        print('démarrage jeux Tank')
        self.terrain = Terrain(map_filenames=['Map/tank_background.map', # terrain de jeux avec maps
                                              'Map/tank_vegetaux.map',
                                              'Map/tank_fondations.map',
                                              'Map/tank_fondations2.map',
                                              'Map/tank_flags1.map',
                                              'Map/tank_flags2.map',
                                              'Map/tank_bords.map',
                                              ])  
        self.tanks = []                                  # liste des tanks
        #premier tank
        self.tanks.append(Tank(self.terrain, 'Tank1',
                               l_img_name=['Media/Tank/Tank1/Markup_128x128.png',
                                'Media/Tank/Tank1/Hull_02_128x128.png',
                                'Media/Tank/Tank1/Gun_05_A_128x128.png'],
                               human=False,
                               pos=(2*self.terrain.size_spriteX, 2*self.terrain.size_spriteY),
                               nb_rotates=64,
                               l_rotation=[3,3,7]
                            ))   
        #second tank
        self.tanks.append(Tank(self.terrain, 'Tank2',
                               l_img_name=['Media/Tank/Tank2/Markup_128x128.png',
                                'Media/Tank/Tank2/Hull_02_128x128.png',
                                'Media/Tank/Tank2/Gun_05_A_128x128.png'],
                               human=True,
                               pos=(0,0),
                               nb_rotates=64,
                               l_rotation=[0,0,4]
                            ))   
    def loop(self):
        """
        boucle infinie  du jeux: lecture des événements et dessin
        """
        while True:
            #lecture des événements Pygame 
            for event in pygame.event.get():  
                if event.type == QUIT:  # evènement click sur fermeture de fenêtre
                    self.destroy()      # dans ce cas on appelle le destructeur de la classe           

            self.terrain.dessine()      #dessin du terrain
            for tank in self.tanks:     #dessin des tanks
                tank.bouge()
                tank.dessine()

            pygame.display.update()     # rafraîchi l'écran


    def destroy(self):
        """
        destructeur de la classe
        """
        print('Bye!')
        pygame.quit() # ferme la fenêtre principale
        exit()        # termine tous les process en cours

# Programme  principal
#----------------------------------------------------------------
if __name__ == '__main__':
    appl=Game() #instanciation d'un objet Game(): le constructeur lance immédiatement le jeux
    try:
        appl.loop()
    except KeyboardInterrupt:  # interruption clavier CTRL-C: appel à la méthode destroy() de appl.
        appl.destroy()
