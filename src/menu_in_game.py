# coding=utf-8

import pygame
from pygame.locals import *
import os
from constantes import *


class Menu:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.Font) -> None:
        self.ecran = ecran
        self.police = police
        self.select = 0
        self.categories = [
            MENU_CREATURES,
            MENU_SAC,
            MENU_CARTE,
            MENU_SAUV,
            MENU_POKEDEX,
            MENU_QUITTER
        ]

    def update(self):
        self.render()
        self.render_categories()

    def render(self):
        pygame.draw.rect(self.ecran, (50, 80, 180), (MENU_X, MENU_Y, MENU_SIZE_X, MENU_SIZE_Y))

    def render_categories(self):
        color = (180, 50, 50) if self.categories[0] != self.select else (50, 180, 50)
        pygame.draw.rect(self.ecran, color, (MENU_X + MENU_X_CAT,
                                             MENU_Y + MENU_Y_CAT,
                                             MENU_SIZE_X_CAT, MENU_SIZE_Y_CAT))
        self.ecran.blit(self.police.render("Créatures", 1, (255, 255, 255)), (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT,
                                                                     MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT))

        color = (180, 50, 50) if self.categories[1] != self.select else (50, 180, 50)
        pygame.draw.rect(self.ecran, color, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                                             MENU_Y + MENU_Y_CAT,
                                             MENU_SIZE_X_CAT, MENU_SIZE_Y_CAT))
        self.ecran.blit(self.police.render("Inventaire", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT))

        color = (180, 50, 50) if self.categories[2] != self.select else (50, 180, 50)
        pygame.draw.rect(self.ecran, color, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                                             MENU_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT,
                                             MENU_SIZE_X_CAT, MENU_SIZE_Y_CAT))
        self.ecran.blit(self.police.render("Carte", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT))

        color = (180, 50, 50) if self.categories[3] != self.select else (50, 180, 50)
        pygame.draw.rect(self.ecran, color, (MENU_X + MENU_X_CAT,
                                             MENU_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT,
                                             MENU_SIZE_X_CAT, MENU_SIZE_Y_CAT))
        self.ecran.blit(self.police.render("Sauvegarder", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 2 + MENU_SIZE_Y_CAT))

        color = (180, 50, 50) if self.categories[4] != self.select else (50, 180, 50)
        pygame.draw.rect(self.ecran, color, (MENU_X + MENU_X_CAT,
                                             MENU_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2,
                                             MENU_SIZE_X_CAT, MENU_SIZE_Y_CAT))
        self.ecran.blit(self.police.render("Pokédex", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))

        color = (180, 50, 50) if self.categories[5] != self.select else (50, 180, 50)
        pygame.draw.rect(self.ecran, color, (MENU_X + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                                             MENU_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2,
                                             MENU_SIZE_X_CAT, MENU_SIZE_Y_CAT))
        self.ecran.blit(self.police.render("Retour", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT + MENU_X_CAT * 2 + MENU_SIZE_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))

    def next(self):
        self.select = self.select + 1 if self.select + 1 < len(self.categories) else 0

    def previous(self):
        self.select = self.select - 1 if self.select > 0 else len(self.categories) - 1

    def valider_choix(self):
        if self.select == MENU_SAC:
            work = RENDER_INVENTAIRE
        elif self.select == MENU_SAUV:
            work = RENDER_SAVE
        elif self.select == MENU_QUITTER:
            work = RENDER_GAME
        elif self.select == MENU_CARTE:
            work = RENDER_CARTE
        elif self.select == MENU_CREATURES:
            work = RENDER_CREATURES
        elif self.select == MENU_POKEDEX:
            work = RENDER_POKEDEX
        else:
            work = RENDER_ERROR

        return work

    def clic(self, xp: int, yp: int):
        real_x, real_y = (xp - MENU_X) // MENU_SIZE_X_CAT, (yp - MENU_Y) // MENU_SIZE_Y_CAT
        if (real_x, real_y) == (0, 0):
            self.select = MENU_CREATURES
        if (real_x, real_y) == (1, 0):
            self.select = MENU_SAC
        if (real_x, real_y) == (0, 1):
            self.select = MENU_SAUV
        if (real_x, real_y) == (1, 1):
            self.select = MENU_CARTE
        if (real_x, real_y) == (0, 2):
            self.select = MENU_POKEDEX
        if (real_x, real_y) == (1, 2):
            self.select = MENU_QUITTER
        return self.valider_choix()

    def mouseover(self, pos: tuple):
        real_x = (pos[0] - MENU_X) // MENU_SIZE_X_CAT
        real_y = (pos[1] - MENU_Y) // MENU_SIZE_Y_CAT

        if (real_x, real_y) == (0, 0):
            self.select = MENU_CREATURES
        if (real_x, real_y) == (1, 0):
            self.select = MENU_SAC
        if (real_x, real_y) == (0, 1):
            self.select = MENU_SAUV
        if (real_x, real_y) == (1, 1):
            self.select = MENU_CARTE
        if (real_x, real_y) == (0, 2):
            self.select = MENU_POKEDEX
        if (real_x, real_y) == (1, 2):
            self.select = MENU_QUITTER