import os
import pygame
from pygame.locals import *
from constantes import *


class Personnage:
    def __init__(self, ecran):
        self.ecran = ecran

    def move(self, direction=+1):
        pass

    def update(self):
        self.render()

    def render(self):
        pass