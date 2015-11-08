# coding=utf-8

import pygame
import os
import pickle
from pygame.locals import *
from exceptions import CreaturesNonTrouvees
from constantes import *
import textwrap as tw


class Element:
    def __init__(self, name: str, id: int, type: int, path: str, desc: str=""):
        self.name = name
        self.id = id
        self.type = type
        self.path = path
        self.description = desc
        self.vu = False
        self.capture = False

    def vu_(self):
        self.vu = True

    def capture_(self):
        self.capture = True


class Typeur:
    def __init__(self):
        self.types = {
            T_TENEBRE: {
                'default': "ténèbre",
                'user': ''
            },
            T_LUMIERE: {
                'default': "lumière",
                'user': ''
            },
            T_FEU: {
                'default': "feu",
                'user': ''
            },
            T_NORMAL: {
                'default': "normal",
                'user': ''
            },
            T_AIR: {
                'default': "air",
                'user': ''
            },
            T_EAU: {
                'default': "eau",
                'user': ''
            },
            T_ELEC: {
                'default': "électrique",
                'user': ''
            },
            T_PLANTE: {
                'default': "plante",
                'user': ''
            },
            T_PLASMA: {
                'default': "plasma",
                'user': ''
            },
            T_TERRE: {
                'default': "terre",
                'user': ''
            }
        }
        self.path = os.path.join("..", "saves", "types" + EXTENSION)

        self.user_types = {}

    def __create_user_type(self):
        self.user_types = {}
        for k, v in self.types.items():
            self.user_types[k] = v['user']

    def change_name(self, type: int, new_name: str):
        if type in self.types.keys():
            self.types[type]['user'] = new_name
        self.__create_user_type()

    def get_name(self, type: int):
        return self.types[type]['user']

    def get_default_name(self, type: int):
        return self.types[type]['default']

    def get_types(self):
        return self.user_types

    @staticmethod
    def count_types():
        return TYPES_NUMBER

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as type_rb:
                self.types = pickle.Unpickler(type_rb).load()
        self.__create_user_type()

    def save(self):
        with open(self.path, "wb") as type_wb:
            pickle.Pickler(type_wb).dump(self.types)


class Indexer:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont, render_manager):
        self.ecran = ecran
        self.police = police
        self.save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        self.page = 0
        self.max_page = 10
        self.par_page = 10
        self.indexer = []
        self.typeur = Typeur()
        self.render_creatures = True
        self.rd_mgr = render_manager
        self.selected_creature = -1
        self.selected_type = -1

    @staticmethod
    def add_new(name: str, id: int, type: int, path: str, desc: str=""):
        save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        if os.path.exists(save_path):
            with open(save_path, 'rb') as rbin:
                tod = pickle.Unpickler(rbin).load()
                tod.append(Element(name, id, type, path, desc))
                pickle.Pickler(open(save_path, 'wb')).dump(tod)
        else:
            with open(save_path, 'wb') as wbin:
                tod = [Element(name, id, type, path, desc)]
                pickle.Pickler(wbin).dump(tod)

    def load(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "rb") as read_index:
                self.indexer = pickle.Unpickler(read_index).load()
        else:
            raise CreaturesNonTrouvees()
        self.typeur.load()

    def save(self):
        with open(self.save_path, "wb") as save_index:
            pickle.Pickler(save_index).dump(self.indexer)
        self.typeur.save()

    def next(self):
        self.page = self.page + 1 if self.page <= self.max_page else self.max_page

    def previous(self):
        self.page = self.page - 1 if self.page - 1 >= 0 else 0

    def get_type_of(self, id: int):
        for creature in self.indexer:
            if creature.id == id:
                return creature.type
        return POK_SEARCH_ERROR

    def get_typeur(self):
        return self.typeur

    def vu_(self, id: int):
        for elem in self.indexer:
            if id == elem.id:
                elem.vu_()
                break

    def capture_(self, id: int):
        for elem in self.indexer:
            if id == elem.id:
                elem.capture_()
                break

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (180, 20, 180), (POK_POSX, POK_POSY, POK_X_SIZE, POK_Y_SIZE))
        titre = self.police.render("Indexeur" if self.render_creatures else "Indexer -> Types", 1, (255, 255, 255))
        self.ecran.blit(titre, (POK_X_TITRE, POK_Y_TITRE))
        pygame.draw.rect(self.ecran, (20, 20, 180), (POK_X_VIEWT, POK_Y_VIEWT, POK_SX_VIEWT, POK_SY_VIEWT))
        tmp = self.police.render("Types" if not self.render_creatures else "Créatures", 1, (255, 255, 255))
        self.ecran.blit(tmp, (POK_X_VIEWT + (POK_SX_VIEWT - tmp.get_width()) // 2, POK_Y_VIEWT + 4))

        i = 0
        if self.render_creatures:
            for elem in self.indexer:
                nom = elem.name
                vu, capture, type_ = elem.vu, elem.capture, elem.type

                if not vu and not capture:
                    nom = "???"
                    type_ = "???"

                self.ecran.blit(self.police.render(str(nom) + " - Type : " + str(type_), 1, (255, 255, 255)),
                                (POK_X_NAME_CREA, POK_Y_NAME_CREA + POK_ESP_Y_ITEM * i))

                if self.selected_creature == i:
                    j = 0
                    for txt in tw.wrap(elem.description, width=38):
                        self.ecran.blit(self.police.render(txt, 1, (255, 255, 255)),
                                        (POK_X_DESC, POK_Y_DESC + j * POK_ESP_Y_ITEM))
                        j += 1

                i += 1
        else:
            for t_id, type_name in self.typeur.get_types().items():
                texte = self.police.render(str(t_id + 1) + " -> '" + type_name + "'", 1, (255, 255, 255))
                self.ecran.blit(texte, (POK_X_TYPE, POK_Y_TYPE + i * POK_SY_TYPE))
                i += 1

    def clic(self, xp: int, yp: int):
        if POK_X_VIEWT <= xp <= POK_X_VIEWT + POK_SX_VIEWT and POK_Y_VIEWT <= yp <= POK_Y_VIEWT + POK_SY_VIEWT:
            self.render_creatures = not self.render_creatures
        if self.render_creatures and POK_X_NAME_CREA <= xp <= POK_X_NAME_CREA + 200:
            self.selected_creature = (yp - POK_Y_NAME_CREA) // POK_ESP_Y_ITEM
            self.selected_creature = self.selected_creature if 0 <= self.selected_creature < len(self.indexer) else -1
        if not self.render_creatures and POK_X_TYPE <= xp <= POK_X_TYPE + 200:
            self.selected_type = (yp - POK_Y_TYPE) // POK_SY_TYPE
            self.selected_type = self.selected_type if 0 <= self.selected_type < self.typeur.count_types() else -1