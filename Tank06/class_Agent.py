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
    """ classe décrivant un agent se déplaçant  selon une direction et une vitesse sur un terrain
    """

    def __init__(self, terrain, name, l_img_name, pos=(0,0), nb_rotates=1,
                 v=0, vmax=0, accel=0, friction_force=0,
                 bloc_size=64,
                 id_img_mask = 0):
        """ constructeur de la classe
             terrain    : le terrain sur lequel évolue l'agent
             name       : nom de l'agent
             l_img_name : liste des noms des images de l'agent devant être dessinées dans l'ordre de la liste
             pos:  position (x,y) de l'agent (coin haut gauche)
             nb_rotates: nombre de rotations à pré-générer  (rotations par pas de 2pi/nb_rotations)
             v=0, vmax=10, accel=0, friction_force=0: vitesse, accélération et force de frottement
             bloc_size  : taille carée centrée de la zone d'ocupation infranchissable de l'agent
             id_img_mask: id de l'image de l'agent pour laquelle le masque sert aux détection de collision
             
        """
        print("--> création de l'agent", name)
        self.name = name
        self.l_img_name = l_img_name
        self.nb_rotates = nb_rotates
        self.init_rotation()  #rotation de chaque image initialisée à 0

        # génération de liste des rotations de chaque image dans l_img_name
        #   self.l_img_rotated[n][i] = image n en rotation i*nb_rotates/360°
        #   self.l_sin[i] = sinus(i*nb_rotates/2pi)
        #   self.l_cos[i] = cosinus(i*nb_rotates/2pi)
        self.l_img_rotated, self.l_sin, self.l_cos = self.rotates_l_img(l_img_name)

        # génère la liste de masques d'images pour les calculs de collision précis au pixel près
        #   self.l_img_mask[i] = masque de l'image sefl_id_img_mask en rotation de i*nb_rotates/360 °
        self.id_img_mask = id_img_mask
        self.l_img_mask = [ pygame.mask.from_surface(self.l_img_rotated[self.id_img_mask][i])
                                                    for i in range(nb_rotates) ]
    
        self.terrain = terrain    # terrain sur lequel évolue le tank
        self.size = self.l_img_rotated[0][0].get_width()  # taille des images en nb de pixels d'un agent
        self.half_size = int(self.size/2)         # 1/2 taille des images en nb de pixels
        self.quart_size = int(self.size/4)        # 1/4 taille des images en nb de pixels
        self.pos = pos                            # position de l'agent (2-tuple, coin haut gauche)
        self.bloc_size = bloc_size                # taille carée du bloc infranchissable de l'agent (centré)
        self.nb_bloc_neighb = int(self.bloc_size/self.terrain.bloc_size)+1 #nb de blocs de la map occupées par la zone infranchissable
        self.bloc_delta = int((self.size-self.bloc_size)/2)  # position relative de la zone infranchissable dans l'agent
        self.v=v                                  # vitesse de l'agent, orienté dans la direction self.l_rotate[0])
        self.vMax = vmax                          # vitesse max de l'agent
        self.accel = accel                        # accélération de l'agent
        self.friction_force = friction_force      # accélération négative dues aux forces de frottements: ralenti l'agent si pas d'accélération
        self.timer = 0                            # timer interne à l'agent +1 à chaque fois qu'il bouge
        self.activates_all()                      # active toutes les images
        
    def pos_to_grid(self):
        """ Retourne la position dans la map en indice (l, c)
            à partir de la position en pixels du bloc infranchissable de l'agent
            (l,c) = indice ligne et colonne dans la map du terrain
        """
        x, y = self.pos # position de l'agent
        c = int((x+self.bloc_delta) / self.terrain.bloc_size)
        l = int((y+self.bloc_delta) / self.terrain.bloc_size)
        return l, c

    def get_neighbour_blocks(self):
        """Retourne la liste des rectangles en collision avec le bloc infranchissable de l'agent
            Vu que le bloc infranchissable de l'agent  est dans le carré pos+bloc_pos de taille bloc_size
            bloc_size faisant la même taille que les bloc_size du terrain
            il ne peut entrer en collision qu'avec 2*2=4 blocs du terrain qui partent de la même case dans la map
        """
        blocks = []
        l_start,c_start = self.pos_to_grid() #position de l'agent (zone infranchissable) sur la grille de la map
        rect_agent = pygame.Rect( (self.pos[0], self.pos[1]),
                                  (self.size, self.size) )  # rectangle pygame zone infranchissable agent
        
        #parcours des blocs voisins sur la map
        for l in range(l_start, l_start+self.nb_bloc_neighb):
            for c in range(c_start, c_start+self.nb_bloc_neighb):
                try:
                    if self.terrain.isFull((l,c)):  #ce bloc contient des éléments infranchissables
                        #contrôle des masques pour voir collision au pixel près
                        topleft = c*self.terrain.bloc_size, l*self.terrain.bloc_size
                        rect_map = pygame.Rect((topleft), (self.terrain.bloc_size, self.terrain.bloc_size))  # rectangle pygame zone map
                        pygame.draw.rect(self.terrain.screen,(255,255,0), rect_map, 3)                       #entoure d'un carré jaune width = 3
                        if self.terrain.matrix_mask[l][c].overlap(                             # masque zone infranchissable du terrain en l,c
                                self.l_img_mask[self.l_rotation[self.id_img_mask]],            # masque zone infranchissable de l'agent
                                (rect_agent.left - rect_map.left, rect_agent.top-rect_map.top) # offset zone agent par rapport à la zone terrain 
                            ) != None :
                            blocks.append(rect_map)
                except: #cas aux limites où l,c se retrouve en dehorts de la map
                    pass
        return blocks     

    def bouge(self):
        """ méthode pour faire bouger l'agent selon acceleration, vitesse et orientation
        """
        pos_save = self.pos
        v_save, accel_save = self.v, self.accel
        
        # si pas d'accélération et vitesse non nule: la force de frottement fait ralentir le tank dans le sens de sa vitesse
        if (self.accel==0 and self.v!=0):
            self.accel = self.friction_force * ( (self.v>0) - (self.v<0) )
        # nouvelle vitesse, ne pouvant dépasser self.vMax en valeur absolue
        self.v += self.accel
        if abs(self.v) > self.vMax:
            self.v = ( (self.v>0) - (self.v<0) ) * self.vMax            
            
        #position modifiée selon vitesse de l'agent
        if self.v !=0 :
            x = self.pos[0] - self.v*self.l_sin[self.l_rotation[0]]
            y = self.pos[1] - self.v*self.l_cos[self.l_rotation[0]]
            self.pos = (x,y)

        self.timer += 1  # timer interne de l'agent incrémenté

        #liste des blocs en collisions avec la zone infranchissable de l'agent
        blocks = self.get_neighbour_blocks()
        
        #dessin des blocs en collision et de la zone infranchissable de l'agent
        for rect in blocks: #dessins de rectangle rouge width=6 sur les blocs en collision
            pygame.draw.rect(self.terrain.screen, (255,0,0), rect, 6)


    def activates_all(self):
        """ active toutes les images
        """
        self.l_actif = [True]* len(self.l_img_name)

    def desactivates_all(self):
        """ désactive toutes les images
        """
        self.l_actif = [False]* len(self.l_img_name)
        
    def init_rotation(self):
        """
        initialise toutes les rotations à 0
        """
        self.l_rotation = [0] * len(self.l_img_name)
        
    def rotates(self, add_rotation, id_elm=None):
        """ gère la rotation des éléments dans la liste l_id_img
             si l_id_img = self.l_rotation: c'est l'agent en entier qui subit une rotation +add_rotation
             si l_id_img = un seul élément: seul cet élément va subir une rotation +add_rotation 
        """
        if id_elm==None:
            for n in range(len(self.l_rotation)): #rotation propagée à tous les éléments de la liste
                self.l_rotation[n]=(self.l_rotation[n] + add_rotation) % self.nb_rotates
        else:
            self.l_rotation[id_elm]=(self.l_rotation[id_elm] + add_rotation) % self.nb_rotates

    def orient(self, id_rotation, id_elm=None):
        """ gère l'orientation des éléments dans la liste l_id_img
             si l_id_img = self.l_rotation: c'est l'agent en entier qui est orienté vers id_rotation
             si l_id_img = un seul élément: seul cet élément va être orienté
        """
        if id_elm==None:
            for n in range(len(self.l_rotation)): #rotation propagée à tous les éléments de la liste
                self.l_rotation[n] = id_rotation % self.nb_rotates
        else:
            self.l_rotation[id_elm] = id_rotation % self.nb_rotates
        
    def dessine(self):
        """ dessin de l'agent sur le terrain en position self.pos
        """
        #parcours des images de l'agent selon leur index respectifs de rotation
        for n in range(len(self.l_actif)):
            if self.l_actif[n]:
                self.terrain.screen.blit(self.l_img_rotated[n][self.l_rotation[n]], self.pos)
        #dessine un carré bleu autour de la zone infranchissable de l'agent.
        rect = pygame.Rect(self.pos[0]+self.bloc_delta,  
                                self.pos[1]+self.bloc_delta,
                                self.bloc_size, self.bloc_size)
        pygame.draw.rect(self.terrain.screen, (0,0,255), rect, 3) 

        
    def rotates_l_img(self, l_img_name):
        """ retourne 3 listes :
        Première liste retournée: liste d'images avec rotations
            rotates_l_img[0] = liste des rotations de l'image l_img_name[0] 
            rotates_l_img[1] = liste des rotations de l'image l_img_name[1] 
            ...
            rotates_l_img[n] = liste des rotations de l'image l_img_name[n]
        Seconde liste retournée: liste des sinus de chaque nb_rotates angles
        Troisième liste retournée: liste des cosinus de chaque nb_rotates angles
        """

        # fonction interne qui génère une liste de nb_rotates rotations à partir d'une seule image
        def rotates_img(img_file, nb_rotates):
            """ génère une liste d'images avec rotations
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
   
