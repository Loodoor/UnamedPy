import os
import pygame
from pygame.locals import *
from constantes import *


class BoutiqueManager:
    def __init__(self, ecran):
        self.ecran = ecran
        self.page = 0

    def update(self):
        self.render()

    def render(self):
        pass