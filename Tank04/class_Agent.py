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
import math


class Agent():
    """
    classe décrivant un agent se déplaçant  selon une direction et une vitesse sur un terrain
    """

    def __init__(self, terrain, name, l_img_name, pos=(0,0), nb_rotates=1,
                 v=0, vmax=0, accel=0, friction_force=0):
        """
        constructeur de la classe
            terrain    : le terrain sur lequel évolue l'agent
            name       : nom de l'agent
            l_img_name : liste des noms des images de l'agent devant être dessinées dans l'ordre de la liste
            pos:  position (x,y) de l'agent (coin haut gauche)
            nb_rotates: nombre de rotations à pré-générer  (rotations par pas de 2pi/nb_rotations)
            v=0, vmax=10, accel=0, friction_force=0: vitesse, accélération et force de frottement
        """
        print("--> création de l'agent", name)
        self.name = name
        self.l_img_name = l_img_name
        self.nb_rotates = nb_rotates
        self.init_rotation()  #rotation de chaque image initialisée à 0
        # génération de liste des rotations de chaque image dans l_img_name
        self.l_img_rotated, self.l_sin, self.l_cos = self.rotates_l_img(l_img_name)
        #print('   ...', len(self.l_img_rotated), '*', len(self.l_img_rotated[0]),'rotations générées')
        self.terrain = terrain    # terrain sur lequel évolue le tank
        self.size = self.l_img_rotated[0][0].get_width()  # taille des images en nb de pixels d'un agent
        self.half_size = int(self.size/2)         # 1/2 taille des images en nb de pixels
        self.quart_size = int(self.half_size/2)   # 1/4 taille des images en nb de pixels
        self.activates_all()                      # liste des éléments actifs affichés
        self.pos = pos                            # position de l'agent (2-tuple, coin haut gauche)
        self.v=v                                  # vitesse de l'agent, orienté dans la direction self.l_rotate[0])
        self.vMax = vmax                          # vitesse max de l'agent
        self.accel = accel                        # accélération de l'agent
        self.friction_force = friction_force      # accélération négative dues aux forces de frottements: ralenti l'agent si pas d'accélération
        self.timer = 0                            # timer interne à l'agent +1 à chaque fois qu'il bouge     
        

    def bouge(self):
        """
        méthode pour faire bouger l'agent selon acceleration, vitesse et orientation
        """
       
        # si pas d'accélération et vitesse non nule: la force de frottement fait ralentir le tank dans le sens de sa vitesse
        if (self.accel==0 and self.v!=0):
            self.accel = self.friction_force * ( (self.v>0) - (self.v<0) )
        # nouvelle vitesse, ne pouvant dépasser self.vMax en valeur absolue
        self.v += self.accel
        if abs(self.v) > self.vMax:
            self.v = ( (self.v>0) - (self.v<0) ) * self.vMax            
            
        #position modifiée selon vitesse de l'agent, sans déborder du cadre
        if self.v !=0 :
            x = self.pos[0] - self.v*self.l_sin[self.l_rotation[0]]
            y = self.pos[1] - self.v*self.l_cos[self.l_rotation[0]]
            if x+self.half_size < 0:
                x, self.v, self.accel = -self.half_size,0,0
            elif (x+self.half_size) > self.terrain.nb_pixelsX:
                x, self.v, self.accel = self.terrain.nb_pixelsX-self.half_size,0,0
            if y+self.half_size<0:
                y, self.v, self.accel = -self.half_size,0,0
            elif (y+self.half_size) > self.terrain.nb_pixelsY: 
                y, self.v, self.accel = self.terrain.nb_pixelsY-self.half_size,0,0
            self.pos = (x,y)

        self.timer += 1  # timer interne de l'agent incrémenté

    def activates_all(self):
        """
        active toutes les images
        """
        self.l_actif = [True]* len(self.l_img_name)

    def desactivates_all(self):
        """
        désactive toutes les images
        """
        self.l_actif = [False]* len(self.l_img_name)
        
    def init_rotation(self):
        """
        initialise toutes les rotations à 0
        """
        self.l_rotation = [0] * len(self.l_img_name)
        
    def rotates(self, add_rotation, id_elm=None):
        """
        gère la rotation des éléments dans la liste l_id_img
            si l_id_img = self.l_rotation: c'est l'agent en entier qui subit une rotation +add_rotation
            si l_id_img = un seul élément: seul cet élément va subir une rotation +add_rotation 
        """
        if id_elm==None:
            for n in range(len(self.l_rotation)): #rotation propagée à tous les éléments de la liste
                self.l_rotation[n]=(self.l_rotation[n] + add_rotation) % self.nb_rotates
        else:
            self.l_rotation[id_elm]=(self.l_rotation[id_elm] + add_rotation) % self.nb_rotates

    def orient(self, id_rotation, id_elm=None):
        """
        gère l'orientation des éléments dans la liste l_id_img
            si l_id_img = self.l_rotation: c'est l'agent en entier qui est orienté vers id_rotation
            si l_id_img = un seul élément: seul cet élément va être orienté
        """
        if id_elm==None:
            for n in range(len(self.l_rotation)): #rotation propagée à tous les éléments de la liste
                self.l_rotation[n] = id_rotation % self.nb_rotates
        else:
            self.l_rotation[id_elm] = id_rotation % self.nb_rotates
        
    def dessine(self):
        """
        dessin de l'agent sur le terrain en position self.pos
        """
        #parcours des images de l'agent selon leur index respectifs de rotation
        for n in range(len(self.l_actif)):
            if self.l_actif[n]:
                self.terrain.screen.blit(self.l_img_rotated[n][self.l_rotation[n]], self.pos)

        
    def rotates_l_img(self, l_img_name):
        """
        retourne 3 listes :
        Première liste retournée: liste d'images avec rotations
            rotates_l_img[0] = liste des rotations de l'image l_img_name[0] 
            rotates_l_img[1] = liste des rotations de l'image l_img_name[1] 
            ...
            rotates_l_img[n] = liste des rotations de l'image l_img_name[n]
        Seconde liste retournée: liste des sinus de chaque nb_rotates angles
        Troisième liste retournée: liste des cosinus de chaque nb_rotates angles
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

        return ( [ rotates_img(l_img_name[n], self.nb_rotates) for n in range(len(l_img_name)) ],
                 [ math.sin(n*2*math.pi/self.nb_rotates) for n in range(self.nb_rotates)],
                 [ math.cos(n*2*math.pi/self.nb_rotates) for n in range(self.nb_rotates)] )
   
