from os import path
from constantes import *
import pickle


class Zone:
    def __init__(self):
        pass


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

    def load(self):
        if path.exists(self.path):
            with open(self.path, 'rb') as zones_rb:
                self.zones = pickle.Unpickler(zones_rb).load()

    def save(self):
        with open(self.path, 'wb') as save_zones:
            pickle.Pickler(save_zones).dump(self.zones)