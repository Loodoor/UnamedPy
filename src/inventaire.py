import os
import pygame
from pygame.locals import *
from constantes import *
import pickle
from hud import HUDInventaire


class Inventaire:
    def __init__(self, ecran):
        self.ecran = ecran
        self.hud = HUDInventaire(self.ecran)

        self.cur_categorie = POCHE_COMMUNS

        #Objets
        self.objets = {}

    def update(self):
        self.render()

    def render(self):
        self.hud.render()
        pass

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "inventaire" + EXTENSION)):
            with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "rb") as read_inventaire:
                self.objets = pickle.Unpickler(read_inventaire).load()

    def save(self):
        with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "wb") as wrb_inventaire:
            pickle.Pickler(wrb_inventaire).dump(self.objets)