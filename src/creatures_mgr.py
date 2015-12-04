# coding=utf-8

import os
import pygame
from pygame.locals import *
from constantes import *
import random


class Attaque:
    def __init__(self, nom: str, type: int, degats: int, texte: str, pp: list):
        self.attaque = {
            ATK_NOM: nom,
            ATK_TYP: type,
            ATK_DEGATS: degats,
            ATK_TXT: texte,
            ATK_PPS: pp
        }

    def utiliser(self):
        if self.attaque[ATK_PPS][ATK_PP] > 0:
            self.attaque[ATK_PPS][ATK_PP] -= 1

    def get_nom(self):
        return self.attaque[ATK_NOM]

    def get_type(self):
        return self.attaque[ATK_TYP]

    def get_texte(self):
        return self.attaque[ATK_TXT]

    def get_dgts(self):
        return self.attaque[ATK_DEGATS]

    def get_pps(self):
        return self.attaque[ATK_PPS]

    def increase_pps(self, add):
        self.attaque[ATK_PPS][ATK_MAX_PP] = self.attaque[ATK_PPS][ATK_MAX_PP] + add \
            if self.attaque[ATK_PPS][ATK_MAX_PP] + add <= MAX_PP_PER_ATK else self.attaque[ATK_PPS][ATK_MAX_PP]
        self.attaque[ATK_PPS][ATK_PP] = self.attaque[ATK_PPS][ATK_MAX_PP]

    def soigne_pps(self):
        self.attaque[ATK_PPS][ATK_PP] = self.attaque[ATK_PPS][ATK_MAX_PP]


class Creature:
    def __init__(self, id: int, type: int, alea_niv: tuple=(10, 20), specs_range: tuple=(2, 10), pvs_range: tuple=(18, 27)) -> None:
        self.specs = {
            SPEC_ATK: random.randint(*specs_range),
            SPEC_DEF: random.randint(*specs_range),
            SPEC_VIT: random.randint(*specs_range),
            SPEC_ID: id,
            SPEC_TYP: type,
            SPEC_NOM: '',
            SPEC_NIV: random.randint(alea_niv[0], alea_niv[1]),
            SPEC_PVS: random.randint(*pvs_range),
        }
        self.specs[SPEC_MAX_PVS] = self.specs[SPEC_PVS]  # quand on crée la créature, les pvs max = pvs actuel
        self.upgrade_range = UPGRADE_RANGE_SPEC
        self.attaques = []
        self.dead = False

    def is_dead(self):
        return self.dead

    def taper(self, dgts):
        self.specs[SPEC_PVS] -= dgts
        if self.get_pvs() <= 0:
            self.dead = True

    def set_pseudo(self, new):
        self.specs[SPEC_NOM] = new

    def get_pseudo(self):
        return self.specs[SPEC_NOM] if self.specs[SPEC_NOM] != '' else "???"

    def get_type(self):
        return self.specs[SPEC_TYP]

    def add_attack(self, name: str, type: int, dgts: int, desc: str, pps: list):
        self.attaques.append(Attaque(name, type, dgts, desc, pps))

    def get_attacks(self):
        return self.attaques[-4:]

    def get_id(self):
        return self.specs[SPEC_ID]

    def set_spec(self, categorie, new):
        if categorie in self.specs.keys():
            self.specs[categorie] = new

    def get_niv(self):
        return self.specs[SPEC_NIV]

    def get_max_pvs(self):
        return self.specs[SPEC_MAX_PVS]

    def get_pvs(self):
        return self.specs[SPEC_PVS]

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