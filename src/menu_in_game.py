import pygame
from pygame.locals import *
import os
from constantes import *


class Menu:
    def __init__(self, ecran: pygame.Surface) -> None:
        self.ecran = ecran
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

    def render(self):
        pygame.draw.rect(self.ecran, (50, 80, 180), (MENU_X, MENU_Y, MENU_SIZE_X, MENU_SIZE_Y))

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

    def clic(self, xp: int, yp: int):
        pass