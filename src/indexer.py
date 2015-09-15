import pygame
import os
import pickle
from pygame.locals import *
from constantes import *


class Indexer:
    def __init__(self, ecran):
        self.ecran = ecran
        self.save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        self.page = 0
        self.indexer = {}

    def load(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "rb") as read_index:
                self.indexer = pickle.Unpickler(read_index).load()

    def save(self):
        with open(self.save_path, "wb") as save_index:
            pickle.Pickler(save_index).dump(self.indexer)

    def next(self):
        self.page = self.page + 1 if self.page <= 10 else 10

    def previous(self):
        self.page = self.page - 1 if self.page - 1 >= 0 else 0

    def vu_(self, nom):
        pass

    def capture_(self, nom):
        pass

    def update(self):
        self.render()

    def render(self):
        pass