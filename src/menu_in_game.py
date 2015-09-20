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
        self.ecran.blit(self.police.render("Quitter", 1, (255, 255, 255)),
                        (MENU_X + MENU_TXT_CAT_X + MENU_X_CAT,
                         MENU_Y + MENU_TXT_CAT_Y + MENU_Y_CAT * 3 + MENU_SIZE_Y_CAT * 2))

    def next(self):
        self.select = self.select + 1 if self.select + 1 < len(self.categories) else 0

    def double_next(self):
        self.next()
        self.next()

    def previous(self):
        self.select = self.select - 1 if self.select > 0 else len(self.categories) - 1

    def double_previous(self):
        self.previous()
        self.previous()

    def valider_choix(self):
        work = 0

        if self.select == MENU_SAC:
            work = RENDER_INVENTAIRE
        if self.select == MENU_SAUV:
            work = RENDER_SAVE
        if self.select == MENU_QUITTER:
            work = RENDER_GAME
        if self.select == MENU_CARTE:
            work = RENDER_CARTE
        if self.select == MENU_CREATURES:
            work = RENDER_CREATURES

        return work

    def clic(self, xp: int, yp: int):
        pass