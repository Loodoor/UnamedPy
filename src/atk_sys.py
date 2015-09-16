import os
import pygame
from pygame.locals import *
from constantes import *


def calcul_degats(degats_basiques, specs_atk, specs_def, coeff):
    return (degats_basiques + specs_atk[SPEC_ATK] / specs_def[SPEC_DEF]) * coeff


def calcul_esquive(specs_atk, specs_def):
    return True if specs_atk[SPEC_VIT] >= 2 * specs_def[SPEC_VIT] else False


def rencontre_creature(tile_actuelle):
    if tile_actuelle == HAUTES_HERBES:
        pass


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
            return self.attaque[ATK_DEGATS], self.attaque[ATK_TYP]
        return ATK_IMPOSSIBLE

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
        self.attaque[ATK_PPS][ATK_MAX_PP] = self.attaque[ATK_PPS][ATK_MAX_PP] + add if self.attaque[ATK_PPS][ATK_MAX_PP] \
            + add <= MAX_PP_PER_ATK else self.attaque[ATK_PPS][ATK_MAX_PP]
        self.attaque[ATK_PPS][ATK_PP] = self.attaque[ATK_PPS][ATK_MAX_PP]

    def soigne_pps(self):
        self.attaque[ATK_PPS][ATK_PP] = self.attaque[ATK_PPS][ATK_MAX_PP]