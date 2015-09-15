import os
import pygame
from pygame.locals import *
from constantes import *
import random


class Creature:
    def __init__(self, nom, type, niv):
        self.nom = nom
        self.type = type
        self.niv = niv
        self.pseudo = ''
        self.specs = {}


class Creatures:
    def __init__(self):
        self.creatures = ['' for _ in range(MAX_CREATURES)]