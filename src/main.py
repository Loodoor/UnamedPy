# coding=utf-8

import os
from exceptions import ErreurRepertoire

if os.path.split(os.getcwd())[1] != "src":
    raise ErreurRepertoire("Le répertoire courant n'est pas correct, le jeu ne peut pas se lancer")
print("Chargement ...")

import game
import pygame
from pygame.locals import *
from constantes import *
import utils


def main():
    pygame.init()

    ecran = pygame.display.set_mode((FEN_large, FEN_haut), HWSURFACE)
    pygame.display.set_caption("Unamed")

    print("Appuyez sur 'J' pour lancer le jeu")

    continuer = 1

    temp = utils.ULoader()
    temp.load()
    del temp

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

    print("Le programme s'est terminé proprement")

if __name__ == '__main__':
    main()