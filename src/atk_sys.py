# coding=utf-8

import pygame
from pygame.locals import *
from gui import GUIBulle
from constantes import *
from utils import upg_bar
import creatures_mgr
from zones_attaques_manager import ZonesManager


def calcul_degats(degats_basiques: int, specs_atk: list, specs_def: list, coeff_types: int, my_type: int) -> int:
    x = 1.3 if specs_atk[ATK_TYP] == my_type else 1
    return (degats_basiques + specs_atk[SPEC_ATK] / specs_def[SPEC_DEF]) * coeff_types * x


def calcul_esquive(specs_atk: list, specs_def: list) -> bool:
    return True if specs_atk[SPEC_VIT] >= 2 * specs_def[SPEC_VIT] else False


class Combat:
    def __init__(self, ecran: pygame.Surface, creature_joueur, zone: ZonesManager, zone_id: int, indexer, font) -> None:
        self.ecran = ecran
        self.compteur_tour = 0
        self.creature_joueur = creature_joueur
        self.adversaire = creatures_mgr.Creature(0, indexer.get_type_of(0))
        self.zones_mgr = zone
        self.zid = zone_id
        self.indexer = indexer
        self.has_started = False
        self.is_running = True
        self.bulle_que_doit_faire = GUIBulle(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE), "Que doit faire ?", font)

    def find_adv(self):
        self.adversaire = self.zones_mgr.get_new_adversary(self.zid)

    def mon_tour(self):
        return True if not self.compteur_tour % 2 else False

    def get_my_creature(self):
        return self.creature_joueur

    def get_adversary(self):
        return self.adversaire

    def end_fight_for_capture(self):
        self.indexer.capturer(self.get_adversary().get_id())
        self.is_running = False

    def update(self):
        if self.is_running:
            if not self.has_started:
                self.indexer.vu_(self.get_adversary().get_id())
                self.has_started = True

            if self.mon_tour():
                self.bulle_que_doit_faire.set_text("Que doit faire " + self.get_my_creature().get_pseudo() + " ?")
                self.bulle_que_doit_faire.update()

            self.compteur_tour += 1
            self.render()

    def render(self):
        # en attendant d'avoir un paysage
        pygame.draw.rect(self.ecran, (50, 50, 180), (COMB_X, COMB_Y, COMB_SX, COMB_SY))
        # affichage des créatures
        self.ecran.blit(self.indexer.get_image_by_id(self.get_adversary().get_id()), (COMB_X_ADV, COMB_Y_ADV))
        self.ecran.blit(self.indexer.get_image_by_id(self.get_my_creature().get_id()), (COMB_X_ME, COMB_Y_ME))
        # affichage des stats
        upg_bar(self.ecran, (COMB_X_ADV, COMB_Y_ADV - COMB_SY_LIFE_BAR - 10, COMB_SX_LIFE_BAR, COMB_SY_LIFE_BAR),
                self.get_adversary().get_pvs() // self.get_adversary().get_max_pvs() * (COMB_SX_LIFE_BAR - BAR_ESP * 2))
        upg_bar(self.ecran, (COMB_X_ME, COMB_Y_ME - COMB_SY_LIFE_BAR - 10, COMB_SX_LIFE_BAR, COMB_SY_LIFE_BAR),
                self.get_my_creature().get_pvs() // self.get_my_creature().get_max_pvs() * (COMB_SX_LIFE_BAR - BAR_ESP * 2))


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