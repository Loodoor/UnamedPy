import os
import pygame
from pygame.locals import *
from constantes import *
import random


class Creature:
    def __init__(self, nom: str, type: int, niv: tuple) -> None:
        self.specs = {
            SPEC_ATK: 0,
            SPEC_DEF: 0,
            SPEC_VIT: 0,
            SPEC_CREA: nom,
            SPEC_TYP: type,
            SPEC_NOM: '',
            SPEC_NIV: random.randint(niv[0], niv[1]),
            SPEC_PVS: 20
        }
        self.upgrade_range = UPGRADE_RANGE_SPEC

    def set_pseudo(self, new):
        self.specs[SPEC_NOM] = new

    def get_pseudo(self):
        return self.specs[SPEC_NOM] if self.specs[SPEC_NOM] != '' else self.specs[SPEC_CREA]

    def set_spec(self, categorie, new):
        if categorie in self.specs.keys():
            self.specs[categorie] = new

    def get_niv(self):
        return self.specs[SPEC_NIV]

    def level_up(self):
        if self.specs[SPEC_NIV] + 1 <= MAX_LEVEL:
            self.specs[SPEC_NIV] += 1
            for i in [SPEC_ATK, SPEC_DEF, SPEC_VIT, SPEC_PVS]:
                self.upgrade_spec(i)

    def upgrade_spec(self, categorie):
        if categorie in self.specs.keys():
            tmp = self.specs[categorie] + random.randrange(self.upgrade_range[0], self.upgrade_range[1])
            self.specs[categorie] = tmp if tmp <= MAX_VAL_SPEC else MAX_VAL_SPEC

    def get_specs(self):
        return self.specs