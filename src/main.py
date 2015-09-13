import os
import game
import pygame
from pygame.locals import *
from constantes import *

pygame.init()

ecran = pygame.display.set_mode((FEN_large, FEN_haut), HWSURFACE)
pygame.display.set_caption("Unamed")
continuer = 1
jeu = game.Game(ecran)

while continuer:
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            continuer = 0
        if event.type == KEYDOWN:
            if event.key == K_j:
                jeu.start()

    #Affichage
    pygame.draw.rect(ecran, (25, 66, 145), (0, 0) + ecran.get_size())

    pygame.display.flip()

pygame.quit()

print("Exited cleanly")