#!/usr/bin/env python3
########################################################################
# Description : création jeux TANK avec Pygame - Partie 03
# auther      : papsdroid.fr
# modification: 2020/04/13
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
            nb_spritesX=18, nb_spritesY=12 représentent la taille du plateau de jeux en nombre de tuiles 64*64 pixels
            chaque sprites est découpée en nb_cuts*nb_cuts carrés qui vont définir la grille sur la map, de 64/nb_cuts * 64/nb_cuts pixels
            cette grille va permettre de savoir ce qui est franchissable ou non sur la map.
        """   
        self.size_spriteX, self.size_spriteY = size_spriteX, size_spriteY       # taille des tuiles (64*64 pixels par défaut)
        self.nb_spritesX, self.nb_spritesY   = nb_spritesX,  nb_spritesY        # taille de la fenêtre en nombre de tuiles
        self.nb_pixelsX = self.size_spriteX * self.nb_spritesX                  # nb de pixels horizontaux (colonnes)
        self.nb_pixelsY = self.size_spriteY * self.nb_spritesY                  # nb de pixels verticaux (lignes)
        self.nb_cuts = 2                                                        # définition des blocs infranchissables en fraction de sprites
        self.bloc_size = int(self.size_spriteX/self.nb_cuts)                    # taille des blocs de la grille sur la map

        self.path_media = 'Media/Decors/'           # chemin relatif où sont stockées les images décors
        self.path_map = 'Map/'                      # chemin relatif où sont stockées les map
        self.sprites_file_name = 'map_sprites.txt'  # dictionnaire des sprites (tuiles 64*64 pixels)

        # création du dictionnaire des sprites utilisées dans la MAP { 'CODE': 'fileName.png'}
        #  et de la liste de nb_cuts*nb_cuts dictionnaires { 'CODE' : TRUE/FALSE } correspondant à l'occupation de chaque sprite sur la grille
        self.sprites, self.l_sprites_grid = self.read_sprites()
        
        # dictionnaire des images des sprites (format PIL) fabriqué à partir du dictionnaire self.sprites
        self.sprites_pil = { key: Image.open(self.path_media+self.sprites[key]).convert('RGBA')
                                  for key in self.sprites.keys()
                                  if key != '  '
                                }
        self.sprites_pil['  '] = None # ajout de la clé '  ' qui correspond à None (pas d'image)
        
        # préparation des matrices d'images (format PIL) et occupations sur la grille
        #    par fusion des MAP fournies dans map_filenames
        # lecture de la 1ère map pour initialiser les matrices
        matrix_map_pil, self.l_matrix_occup = self.read_map(map_filenames[0]) 

        #parcours des map_filenames suivants pour fusionner les éléments dans les matrices
        for map_filename in map_filenames[1:]: 
            matrix_map_add_pil, l_matrix_occup = self.read_map(map_filename) #converti la map_filename en matrice d'image PIL + matrices d'occupations
            # on fusionne chaque image non nulle (!=None) avec l'image initiale dans la matrice matrix_map_pil
            for y in range(self.nb_spritesY):
                for x in range(self.nb_spritesX):
                    if  matrix_map_add_pil[y][x] != None : # image non vide
                        matrix_map_pil[y][x] = Image.alpha_composite(matrix_map_pil[y][x], matrix_map_add_pil[y][x])
                        #fusion des codes occupations: si un code à fusionner est TRUE, alors le code final fusionné est TRUE.
                        for n in range(len(l_matrix_occup)):
                            if l_matrix_occup[n][y][x]:
                                self.l_matrix_occup[n][y][x] = True

        #construction matrice d'occupation full avec tous les nb_cuts*nb_cuts blocs de chaque sprites
        # cette matrice est de dimension nb_spritesY*nb_cuts lignes et nb_spritesX*nb_cuts colonnes
        # self.map_occup[l] = liste des True/False de chaque bloc sur la grille de la ligne y
        # self.map_occup[l][c] = True/False concernant un bloc en ligne l et colonne c
        # True signifie que ce bloc est occupé par un obstacle infranchissable        
        self.map_occup = []
        for l in range(self.nb_cuts*self.nb_spritesY):     # parcours des lignes de la gille
            self.map_occup.append([])                      # insertion d'une ligne vierge
            for c in range(self.nb_cuts*self.nb_spritesX): # parcours des colonnes de la grille
                x, y = int(c/self.nb_cuts), int(l/self.nb_cuts)    # coordonées dans les tableaux de sprites
                n = (l % self.nb_cuts) * self.nb_cuts + (c % self.nb_cuts) # index n° de bloc dans les listes
                self.map_occup[l].append(self.l_matrix_occup[n][y][x])
        
        print('self.map_occup', len(self.map_occup),'*',len(self.map_occup[0]), self.map_occup)

        #construction du background final en y collant toutes les images 64*64 générées
        print('...contruction décors',self.nb_pixelsY,'*',self.nb_pixelsX, 'pixels')
        background_pil = Image.new('RGBA',(self.nb_pixelsX, self.nb_pixelsY), 0) #création d'une image noire de la taille de l'écran
        #parcours la matrice d'images 64*64 à coller une par une au bon endroit
        for y in range(self.nb_spritesY):
            for x in  range(self.nb_spritesX):
                background_pil.paste(matrix_map_pil[y][x], (x*self.size_spriteX, y*self.size_spriteY))

        #initialisation pygame
        pygame.init()                   
        self.screen = pygame.display.set_mode((self.nb_pixelsX, self.nb_pixelsY),0,32)
        pygame.display.set_caption("TANK - Pygame Tutoriel - papsdroid.fr")   # titre

        #conversion finale de l'image PIL en image Pygame
        self.background_img = pygame.image.fromstring(background_pil.tobytes(), background_pil.size, 'RGBA')
        
    def isFull(self,grid_pos):
        """ determine s'il y a un obstacle infranchissable sur la map en ligne l, colonne c 
        """
        l,c = grid_pos
        return self.map_occup[l][c]
    
    def read_sprites(self):
        """
        lecture des sprites, retourne le disctionnairele dictionnaire des sprites {'code_sprite': 'filemane.png'}
         ainsi qu'une liste de dictionnaires {'code_sprite':TRUE/FALSE} correspondant à chaque bloc de la grille (liste de nb_cuts*nbcuts dictionnaires)
        """
        dic_sprites = {}  #dictionnaire des sprites initialisé à vide
        #liste des nb_cuts*nb_cuts dictionnaires pour chaque bloc sur la grille, initialisés à vides
        l_dic_map = []
        for n in range (self.nb_cuts*self.nb_cuts):
            l_dic_map.append({})
        try:
            # ouverture du fichier Map/map_sprites.txt en lecture seule
            with open(self.path_map + self.sprites_file_name, 'r') as f: 
                for line in f:                  # parcours des lignes du fichier
                    if line[0] != '#':          # on ignore toutes les lignes de commentaires qui commencent par '#'
                        words = line.split('|') # récupère tous les mots séparés par '|' dans une liste
                        #on ajoute dans self.map la liste des codes trouvés sauf retour chariot '\n' et sauf entête 'M'
                        try:
                            code = words[1]               # code sprites
                            file_name = words[2].strip()  # file name de la sprite, avec supression des espaces
                            try:   #vérification de l'existance du fichier
                                with open(self.path_media + file_name, 'r') as fs:
                                    pass 
                            except:
                                print('Le fichier: "' + self.path_media + file_name+ '" est introuvable.')
                                exit()
                            l_occup=[]
                            #liste des nb_cuts*nb_cuts codes occupation 
                            for n in range (self.nb_cuts*self.nb_cuts):
                                l_occup.append(words[4+n].strip())
                        except: #ficher Map/map_sprites.txt ne respecte pas le bon format
                            print('Le ficher " ' + self.path_map+self.sprites_file_name+'" ne respecte pas le bon format:')
                            print('ligne lue: ', line)
                            exit()
                        dic_sprites[code] = file_name  # ajout de {code : filename} au dictionnaire dic_sprites
                        # ajout de {code: TRUE/FALSE} au dictionnaire correspondant au bloc sur la grille
                        for n in range (self.nb_cuts*self.nb_cuts): 
                            l_dic_map[n][code] = (l_occup[n]!='')
        except:
            print('Problème avec le fichier: "' + self.path_map+self.sprites_file_name + '"')
            exit()

        #ajout du code '  ' aux dictionnaires, ce code signifiant l'absence d'image
        dic_sprites['  '] = None
        for n in range (self.nb_cuts*self.nb_cuts):
            l_dic_map[n]['  '] = False

        #print(l_dic_map)
        return dic_sprites, l_dic_map    
        
    def read_map(self, map_file_name):
        """
        lecture d'un fichier MAP (voir fichier modèle.map), retourne les matrices:
            matrice d'images format PIL: matrix_map_pil[y][x] = image ligne y, colonne x (en nb de sprites)
            l_matrix_map[n][y][x] = code occupation TRUE/FALSE du bloc n en ligne y, colonne x (en nb de sprites)
        On connait ainsi pour chaque tuile en [y][x] quelle est l'image à afficher, et les occupations TRUE/FALSE de chaque bloc n
        """
        # préparation de la matrice des codes map, dimension nb_spirteY lignes * nb_spritesX colonnes
        # matrix_map[y][x] = code sprite
        matrix_map = [] 
        try:
            with open(map_file_name, 'r') as f: # ouverture du fichier map en lecture seule
                for line in f:                  # parcours des lignes du fichier
                    if line[0] == 'M':          # on ignore toutes les lignes de commentaires qui ne commencent par par 'M'
                        codes = line.split('|') # récupère tous les codes séparés par '|' dans une liste
                        #on ajoute dans self.map la liste des codes trouvés sauf retour chariot '\n' et sauf entête 'M'
                        try:
                            matrix_map.append([c for c in codes if c!='\n' and c[0]!='M']) #liste de codes ajoutés à la map
                        except:
                            print('fichier',map_file_name,'ne respecte pas le bon format')
                            exit()
        except:
            print('Problème de lecture du fichier: "' + map_file_name + '".')
            exit()

        # conversion des codes de matrix_map en matrices d'images grâce au dictionnaires d'images self.sprites_pil
        # matrix_map_pil[y][x] = image ligne y, colonne x
        matrix_map_pil = [ [ self.sprites_pil[matrix_map[y][x]]
                              for x in range(self.nb_spritesX) ]
                                for y in range(self.nb_spritesY)
                          ]

        #conversion des codes de matrix_map en une liste de nb_cuts*nb_cuts matrices d'occupation  pour chaque bloc dans chaque sprite
        # l_matrix_map[n][y][x] = code occupation TRUE/FALSE du bloc n de la sprite en ligne y, colonne x
        l_matrix_map = [] 
        for n in range(self.nb_cuts*self.nb_cuts):
            l_matrix_map.append([])
            l_matrix_map[n] =[ [ self.l_sprites_grid[n][matrix_map[y][x]]
                                 for x in range(self.nb_spritesX) ]
                                    for y in range(self.nb_spritesY)
                          ]
    
        print(' ... lecture map', map_file_name, len(matrix_map_pil), 'lignes *', len(matrix_map_pil[0]),'colonnes')
        return matrix_map_pil, l_matrix_map

    def dessine(self):
        """
        méthode de déssin des décors du terrain
        """
        self.screen.blit(self.background_img, (0,0))
