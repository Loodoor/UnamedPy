import os
import pickle
import pygame
from pygame.locals import *


class Carte:
    def __init__(self, ecran):
        self.ecran = ecran
        self.carte = []
        self.map_path = os.path.join("..", "saves", "map.umd")

        self.load_map()

    def load_map(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "rb") as map_rdb:
                self.carte = pickle.Unpickler(map_rdb).load()
        else:
            #générer la carte ?
            pass

    def save(self):
        with open(self.map_path, "wb") as map_wb:
            pickle.Pickler(map_wb).dump(self.carte)

    def update(self):
        self.render()

    def render(self):
        pass