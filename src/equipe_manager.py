import pygame
import os
from pygame.locals import *
import creatures_mgr
import pickle
from constantes import *


class EquipeManager:
    def __init__(self, ecran: pygame.Surface, size: int=6):
        self.size = size
        self.ecran = ecran
        self.creatures = []
        self.path = os.path.join("..", "saves", "equipe" + EXTENSION)

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as equipe_rb:
                self.creatures = pickle.Unpickler(equipe_rb).load()

    def save(self):
        with open(self.path, "wb") as equipe_wb:
            pickle.Pickler(equipe_wb).dump(self.creatures)

    def add_creature(self, new: creatures_mgr.Creature):
        if len(self.creatures) < self.size:
            self.creatures.append(new)

    def move_creature(self, first: int, second: int):
        ftmp = self.creatures[first]
        stmp = self.creatures[second]
        self.creatures[first] = stmp
        self.creatures[second] = ftmp

    def remove_creature(self, index: int):
        return self.creatures.pop(index)

    def get_creature(self, index: int):
        return self.creatures[index]

    def get_all(self):
        return self.creatures