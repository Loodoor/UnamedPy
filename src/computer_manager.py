import pygame
import os
from pygame.locals import *
from creatures_mgr import Creature
import pickle
from constantes import *


class ComputerManager:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont, max_size=PC_MAX_CREA):
        self.ecran = ecran
        self.police = police
        self.storage = []
        self.path = os.path.join("..", "saves", "pc" + EXTENSION)

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as pc_rb:
                self.storage = pickle.Unpickler(pc_rb).load()

    def save(self):
        with open(self.path, "wb") as pc_wb:
            pickle.Pickler(pc_wb).dump(self.storage)

    def update(self):
        self.render()

    def render(self):
        pass

    def add_creature(self, new: Creature):
        self.storage.append(new)

    def get_creature(self, index: int):
        return self.storage[index] if 0 <= index < len(self.storage) else PC_GET__ERROR

    def pop_creature(self, index: int):
        return self.storage.pop(index) if 0 <= index < len(self.storage) else PC_POP__ERROR