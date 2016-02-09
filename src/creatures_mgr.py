# coding=utf-8

from exceptions import CategorieInexistante, ErreurDeCreationDeClass
from constantes import *
from utils import uset_image_as_shiney
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
            return self.attaque[ATK_DEGATS]
        return 0

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
    def __init__(self, id: int, type_: int, alea_niv: tuple or int=(10, 20) or 10, specs_range: tuple=(2, 10),
                 pvs_range: tuple=(18, 27), indexer=None) -> None:
        if not indexer:
            raise ErreurDeCreationDeClass

        self.specs = {
            SPEC_ATK: random.randint(*specs_range),
            SPEC_DEF: random.randint(*specs_range),
            SPEC_VIT: random.randint(*specs_range),
            SPEC_ID: id,
            SPEC_TYP: type_,
            SPEC_NOM: '',
            SPEC_NIV: random.randint(*alea_niv) if isinstance(alea_niv, tuple) else alea_niv,
            SPEC_PVS: random.randint(*pvs_range),
            SPEC_XP: 0
        }
        self.specs[SPEC_MAX_PVS] = self.specs[SPEC_PVS]  # quand on crée la créature, les pvs max = pvs actuel
        self.upgrade_range = UPGRADE_RANGE_SPEC
        self.attaques = []
        self.dead = False
        self.__shiney = True if random.random() <= SPEC_PROBA_SHINEY else False
        self.__image = indexer.get_image_by_id(self.specs[SPEC_ID]) if not self.is_shiney() else \
            uset_image_as_shiney(indexer.get_image_by_id(self.specs[SPEC_ID]))
        self._images_resized = {
            self.__image.get_size(): self.__image
        }

    def get_image(self):
        return self.__image

    def get_image_with_size(self, size: tuple):
        if size not in self._images_resized.keys():
            self._images_resized[size] = pygame.transform.scale(self.__image, size)
        return self._images_resized[size]

    def is_shiney(self):
        return self.__shiney

    def is_dead(self):
        return self.dead

    def _calc_seuil_xp(self):
        return int(SPEC_SEUIL_XP_LVL_UP / 2 * math.sqrt(self.get_niv() + 1) * 0.9)

    def get_seuil_xp(self):
        return self._calc_seuil_xp()

    def get_xp(self):
        return self.specs[SPEC_XP]

    def gagner_xp(self, adv):
        gain = random.randint(
            int(SPEC_XP_GAGNE * math.sqrt(adv.get_niv() + 1) * random.randint(30, 75) / 100),
            int(SPEC_XP_GAGNE * math.sqrt(adv.get_niv() + 1) * random.randint(75, 125) / 100)
        )
        self.specs[SPEC_XP] += gain

        if self.specs[SPEC_XP] >= self._calc_seuil_xp():
            levels_ups = []
            for _ in range(self.specs[SPEC_XP] // self._calc_seuil_xp()):
                levels_ups.append(self._level_up())
            self.specs[SPEC_XP] %= self._calc_seuil_xp()
            self.specs[SPEC_PVS] = self.specs[SPEC_MAX_PVS]
            return levels_ups
        else:
            return gain

    def taper(self, dgts):
        self.specs[SPEC_PVS] -= dgts
        if self.get_pvs() <= 0:
            self.dead = True
            self.specs[SPEC_PVS] = 0

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
        # on ne doit pas pouvoir manipuler l'xp
        if categorie in self.specs.keys() and categorie != SPEC_XP:
            self.specs[categorie] = new
        else:
            raise CategorieInexistante

    def get_niv(self):
        return self.specs[SPEC_NIV]

    def get_max_pvs(self):
        return self.specs[SPEC_MAX_PVS]

    def get_pvs(self):
        return self.specs[SPEC_PVS]

    def _level_up(self):
        if self.specs[SPEC_NIV] + 1 <= MAX_LEVEL:
            self.specs[SPEC_NIV] += 1
            won = {}
            for i in [SPEC_ATK, SPEC_DEF, SPEC_VIT, SPEC_MAX_PVS]:
                won[i] = self.upgrade_spec(i)
            return won
        return {}

    def upgrade_spec(self, categorie):
        if categorie in self.specs.keys():
            gain = random.randrange(*self.upgrade_range)
            tmp = self.specs[categorie] + gain
            self.specs[categorie] = tmp if tmp <= MAX_VAL_SPEC else MAX_VAL_SPEC
            return gain
        return -1

    def get_specs(self):
        return self.specs