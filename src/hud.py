import os
import pygame
from pygame.locals import *


class HUD:
    def __init__(self, ecran):
        self.ecran = ecran
        self.page = 0
        self.max_pages = 10
        self.objet = None

    def update(self, objet):
        self.objet = objet
        self.render()

    def next(self):
        self.page = self.page + 1 if self.page + 1 <= self.max_pages else self.max_pages

    def previous(self):
        self.page = self.page - 1 if self.page - 1 >= 0 else 0

    def render(self):
        return


class HUDCombat(HUD):
    def __init__(self, ecran):
        super().__init__(ecran)


class HUDBoutique(HUD):
    def __init__(self, ecran):
        super().__init__(ecran)


class HUDInventaire(HUD):
    def __init__(self, ecran):
        super().__init__(ecran)


class HUDGear(HUD):
    def __init__(self, ecran):
        super().__init__(ecran)