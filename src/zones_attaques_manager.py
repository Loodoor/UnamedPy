from os import path
from constantes import *
import pickle
from creatures_mgr import Creature
from random import choice, randrange
from indexer import Indexer


class Zone:
    def __init__(self, id: str, types: list, creatures_id: list, level_range: tuple, indexer: Indexer):
        self.id = id
        self.types = types
        self.creatures_id = creatures_id
        self.level_range = level_range
        self.indexer = indexer

    def get_id(self):
        return self.id

    def get_new_adversaire(self):
        return self


class ZonesManager:
    def __init__(self):
        self.path = path.join("..", "saves", "zones" + EXTENSION)
        self.zones = []

    @staticmethod
    def add_new_zone_to_path(zone: Zone):
        path_ = path.join("..", "saves", "zones" + EXTENSION)
        if path.exists(path_):
            with open(path_, 'rb') as read_zones:
                pickle.Pickler(open(path_, 'wb')).dump(pickle.Unpickler(read_zones).load().append(zone))
        else:
            with open(path_, 'wb') as add_new:
                pickle.Pickler(add_new).dump([zone])

    def get_new_adversary(self, with_zoneid: int):
        for zone in self.zones:
            if zone.get_id() == with_zoneid:
                return zone.get_new_adversaire()
        return ZONE_ADV_ERROR

    def load(self):
        if path.exists(self.path):
            with open(self.path, 'rb') as zones_rb:
                self.zones = pickle.Unpickler(zones_rb).load()

    def save(self):
        with open(self.path, 'wb') as save_zones:
            pickle.Pickler(save_zones).dump(self.zones)