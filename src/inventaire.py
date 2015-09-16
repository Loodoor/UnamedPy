import os
import pygame
from pygame.locals import *
from constantes import *
import pickle


class Inventaire:
    def __init__(self, ecran):
        self.ecran = ecran

        self.cur_categorie = POCHE_COMMUNS

        #Objets
        self.objets = [
            [],  # Poche communs
            [],  # Poche capturateurs
            [],  # Poche médicaments
            [],  # Poche Objets Rares
            []   # Poche CT/CS
        ]

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (50, 180, 70), (0, 0, 20, 50))

    def next(self):
        self.cur_categorie = self.cur_categorie + 1 if self.cur_categorie + 1 < len(self.objets) else len(self.objets) - 1

    def previous(self):
        self.cur_categorie = self.cur_categorie - 1 if self.cur_categorie - 1 >= 0 else 0

    def jeter(self, item: int):
        self.objets[self.cur_categorie].pop(item)

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "inventaire" + EXTENSION)):
            with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "rb") as read_inventaire:
                self.objets = pickle.Unpickler(read_inventaire).load()

    def save(self):
        with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "wb") as wrb_inventaire:
            pickle.Pickler(wrb_inventaire).dump(self.objets)