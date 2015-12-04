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
        self.has_attacked = False
        self.is_running = True
        self.bulle_que_doit_faire = GUIBulle(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE), "Que doit faire ?", font)
        self.indic_captured = pygame.image.load(os.path.join("..", "assets", "gui", "captured.png")).convert_alpha()
        self.font = font

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
                self.get_my_creature().add_attack("test", T_EAU, 50, "TEST d'attaque de type eau", [10, MAX_PP_PER_ATK])
                self.get_my_creature().add_attack("test2", T_EAU, 50, "TEST d'attaque de type eau", [10, MAX_PP_PER_ATK])
                self.get_my_creature().add_attack("test3", T_EAU, 50, "TEST d'attaque de type eau", [10, MAX_PP_PER_ATK])
                self.get_my_creature().add_attack("test4", T_EAU, 50, "TEST d'attaque de type eau", [10, MAX_PP_PER_ATK])

            self.render()

            if self.mon_tour():
                self.bulle_que_doit_faire.set_text("Que doit faire " + self.get_my_creature().get_pseudo() + " ?")
                self.bulle_que_doit_faire.update()

                if self.has_attacked:
                    self.compteur_tour += 1
                    self.has_attacked = False

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
        # affichage des noms des créatures
        if self.indexer.get_captured(self.get_adversary().get_id()):
            self.ecran.blit(self.indexer.get_by_id(self.get_adversary()).get_pseudo(),
                            (COMB_X_ADV, COMB_Y_ADV - COMB_SY_TXT_NAME))
        else:
            self.ecran.blit(self.font.render("???", 1, (10, 10, 10)),
                            (COMB_X_ADV, COMB_Y_ADV - COMB_SY_TXT_NAME - COMB_SY_LIFE_BAR - 10))
        self.ecran.blit(self.font.render(self.get_my_creature().get_pseudo(), 1, (10, 10, 10)),
                        (COMB_X_ME, COMB_Y_ME - COMB_SY_TXT_NAME - COMB_SY_LIFE_BAR - 10))
        # affichage d'un indicateur pour dire s'il on a déjà capturé la créature adverse ou non
        if self.indexer.get_captured(self.get_adversary()):
            self.ecran.blit(self.indic_captured, (COMB_X_ADV + COMB_CHECK_SX + 10, COMB_Y_ADV - COMB_SY_TXT_NAME))
        # affichage du choix des attaques
        i = 0
        for atk in self.get_my_creature().get_attacks():
            pygame.draw.rect(self.ecran, (180, 180, 50), (COMB_X_ADV, COMB_Y_ADV + COMB_SY_ADV + 20 * i, 150, 20))
            self.ecran.blit(self.font.render(atk.get_nom() +
                                             ", dégâts: " + str(atk.get_dgts()) +
                                             ", description: " + atk.get_texte(), 1, (10, 10, 10)),
                            (COMB_X_ADV, COMB_Y_ADV + COMB_SY_ADV + (COMB_SY_ATK_FIELD + 10) * i,
                             COMB_SX_ATK_FIELD, COMB_SY_ATK_FIELD))
            i += 1