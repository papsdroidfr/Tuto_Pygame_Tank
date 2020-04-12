#!/usr/bin/env python3
########################################################################
# Filename    : Tank_partie01.py
# Description : création jeux TANK avec Pygame - Partie 02
# auther      : papsdroid.fr
# modification: 2020/04/10
########################################################################

import pygame                   # PYGAME package
from pygame.locals import *     # PYGAME constant & functions
from sys import exit            # exit script
from PIL import Image           # bilbiothèque pour traitement d'image

class Terrain():
    """
    classe du terrain de jeux défini par un nombre de tuiles (size_factor_X, size_factor_Y)
    """
    
    def __init__(self, map_filenames, size_spriteX=64, size_spriteY=64, nb_spritesX=18, nb_spritesY=12):
        """
        constructeur de la classe qui va initiliaser la fenêtre pygame
            map_filenames : liste des maps à fusionner l'une sur l'autre pour fabriquer le décors fixe de la map
            size_spriteX=64, size_spriteY=64 représentent la taille des tuiles 64*64 pixels par défaut
            nb_spritesX=18, nb_spritesY=12 représentent la taille du plateau de jeux en nombre de tuiles
        """   
        self.size_spriteX, self.size_spriteY = size_spriteX, size_spriteY       # taille des tuiles (64*64 pixels par défaut)
        self.nb_spritesX, self.nb_spritesY   = nb_spritesX,  nb_spritesY        # taille de la fenêtre en nombre de tuiles
        self.nb_pixelsX = self.size_spriteX * self.nb_spritesX                  # nb de pixels horizontaux (colonnes)
        self.nb_pixelsY = self.size_spriteY * self.nb_spritesY                  # nb de pixels verticaux (lignes)

        # initialisation Pygame
        pygame.init()                   
        self.screen = pygame.display.set_mode((self.nb_pixelsX, self.nb_pixelsY),0,32)
        pygame.display.set_caption("TANK - Pygame Tutorial PARTIE 02")   # titre
        self.path_media = 'Media/Decors/' # chemin relatif où sont stockées les images décors

        # dictionnaire des tuiles utilisées dans la MAP { 'CODE': 'fileName'}
        self.sprites = {'  ': None,   
                        '00': 'Ground_Tile_01_A_64x64.png', # fond désert 1
                        '01': 'Ground_Tile_02_A_64x64.png', # fond désert 2
                        'h1': 'Hedge_A_01_64x64.png',       # bord haut gauche
                        'h2': 'Hedge_A_01b_64x64.png',      # bord haut droite
                        'h3': 'Hedge_A_01c_64x64.png',      # bord bas droite
                        'h4': 'Hedge_A_01d_64x64.png',      # bord bas gauche  
                        'b1': 'Hedge_A_02_64x64.png',       # bord haut
                        'b2': 'Hedge_A_02b_64x64.png',      # bord droite
                        'b3': 'Hedge_A_02c_64x64.png',      # bord bas
                        'b4': 'Hedge_A_02d_64x64.png',      # bord gauche
                        'p1': 'Platform_64x64.png',         # plateforme
                        'Ph': 'Block_AH_01_64x64.png',      # mur en pierres haut
                        'Pg': 'Block_AG_01_64x64.png',      # mur en pieres gauche
                        'Pd': 'Block_AD_01_64x64.png',      # mur en pierres droite
                        'Pb': 'Block_AB_01_64x64.png',      # mur en pierres bas
                        'P1': 'Block_AHG_02_64x64.png',     # mur petite pierres Haut Gauche
                        'P2': 'Block_AHD_02_64x64.png',     # mur petite pierres Haut Droite
                        'P3': 'Block_ABG_02_64x64.png',     # mur petite pierres Bas Gauche
                        'P4': 'Block_ABD_02_64x64.png',     # mur petite pierres Bas Droite
                        'R1': 'Rock_01_64x64.png',          # rochers 1
                        'Rm': 'Rock_01m_64x64.png',         # tas de rochers 1
                        'R2': 'Rock_02_64x64.png',          # rochers 2
                        'R3': 'Rock_03_64x64.png',          # rochers 3
                        'T7': 'Tree_07_64x64.png',          # sourche arbre 
                        'T8': 'Tree_08_64x64.png',          # souche arbre
                        'T9': 'Tree_09_64x64.png',          # souche arbre
                        'Tm': 'Tree_07m_64x64.png',         # souches multiples avec pierres
                        'T1': 'Log_64x64.png',              # tronc à terre horizontal
                        'T2': 'Logb_64x64.png',             # tronc à terre vertical
                        'c1': 'Cactus_01_64x64.png',        # cactus
                        'c2': 'Cactus_02_64x64.png',        # cactus
                        'c3': 'Cactus_03_64x64.png',        # cactus
                        's1': 'Decor_Tile_B_01_64x64.png',  # sol fermeture haut gauche
                        's2': 'Decor_Tile_B_02_64x64.png',  # sol fermeture haut
                        's3': 'Decor_Tile_B_03_64x64.png',  # sol fermeture haut droite
                        's4': 'Decor_Tile_B_04_64x64.png',  # sol fermeture gauche
                        's5': 'Decor_Tile_B_05_64x64.png',  # sol sans aucune fermeture
                        's6': 'Decor_Tile_B_06_64x64.png',  # sol fermeture droite
                        's7': 'Decor_Tile_B_07_64x64.png',  # sol fermeture bas gauche
                        's8': 'Decor_Tile_B_08_64x64.png',  # sol fermeture bas
                        's9': 'Decor_Tile_B_09_64x64.png',  # sol fermeture bas droite
                        'fa': 'Dot_A_64x64.png',            # marqueur rouge
                        'fb': 'Dot_B_64x64.png',            # marqueur bleu
                        }
        
        # dictionnaire des images des tuiles (format PIL) fabriqué à partir du dictionnaire des tuiles self.sprites
        self.sprites_pil = { key: Image.open(self.path_media+self.sprites[key]).convert('RGBA')
                                  for key in self.sprites.keys()
                                  if key != '  '
                                }
        self.sprites_pil['  '] = None # ajout de la clé '  ' qui correspond à None (pas d'image)
        
        # préparation de la matrice d'images (format PIL) de la map, par fusion des MAP fournies dans map_filenames
        matrix_map_pil = self.lire_map(map_filenames[0]) #conversion de la 1ère map en matrice d'image PIL

        #parcours des map_filenames suivants
        for map_filename in map_filenames[1:]: 
            matrix_map_add_pil = self.lire_map(map_filename) #converti la map_filename en matrice d'image PIL
            # on fusionne chaque image non nulle (!=None) avec l'image initiale dans la matrice matrix_map_pil
            for y in range(self.nb_spritesY):
                for x in range(self.nb_spritesX):
                    if  matrix_map_add_pil[y][x] != None : # image non vide
                        matrix_map_pil[y][x] = Image.alpha_composite(matrix_map_pil[y][x], matrix_map_add_pil[y][x])  

        #construction du background final en y collant toutes les images 64*64 générées
        print('...contruction décors',self.nb_pixelsY,'*',self.nb_pixelsX, 'pixels')
        background_pil = Image.new('RGBA',(self.nb_pixelsX, self.nb_pixelsY), 0) #création d'une image noire de la taille de l'écran
        #parcours la matrice d'images 64*64 à coller une par une au bon endroit
        for y in range(self.nb_spritesY):
            for x in  range(self.nb_spritesX):
                background_pil.paste(matrix_map_pil[y][x], (x*self.size_spriteX, y*self.size_spriteY))

        #conversion finale de l'image PIL en image Pygame
        self.background_img = pygame.image.fromstring(background_pil.tobytes(), background_pil.size, 'RGBA')
        
                
    def lire_map(self, map_file_name):
        """
        lecture d'un fichier MAP (voir fichier modèle.map)
            retourne une matrice 2d d'images PIL
        """
        matrix_map = []
        with open(map_file_name, 'r') as f: # ouverture du fichier map en lecture seule
            for line in f:                  # parcours des lignes du fichier
                if line[0] == 'M':          # on ignore toutes les lignes de commentaires qui ne commencent par par 'M'
                    codes = line.split('|') # récupère tous les codes séparés par '|' dans une liste
                    #on ajoute dans self.map la liste des codes trouvés sauf retour chariot '\n' et sauf entête 'M'
                    matrix_map.append([c for c in codes if c!='\n' and c[0]!='M']) #liste de codes ajoutés à la map
        matrix_map_pil = [ [ self.sprites_pil[matrix_map[y][x]]
                              for x in range(self.nb_spritesX) ]
                                for y in range(self.nb_spritesY)
                          ]        
        print(' ... lecture map', map_file_name, len(matrix_map_pil),'lignes *',len(matrix_map_pil[0]),'colonnes')
        return matrix_map_pil

    def dessine(self):
        """
        méthode de déssin des décors du terrain
        """
        self.screen.blit(self.background_img, (0,0))
                
class Tank():
    """
    classe décrivant un tank
    """

    def __init__(self, tank_img_filenames, terrain, human=False, x=0, y=0):
        """
        constructeur de la classe
            tank_img_filenames: liste des chemins des images qui constituent le tank
            terrain: le terrain sur lequel évolue le tank
            bool_human: True si joué par un humain, False si joué par la machine
            x,y: position du tank (coin haut gauche), valeur par défaut = (0,0)
        """
        self.tank_base_img = pygame.image.load(tank_img_filenames[0]).convert_alpha()    # image du coprs du tank
        self.tank_weapon_img = pygame.image.load(tank_img_filenames[1]).convert_alpha()  # image du canon du tank
        self.terrain = terrain    # terrain sur lequel évolue le tank
        self.human = human        # True: joué par un humain
        self.sizeX, self.sizeY = self.tank_base_img.get_width(), self.tank_base_img.get_height()  # taille du tank en nb de pixels
        self.half_sizeX, self.half_sizeY = int(self.sizeX/2), int(self.sizeY/2)  #1/2 taille qui sera souvent utilisée pour localiser le centre
        self.weapon_sizeX, self.weapon_sizeY = self.tank_weapon_img.get_width(), self.tank_weapon_img.get_height()  # taille arme en nb de pixels
        self.weapon_deltaX = self.half_sizeX - int(self.weapon_sizeX/2) # correction de la position du canon pour qu'il soit centré sur le tank
        self.x, self.y = x,y   # position du centre du tank

    def bouge(self):
        """
        méthode pour faire bouger le tank
        """
        if self.human:
            #positionnenemnt du tank joué par un humain avec la souris
            x,y = pygame.mouse.get_pos() # récupère la position de la souris
            self.x, self.y = x-self.half_sizeX, y-self.half_sizeY

    def dessine(self):
        """
        méthode de dessin du tank sur le terrain en position (x,y)
        """
        self.terrain.screen.blit(self.tank_base_img, (self.x,self.y)) # dessine le coprs du tank en (x,y)
        self.terrain.screen.blit(self.tank_weapon_img, (self.x + self.weapon_deltaX, self.y ) )       # canon du tank bien centré


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
        self.tanks.append(Tank(['Media/Tank/Hull_02_colorA_64x64.png', # premier tank
                                'Media/Tank/Gun_05_colorA_19x49.png'],
                                 self.terrain, human=False,
                                 x = 2*self.terrain.size_spriteX,
                                 y = 2*self.terrain.size_spriteY
                                 ))   
        self.tanks.append(Tank(['Media/Tank/Hull_02_colorD_64x64.png',  # second tank
                                'Media/Tank/Gun_05_colorD_19X49.png'],
                                self.terrain, human=True
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
