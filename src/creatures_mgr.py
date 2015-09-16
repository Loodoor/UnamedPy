import os
import pygame
from pygame.locals import *
from constantes import *
import random


class Creature:
    def __init__(self, nom: str, type: int, niv: tuple) -> None:
        self.nom = nom
        self.type = type
        self.niv = random.randint(niv[0], niv[1])
        self.pseudo = ''
        self.specs = {}
        self.upgrade_range = UPGRADE_RANGE_SPEC

    def set_pseudo(self, new):
        self.pseudo = new

    def get_pseudo(self):
        return self.pseudo

    def set_spec(self, categorie, new):
        if categorie in self.specs.keys():
            self.specs[categorie] = new

    def level_up(self):
        self.niv = self.niv + 1 if self.niv + 1 <= MAX_LEVEL else MAX_LEVEL
        for i in self.specs.keys():
            self.upgrade_spec(i)

    def upgrade_spec(self, categorie):
        if categorie in self.specs.keys():
            tmp = self.specs[categorie] + random.randrange(self.upgrade_range[0], self.upgrade_range[1])
            self.specs[categorie] = tmp if tmp <= MAX_VAL_SPEC else MAX_VAL_SPEC

    def get_specs(self):
        return self.specs