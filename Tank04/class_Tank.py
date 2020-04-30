#!/usr/bin/env python3
########################################################################
# Description : création jeux TANK avec Pygame - Partie 3
# auther      : papsdroid.fr
# modification: 2020/04/10
########################################################################

import pygame                     # PYGAME package
from pygame.locals import *       # PYGAME constant & functions
from class_Terrain import Terrain # classe Terrain() du fichier class_Terrain.py
from class_Agent import Agent     # classe Agent() du fichier class_Agent.py

#--- EXPLOSION
class Explosion(Agent):
    """
    classe décrivant une explosion (d'un obus sur un obstacle)
    """

    def __init__(self, terrain, obus, name):
        """
        constructeur de la classe
            terrain    : le terrain sur lequel évolue l'obus
            obus       : l'obus qui a généré l'explosion
            name       : nom de l'agent
        """
        # appel au constructeur de la classe mère Agent: vitesse et accélération nulle, pas de rotation
        Agent.__init__(self,terrain, name,
                       l_img_name= ['Media/Tank/Explosion/Sprite_Effects_Explosion_000_64x64.png', # motif explosion 1
                           'Media/Tank/Explosion/Sprite_Effects_Explosion_001_64x64.png', # motif explosion 2
                           'Media/Tank/Explosion/Sprite_Effects_Explosion_002_64x64.png', # motif explosion 3
                           'Media/Tank/Explosion/Sprite_Effects_Explosion_003_64x64.png', # motif explosion 4
                           'Media/Tank/Explosion/Sprite_Effects_Explosion_004_64x64.png', # motif explosion 5
                           'Media/Tank/Explosion/Sprite_Effects_Explosion_005_64x64.png', # motif explosion 6
                           'Media/Tank/Explosion/Sprite_Effects_Explosion_006_64x64.png', # motif explosion 7
                           'Media/Tank/Explosion/Sprite_Effects_Explosion_007_64x64.png', # motif explosion 8
                           'Media/Tank/Explosion/Sprite_Effects_Explosion_008_64x64.png'  # motif explosion 9
                           ]
                       )
        self.desactivates_all()     # désactive toutes les images
        self.booom = False          # True: l'explosion est visible
        
    def bouge(self):
        """
        méthode pour animer l'explosion
        """
        if self.booom:
            if self.timer>0:
                self.l_actif[self.timer-1] = False     # désactive l'imge précédente
            self.l_actif[self.timer] = True            # active image suivante selon timer interne
            if self.timer == len(self.l_img_name) -1 : # fin de l'explosion
                self.booom = False
                self.desactivates_all()
                self.timer = 0
            Agent.bouge(self)
    
#--- OBUS
class Shell(Agent):
    """
    classe décrivant un obus d'un tank: dérive de la classe Agent.
    """

    def __init__(self, terrain, tank, name):
        """
        constructeur de la classe
            terrain    : le terrain sur lequel évolue l'obus
            tank       : le tank qui a tiré cet obus
            name       : nom de l'agent
            l_img_name : liste des noms des images  devant être dessinées dans l'ordre de la liste
            pos:  position (x,y) du tank (coin haut gauche)
            nb_rotates: nombre de rotations à pré-générer  (rotations par pas de 2pi/nb_rotations)
        """
        self.tank = tank  # le tank qui a tiré l'obus
        # appel au constructeur de la classe mère Agent: vitesse = vitesse max = 30, pas d'accel et pas de frottement
        Agent.__init__(self,terrain, name,
                        l_img_name=['Media/Tank/Explosion/Light_Shell_128x128.png',          # obus
                                    'Media/Tank/Explosion/Sprite_Fire_Shots_Shot_A_000.png'  # feux de tir
                                   ],
                        pos=tank.pos, nb_rotates=tank.nb_rotates,
                        v=30, vmax=30, accel=0, friction_force=0)
        self.id_shell = 0   # id de l'obus
        self.id_fire = 1    # id du feux de tir
        self.countdown = 0  # si compte à rebours obus à 0: le tank peut tirer son obus
        self.explosion = Explosion(terrain, self, self.name+' explosion') # explosion quand l'obus touche un obstacle
        
    def bouge(self):
        """
        méthode pour faire bouger l'obus
        """
        if self.timer > 0:   # boule de feux de tir activée au tout début, quand timer = 0
            self.l_actif[self.id_fire]=False
        if self.countdown == 0: # fin du compte à rebourg: arrêt et explosion de l'obus.
            self.v=0
        Agent.bouge(self)
        if self.v==0:        # l'obus a rencontré un obstacle : explosion activée
            self.explosion.pos = (self.pos[0]-self.explosion.half_size+self.half_size,
                                  self.pos[1]-self.explosion.half_size+self.half_size ) # positionne l'explosion centrée sur l'obus
            self.explosion.booom = True   # active l'animation de l'explosion

#--- TANK
class Tank(Agent):
    """
    classe décrivant un tank: dérive de la classe Agent.
    """

    def __init__(self, terrain, name, l_img_name, human=False, pos=(0,0), nb_rotates=16):
        """
        constructeur de la classe
            terrain    : le terrain sur lequel évolue le tank
            name       : nom du tank
            l_img_name : liste des noms des images du tank devant être dessinées dans l'ordre de la liste
            human: True si joué par un humain, False si joué par la machine
            pos:  position (x,y) du tank (coin haut gauche)
        """
        # appel au constructeur de la classe mère Agent
        Agent.__init__(self,terrain, name, l_img_name, pos, nb_rotates=64, v=0, vmax=10, accel=0, friction_force=-1)
        self.human = human        # True: joué par un humain
        self.id_shield, self.id_hull, self.id_weapon = 0,1,2 #id image du bouclier, coprs , canon et tir du tank
        self.new_accel = 1 #accélération du tank quand la commande Acceleration est activée
        self.shell = Shell(self.terrain, self, self.name+' shell') # agent "Obus" qui sera activé si tir.
        self.shell_countdown_init = 20    # compte à rebours pour retirer un obus: -1 chaque mouvement
         
    def bouge(self):
        """
        méthode pour faire bouger le tank
        """
        if self.human:
            key_pressed = pygame.key.get_pressed()   # capture touche pressée
            #orientation du tank si touche pressée LEFT(rotation +1) ou RIGTH(rotation-1)
            self.rotates(key_pressed[K_LEFT] - key_pressed[K_RIGHT])             
            #rotation du canon uniquement si touches pressée  'S'(rotation +1) ou 'D' (rotation-1)
            self.rotates(key_pressed[K_s] - key_pressed[K_d], self.id_weapon)
            #accélération du tank selon commande d'accélération UP ou DOWN
            self.accel = self.new_accel*( key_pressed[K_UP] - key_pressed[K_DOWN] )

        Agent.bouge(self)              # nouvelle position et orientation du tank

        if self.shell.countdown > 0:   # l'obus a été tiré
            self.shell.countdown -= 1  # décompte le compte à rebours de l'obus
            self.shell.bouge()         # anime l'obus

        if self.shell.explosion.booom:   # l'obus tiré a rencontré un obstacle
            self.shell.explosion.bouge() # anime l'explosion
            

    def changes_shield(self):
        """
        inverse le status actif/inactif du bouclier
        """
        self.l_actif[self.id_shield] = not(self.l_actif[self.id_shield])

    def fire(self):
        """
        tir d'obus si le timing le permet
        """
        if self.shell.countdown == 0 :
            self.shell.timer = 0                                 # remet le timer interne de l'obus à zéro
            self.shell.v = self.shell.vMax                       # vitesse de l'obus = vMax dès le début
            self.shell.pos = self.pos                            # position de l'obus = celle du tank
            self.shell.activates_all()                           # active toutes les images
            self.shell.orient(self.l_rotation[self.id_weapon])   # orientation de l'obus = orientation du canon
            self.shell.countdown = self.shell_countdown_init     # début du compte à rebours
        
   
