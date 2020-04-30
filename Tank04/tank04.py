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

    def __init__(self, size_spriteX=64, size_spriteY=64, nb_spritesX=18, nb_spritesY=12, fps=30):
        """
        constructeur de la classe
            size_spriteX=64, size_spriteY=64 représentent la taille d'une tuile (64*64 pixels par défaut)
            nb_spritesX=18, nb_spritesY=12 représentent la taille du plateau de jeux en nombre de tuiles (18*12 tuiles par défaut)
            fps: nombre d'images max par secondes
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
        self.tanks = []  # liste des tanks
        

        #second tank joué au clavier
        self.tanks.append(Tank(self.terrain, 'Tank2',
                               l_img_name=['Media/Tank/Tank2/Markup_128x128.png',
                                'Media/Tank/Tank2/Hull_02_128x128.png',
                                'Media/Tank/Tank2/Gun_03_128x128.png'],
                               human=True,
                               pos=( (self.terrain.nb_spritesX-3.5) * self.terrain.size_spriteX,
                                     (self.terrain.nb_spritesY-3.5) * self.terrain.size_spriteY)
                            ))
        self.humanTank = self.tanks[0] #tank joué au clavier par un humain

        #autres tank joué par l'ordi
        #self.tanks.append(Tank(self.terrain, 'Tank1',
        #                       l_img_name=['Media/Tank/Tank1/Markup_128x128.png',
        #                        'Media/Tank/Tank1/Hull_02_128x128.png',
        #                        'Media/Tank/Tank1/Gun_03_128x128.png'],
        #                       human=False,
        #                       pos=(2*self.terrain.size_spriteX, 2*self.terrain.size_spriteY)
        #                    ))   


        self.timer = pygame.time.Clock()  # timer pour contrôler le FPS
        self.fps = fps                    # fps = 30 images par seconde
        
    def loop(self):
        """
        boucle infinie  du jeux: lecture des événements et dessin
        """
        while True:
            #lecture des événements Pygame 
            for event in pygame.event.get():  
                if event.type == QUIT:  # evènement click sur fermeture de fenêtre
                    self.destroy()      # dans ce cas on appelle le destructeur de la classe
                elif event.type == KEYDOWN: 
                    if (event.key==K_SPACE):  # activation du bouclier
                        self.humanTank.changes_shield()
                    elif (event.key==K_f):    # tir d'un obus
                        self.humanTank.fire()
                        
            self.timer.tick(self.fps)   #limite le fps
            
            self.terrain.dessine()      #dessin du terrain
            
            for tank in self.tanks:        # dessin des tanks et obus tirés
                tank.dessine()             # dessine le tank
                if tank.shell.countdown>0: # dessine l'obus s'il a été tiré
                    tank.shell.dessine()
                if tank.shell.explosion.booom: # dessine l'explosion de l'obus si activée
                    tank.shell.explosion.dessine()
                tank.bouge()            # fait bouger le tank et l'obus s'il est tiré

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
