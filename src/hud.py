import os
import pygame
from pygame.locals import *


class HUD:
    def __init__(self, ecran):
        self.ecran = ecran

    def update(self):
        self.render()

    def render(self):
        pass


class HUDCombat(HUD):
    def __init__(self, ecran):
        super().__init__(ecran)


class HUDBoutique(HUD):
    def __init__(self, ecran):
        super().__init__(ecran)


class HUDInventaire(HUD):
    def __init__(self, ecran):
        super().__init__(ecran)