#!/usr/bin/env python3
# reduction en masse d'images stockées dans un répertoire


from PIL import Image

from os import listdir
from os.path import isfile, join, splitext


mypath = input("Dans quel dossier sont les images ? ")
imageFiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
ratio = int(input("quel ratio de réduction appliquer ?"))

for im in imageFiles:
    fileName, fileExtension = splitext(join(mypath,im))
    im1 = Image.open(join(mypath,im))
    originalWidth, originalHeight = im1.size
    width, height = int(originalWidth/ratio), int(originalHeight/ratio) 
    im2 = im1.resize((width, height), Image.ANTIALIAS)
    fileNameTarget= fileName +"_"+str(width)+"x"+str(height) + fileExtension
    im2.save(fileNameTarget)
    print (im, "de taille initiale",im1.size , "redimensionnée en", im2.size)
print ("Travail terminé !", len(imageFiles), "images redimensionnées.")

