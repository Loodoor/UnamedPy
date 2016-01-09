# coding=utf-8

from os import path
from constantes import *
import pickle
from random import choice
from indexer import Indexer


class Zone:
    def __init__(self, id: str, creatures_id: list, level_range: tuple):
        self.id = id  # c'est l'id d'une subCarte
        self.creatures_id = creatures_id
        self.level_range = level_range

    def get_id(self):
        return self.id

    def get_new_adversaire(self, indexer: Indexer):
        id_ = choice(self.creatures_id)
        type_ = indexer.get_type_of(id_)
        return id_, type_, self.level_range


class ZonesManager:
    def __init__(self, indexer: Indexer):
        self.indexer = indexer
        self.path = path.join("..", "saves", "zones" + EXTENSION)
        self.zones = []

    @staticmethod
    def add_new_zone_to_path(zone: Zone):
        path_ = path.join("..", "saves", "zones" + EXTENSION)
        if path.exists(path_):
            with open(path_, 'rb') as read_zones:
                sv = pickle.Unpickler(read_zones).load()
                sv.append(zone)
                pickle.Pickler(open(path_, 'wb')).dump(sv)
        else:
            with open(path_, 'wb') as add_new:
                pickle.Pickler(add_new).dump([zone])

    def get_new_adversary(self, with_zoneid: int):
        for zone in self.zones:
            if zone.get_id() == with_zoneid:
                return zone.get_new_adversaire(self.indexer)
        return ZONE_ADV_ERROR

    def load(self):
        if path.exists(self.path):
            with open(self.path, 'rb') as zones_rb:
                self.zones = pickle.Unpickler(zones_rb).load()

    def save(self):
        with open(self.path, 'wb') as save_zones:
            pickle.Pickler(save_zones).dump(self.zones)