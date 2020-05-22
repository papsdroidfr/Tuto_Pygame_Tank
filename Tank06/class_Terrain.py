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
from PIL import ImageDraw       # dessin à partir de PIL 

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
        self.bloc_size =  self.size_spriteX                                     # taille des blocs carrés de la grille sur la map

        self.path_media = 'Media/Decors/'           # chemin relatif où sont stockées les images décors
        self.path_map = 'Map/'                      # chemin relatif où sont stockées les map
        self.sprites_file_name = 'map_sprites.txt'  # dictionnaire des sprites (tuiles 64*64 pixels)

        # création du dictionnaire des sprites utilisées self.sprites = { 'CODE': 'fileName.png'}
        #  et du dictionnaire des codes occupation des sprites self.sprites_grid =  {'CODE' : TRUE/FALSE}
        #     TRUE signifie que la sprite est un bloc infranchissable
        self.sprites, self.sprites_grid = self.read_sprites()
        
        # dictionnaire des images des sprites (format PIL) fabriqué à partir du dictionnaire self.sprites
        self.sprites_pil = { key: Image.open(self.path_media+self.sprites[key]).convert('RGBA')
                                  for key in self.sprites.keys()
                                  if key != '  '
                                }
        self.sprites_pil['  '] = None # ajout de la clé '  ' qui correspond à None (pas d'image)
        
        # préparation des matrices d'images (format PIL) et occupations sur la grille
        #    par fusion des MAP fournies dans map_filenames

        # lecture de la 1ère map pour initialiser les matrices d'images et de blocs avec le background
        #  matrix_pil_background[l][c] = image 64*64 pixels ligne l colonne c d'une zone franchissable
        #  matrix_pil_bloc[l][c] = image 64*64 pixels ligne l colonne c concernant un bloc infranchissable
        #  self.matrix_bloc[l][c] = True/False True = bloc infranchissable
        matrix_pil_background, matrix_pil_bloc, self.matrix_bloc = self.read_map(map_filenames[0])

        #parcours des map_filenames suivants pour fusionner les éléments dans les matrices
        for map_filename in map_filenames[1:] :
            matrix_pil_background_add, matrix_pil_bloc_add, matrix_bloc_add = self.read_map(map_filename) 
            # on fusionne chaque image non nulle (!=None) avec l'image initiale dans les matrices
            for l in range(self.nb_spritesY):
                for c in range(self.nb_spritesX):
                    if  matrix_pil_background_add[l][c] != None : # image non vide
                        matrix_pil_background[l][c] = Image.alpha_composite(matrix_pil_background[l][c], matrix_pil_background_add[l][c])
                        #fusion des blocs non franchissables: si un code d'une MAP est TRUE, alors le code final fusionné est TRUE.
                        if matrix_bloc_add[l][c]:
                           self.matrix_bloc[l][c] = True
                           if matrix_pil_bloc[l][c] == None :
                               matrix_pil_bloc[l][c] = matrix_pil_bloc_add[l][c]
                           else:
                               matrix_pil_bloc[l][c] = Image.alpha_composite(matrix_pil_bloc[l][c], matrix_pil_bloc_add[l][c])
                                        
        #print('FINAL self.matrix_bloc', len(self.matrix_bloc),'*',len(self.matrix_bloc[0]), self.matrix_bloc)

        #construction du background final en y collant toutes les images 64*64 générées
        print('...contruction décors',self.nb_pixelsY,'*',self.nb_pixelsX, 'pixels')

        background_pil = Image.new('RGBA',(self.nb_pixelsX, self.nb_pixelsY), 0) #création d'une image noire de la taille de l'écran
        draw = ImageDraw.Draw(background_pil) #on va dessiner des rectangles sur la MAP correspondants aux tuiles

        #parcours la matrice d'images 64*64 pour fabriquer le background 
        for l in range(self.nb_spritesY):
            for c in  range(self.nb_spritesX):
                #construction du background 
                background_pil.paste(matrix_pil_background[l][c], (c*self.size_spriteX, l*self.size_spriteY))
                #dessine un carré bord noir sur chaque tuile
                draw.rectangle( [c*self.size_spriteX, l*self.size_spriteY , (c+1)*self.size_spriteX, (l+1)*self.size_spriteY],
                                outline='black')

        #prépare les masques de zones infranchissables
        self.matrix_mask = [] # matrix_mask[l][c] = masque des tuiles en ligne l et colonne c, 'None' si zone franchissable
        for l in range(self.nb_spritesY):
            self.matrix_mask.append([]) # ligne de masque vierge
            for c in  range(self.nb_spritesX):
                if self.matrix_bloc[l][c]:
                    #encadre la zone avec un carré au bord jaune
                    draw.rectangle( [c*self.size_spriteX, l*self.size_spriteY , (c+1)*self.size_spriteX, (l+1)*self.size_spriteY],
                                    outline='yellow')
                    #calcule le masque correspondantx aux pixels non transparents
                    self.matrix_mask[l].append(pygame.mask.from_surface(
                        pygame.image.fromstring(matrix_pil_bloc[l][c].tobytes(), matrix_pil_bloc[l][c].size, 'RGBA')))
                else:
                    self.matrix_mask[l].append(None)

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
        return self.matrix_bloc[l][c]
    
    def read_sprites(self):
        """ lecture des sprites, retourne le dictionnaire des sprites {'code_sprite': 'filemane.png'}
            ainsi que le dictionnaires des occupations {'code_sprite':TRUE/FALSE}  TRUE signifie sprite infranchissable
        """
        dic_sprites = {}      # dictionnaire des sprites initialisé à vide
        dic_sprites_grid = {} # dictionnaire des occupatons des sprites initialisé à vide
        try:
            # ouverture du fichier Map/map_sprites.txt en lecture seule
            with open(self.path_map + self.sprites_file_name, 'r') as f: 
                for line in f:                  # parcours des lignes du fichier
                    if line[0] != '#':          # on ignore toutes les lignes de commentaires qui commencent par '#'
                        words = line.split('|') # récupère tous les mots séparés par '|' dans une liste
                        #on ajoute dans self.map la liste des codes trouvés sauf retour chariot '\n' et sauf entête 'M'
                        try:
                            code = words[1]               # code sprites
                            file_name = words[2].strip()  # file name de la sprite, avec suppression des espaces
                            try:   #vérification de l'existance du fichier
                                with open(self.path_media + file_name, 'r') as fs:
                                    pass 
                            except:
                                print('Le fichier: "' + self.path_media + file_name+ '" est introuvable.')
                                exit()
                            code_occup = words[4].strip()
                        except: #ficher Map/map_sprites.txt ne respecte pas le bon format
                            print('Le ficher " ' + self.path_map+self.sprites_file_name+'" ne respecte pas le bon format:')
                            print('ligne lue: ', line)
                            exit()
                        dic_sprites[code] = file_name               # ajout de {code : filename} au dictionnaire dic_sprites
                        dic_sprites_grid[code] = (code_occup=='x')  # ajout de {code : True/False} au dictionnaire dic_sprites_grid
                        # ajout de {code: TRUE/FALSE} au dictionnaire correspondant au bloc sur la grille
        except:
            print('Problème avec le fichier: "' + self.path_map+self.sprites_file_name + '"')
            exit()

        #ajout du code '  ' aux dictionnaires, ce code signifiant l'absence d'image
        dic_sprites['  '] = None
        dic_sprites_grid['  '] = False
        #print('Dictionnaire des tuiles:',dic_sprites, '\n CODE OCCUPATIONS:', dic_sprites_grid)
        return dic_sprites, dic_sprites_grid    
        
    def read_map(self, map_file_name):
        """
        lecture d'un fichier MAP (voir fichier modèle.map), retourne les matrices:
            matrix_pil_background[l][c] = image format PIL ligne l, colonne c (en nb de sprites)
            matrix_pil_bloc[l][c] = image format PIL ligne l, colonne c d'un bloc infranchissable ('None' sinon)
            matrix_bloc[l][c] = True/False: True signifie bloc infranchissable
        On connait ainsi pour chaque tuile en [l][c]:
            quelle est l'image à afficher,
            quel est l'image d'un bloc infranchissalbe (None pour un bloc franchissable)
            et le code infranchissable TRUE/FALSE de chaque bloc 
        """
        # préparation de la matrice des codes map, dimension nb_spirteY lignes * nb_spritesX colonnes
        # matrix_map[l][c] = code sprite
        matrix_map, matrix_pil_background, matrix_pil_bloc  = [] , [], []
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
        # matrix_map_pil[l][c] = image ligne l, colonne c
        for l in range(self.nb_spritesY):
            matrix_pil_background.append([]) # ajout d'une ligne vide
            matrix_pil_bloc.append([])       # ajout d'une ligne vide
            for c in range(self.nb_spritesX):
                #ajout de l'image récupérée dans le dictionnaire self.sprites_pil, à partir du code matrix_map[l][c]
                matrix_pil_background[l].append(self.sprites_pil[matrix_map[l][c]])
                if self.sprites_grid[matrix_map[l][c]]: # si le code est un bloc infranchissable (= True)
                    matrix_pil_bloc[l].append(self.sprites_pil[matrix_map[l][c]]) # on le rajoute à matrix_pil_bloc
                else:
                    matrix_pil_bloc[l].append(None) 

        # création matrice des codes True/False pour chaque bloc franchissable ou non
        matrix_bloc =[ [ matrix_pil_bloc[l][c] != None 
                                for c in range(self.nb_spritesX) ]
                                    for l in range(self.nb_spritesY)
                     ]
    
        print(' ... lecture map', map_file_name, len(matrix_pil_background), 'lignes *', len(matrix_pil_background[0]),'colonnes')
        #print('Matrix_bloc:', matrix_bloc)
        return matrix_pil_background, matrix_pil_bloc, matrix_bloc

    def dessine(self):
        """
        méthode de déssin des décors du terrain
        """
        self.screen.blit(self.background_img, (0,0))
