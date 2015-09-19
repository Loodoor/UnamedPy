import pygame
from pygame.locals import *
import os
from carte import CarteManager


class PNJ:
    def __init__(self, ecran: pygame.Surface, carte_mgr: CarteManager, pos: list, type_mvt: list) -> None:
        self.ecran = ecran
        self.carte_mgr = carte_mgr
        self.pos = pos
        self.type_mvt = type_mvt

    def update(self):
        self.move()
        self.render()

    def move(self):
        pass

    def render(self):
        pass