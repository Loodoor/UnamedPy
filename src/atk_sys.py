import os
import pygame
from pygame.locals import *
from constantes import *
import random
import creatures_mgr


def calcul_degats(degats_basiques: int, specs_atk: list, specs_def: list, coeff_types: int, my_type: int) -> int:
    if specs_atk[ATK_TYP] == my_type:
        x = 1.3
    else:
        x = 1
    return (degats_basiques + specs_atk[SPEC_ATK] / specs_def[SPEC_DEF]) * coeff_types * x


def calcul_esquive(specs_atk: list, specs_def: list) -> bool:
    return True if specs_atk[SPEC_VIT] >= 2 * specs_def[SPEC_VIT] else False


def rencontre_creature(tile_actuelle: int):
    if tile_actuelle == HAUTES_HERBES:
        return True
    return False


class Combat:
    def __init__(self, ecran: pygame.Surface, creature_joueur, types: list=[T_NORMAL]) -> None:
        self.ecran = ecran
        self.compteur_tour = 0
        self.creature_joueur = creature_joueur
        self.seq = types
        types = [T_NORMAL]
        self.adversaire = creatures_mgr.Creature("", -1, T_NORMAL)

    def find_adv(self):
        name_ = ''
        type_ = random.choice(self.seq)
        self.adversaire = creatures_mgr.Creature(name_, type_)

    def mon_tour(self):
        return True if not self.compteur_tour % 2 else False

    def update(self):
        self.compteur_tour += 1
        self.render()

    def render(self):
        pass

    def process_events(self, events: pygame.event):
        for event in events:
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

    def utiliser(self) -> tuple:
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