import pygame
import os
import pickle
from pygame.locals import *
from constantes import *


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
            T_TENEBRE: "ténèbre",
            T_LUMIERE: "lumière",
            T_FEU: "feu",
            T_NORMAL: "normal",
            T_AIR: "air",
            T_EAU: "eau",
            T_ELEC: "électrique",
            T_PLANTE: "plante",
            T_PLASMA: "plasma",
            T_TERRE: "terre"
        }
        self.path = os.path.join("..", "saves", "types" + EXTENSION)

    def change_name(self, type: int, new_name: str):
        if type in self.types.keys():
            self.types[type] = new_name

    def get_name(self, type: int):
        return self.types[type]

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as type_rb:
                self.types = pickle.Unpickler(type_rb).load()

    def save(self):
        with open(self.path, "wb") as type_wb:
            pickle.Pickler(type_wb).dump(self.types)


class Indexer:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont):
        self.ecran = ecran
        self.police = police
        self.save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        self.page = 0
        self.max_page = 10
        self.par_page = 10
        self.indexer = []

    @staticmethod
    def add_new(name: str, id: int, type: int, path: str, desc: str=""):
        save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        if os.path.exists(save_path):
            with open(save_path, 'rb') as rbin:
                tod = pickle.Unpickler(rbin).load() + [Element(name, id, type, path, desc)]
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
            pass
            #raise NotImplementedError("Désolé, aucune créature ne semble exister")

    def save(self):
        with open(self.save_path, "wb") as save_index:
            pickle.Pickler(save_index).dump(self.indexer)

    def next(self):
        self.page = self.page + 1 if self.page <= self.max_page else self.max_page

    def previous(self):
        self.page = self.page - 1 if self.page - 1 >= 0 else 0

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
        self.ecran.blit(self.police.render("Indexeur", 1, (255, 255, 255)), (POK_X_TITRE, POK_Y_TITRE))
        i = 0
        for elem in self.indexer:
            nom = elem.name
            vu, capture, type_ = elem.vu, elem.capture, elem.type

            #if not vu and not capture:
            #    nom = "???"
            #    type_ = "???"

            self.ecran.blit(self.police.render(str(nom) + " - " + str(type_), 1, (255, 255, 255)),
                            (POK_X_NAME_CREA, POK_Y_NAME_CREA + POK_ESP_Y_ITEM * i))
            i += 1