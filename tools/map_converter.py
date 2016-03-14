__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

import os
import glob
import pickle
from constantes import *


class SubCarte:
    """
    chaque carte crée ses propres PNJ et s'occupe de les afficher
    chaque carte s'occupe aussi de gérer ses objets (au sol), et les chemins vers d'autres cartes
    elles gérent aussi leur ZID
    """
    def __init__(self, carte: list, objets: dict, buildings: dict, zid: int, pnjs: list, spawns: dict, triggers: dict, id_: int):
        self.carte = carte
        self.objets = objets
        self.buildings = buildings
        self.zid = zid
        self.pnjs = pnjs
        self.spawns = spawns
        self.triggers = triggers
        self.id = id_

    def create_pnj(self, pnj):
        self.pnjs.append(pnj)

    def add_building(self, x: int, y: int, id_: int):
        self.buildings[x, y] = id_

    def get_all(self):
        return self.carte

    def get_at(self, x: int, y: int):
        return self.carte[y][x]

    def get_objects(self):
        return self.objets

    def building_at(self, x: int, y: int):
        return True if (x, y) in self.buildings.keys() else False

    def get_spawn_pos_with_id(self, id_: int):
        for pos, map_id in self.spawns.items():
            if map_id == id_:
                return pos
        return None

    def get_building_id_at(self, x: int, y: int):
        if self.building_at(x, y):
            return str(self.buildings[x, y])
        return BUILDING_GET_ERROR

    def get_zid(self):
        return self.zid

    def size(self):
        return len(self.carte[0]), len(self.carte)

    def get_object_at(self, x: int, y: int):
        if (x, y) in self.objets.keys():
            work = self.objets[x, y]
            del self.objets[x, y]
            return work
        return OBJET_GET_ERROR

    def set_all(self, new: list):
        self.carte = new

    def set_at(self, x: int, y: int, new):
        self.carte[y][x] = new

    def collide_at(self, x: int, y: int):
        if 0 <= int(y) < len(self.carte) and 0 <= int(x) < len(self.carte[0]):
            return True if COLLIDE_ITEM(self.carte[int(y)][int(x)][1]) else False
        return True

    def trigger_at(self, x: int, y: int):
        return (x, y) in self.triggers.keys()

    def call_trigger_at(self, x: int, y: int, triggers_mgr):
        if self.trigger_at(x, y):
            triggers_mgr.call_trigger_with_id(self.triggers[x, y], self.id)
            return True
        return False

    def has_object(self, x: int, y: int):
        return True if (x, y) in self.objets.keys() else False

    def drop_object_at(self, x: int, y: int, obj, from_poche):
        if (x, y) not in self.objets:
            self.objets[x, y] = [obj, from_poche]
        else:
            self.drop_object_at(x, y - 1, obj, from_poche)


def run():
    for file in glob.glob(os.path.join("..", "assets", "map", "*.umd")):
        old = pickle.Unpickler(open(file, 'rb')).load()
        carte, objets, buildings, zid, pnjs, spawns = old
        pickle.Pickler(open(file, 'wb')).dump(SubCarte(carte, objets, buildings, zid, pnjs, spawns, {}, os.path.split(file)[1].replace('.umd', '')[3:]))


if __name__ == '__main__':
    run()