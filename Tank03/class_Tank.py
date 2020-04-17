#!/usr/bin/env python3
########################################################################
# Description : création jeux TANK avec Pygame - Partie 3
# auther      : papsdroid.fr
# modification: 2020/04/10
########################################################################

import pygame                   # PYGAME package
from pygame.locals import *     # PYGAME constant & functions
from PIL import Image           # bilbiothèque pour traitement d'image
from class_Terrain import Terrain  # classe Terrain() du fichier tank_Terrain.py


class Tank():
    """
    classe décrivant un tank
    """

    def __init__(self, terrain, name, l_img_name, l_detla_pos, human=False,
                 pos=(0,0), nb_rotates=16, l_rotation=[0,0,0]):
        """
        constructeur de la classe
            terrain    : le terrain sur lequel évolue le tank
            name       : nom du tank
            l_img_name : liste des noms des images du tank devant être dessinées dans l'ordre de la liste
            l_delta_pos: delta (dx,dy) des positions à opérer sur les images du tank
            human: True si joué par un humain, False si joué par la machine
            pos:  position (x,y) du tank (coin haut gauche)
            nb_rotates: nombre de rotations à pré-générer  (rotations par pas de 2pi/nb_rotations)
            l_rotation: rotation de chaque image (index de 0 à nb_rotates-1)
        """
        print('--> création du tank', name)
        self.name = name
        self.nb_rotates = nb_rotates
        # génération de liste des rotations de chaque image dans l_img_name
        self.l_img_rotated = self.rotates_l_img(l_img_name)
        print('   ...', len(self.l_img_rotated), '*', len(self.l_img_rotated[0]),'rotations générées')
        self.terrain = terrain    # terrain sur lequel évolue le tank
        self.human = human        # True: joué par un humain
        self.size = self.l_img_rotated[0][0].get_width()  # taille des images en nb de pixels d'un côté du carré
        self.half_size = int(self.size/2)         # 1/2 taille des images en nb de pixels d'un côté du carré
        self.pos = pos                            # position du tank (2-tuple, coin haut gauche)
        self.l_rotation=l_rotation                # liste des rotations de chaque image (index de 0 à nb_rotates-1)
                                      
    def bouge(self):
        """
        méthode pour faire bouger le tank
        """
        if self.human:
            #positionnenemnt du tank joué par un humain avec la souris
            x,y = pygame.mouse.get_pos() # récupère la position de la souris
            self.pos = (x-self.half_size, y)                    # postionne le tank aligné sur la souris, en bas.
            # rotation du coprs du tank selon position verticale de la souris
            self.l_rotation[1] = (int)(self.nb_rotates*2*x/(self.terrain.nb_pixelsY))%self.nb_rotates   
            # rotation du canon en fonction de la position horizontale de la souris
            # la rotation du corps du tank doit être propagée à la rotation du canon
            self.l_rotation[2] = (self.l_rotation[1] + (int)(self.nb_rotates*2*y/(self.terrain.nb_pixelsX)))%self.nb_rotates  

    def dessine(self):
        """
        dessin du tank sur le terrain en position self.pos
        """
        #parcours des images du tank selon leur index respectifs de rotation
        for n in range(len(self.l_img_rotated)):
            self.terrain.screen.blit(self.l_img_rotated[n][self.l_rotation[n]], self.pos)

    def rotates_l_img(self, l_img_name):
        """
        génère une liste d'images avec rotations
            rotates_l_img[0] = liste des rotations de l'image l_img_name[0] 
            rotates_l_img[1] = liste des rotations de l'image l_img_name[1] 
            ...
            rotates_l_img[n] = liste des rotations de l'image l_img_name[n] 
        """

        #fonction interne qui génère une liste de rotation à partir d'une seule image
        def rotates_img(img_file, nb_rotates):
            """
            génère une liste d'images avec rotations
                rotates_img[0] = image originale sans rotation
                rotates_img[1] = image rotation 1 * 2pi/self.nb_rotates
                rotates_img[2] = image rotation 2 * 2pi/self.nb_rotates
                ...
                rotates_img[n] = image rotation n * 2pi/self.nb_rotates
            """
            angle = (float)(360.0/nb_rotates)  # angle de rotation = -2*pi/self.nb_rotates
            img= Image.open(img_file)          # image au format PIL
            return [ pygame.image.fromstring( img.rotate(n*angle).tobytes(), img.size, 'RGBA' )
                     for n in range(nb_rotates) ]

        return [ rotates_img(l_img_name[n], self.nb_rotates) for n in range(len(l_img_name)) ]




    
        
