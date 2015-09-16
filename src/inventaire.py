import os
import pygame
from pygame.locals import *
from constantes import *
import pickle


class Inventaire:
    def __init__(self, ecran, police):
        self.ecran = ecran
        self.police = police

        self.cur_categorie = POCHE_COMMUNS

        #Objets
        self.objets = [
            ["test", "autre test", "encore un test", "fin du test"],  # Poche communs
            ["seconde poche"],  # Poche capturateurs
            ["troisieme poche"],  # Poche médicaments
            ["quatrieme poche"],  # Poche Objets Rares
            ["cinquieme et derniere poche"]   # Poche CT/CS
        ]

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (50, 180, 70), (20, 20, FEN_large - 40, FEN_haut - 40))
        self.ecran.blit(self.police.render("Inventaire", 1, (10, 10, 10)), (FEN_large // 2, 30))
        for i in range(len(self.objets[self.cur_categorie])):
            self.ecran.blit(self.police.render(self.objets[self.cur_categorie][i], 1, (10, 10, 10)), (30, 40 + i * 20))

    def next(self):
        self.cur_categorie = self.cur_categorie + 1 if self.cur_categorie + 1 < len(self.objets) else 0

    def previous(self):
        self.cur_categorie = self.cur_categorie - 1 if self.cur_categorie - 1 >= 0 else len(self.objets) - 1

    def jeter(self, item: int):
        self.objets[self.cur_categorie].pop(item)

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "inventaire" + EXTENSION)):
            with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "rb") as read_inventaire:
                self.objets = pickle.Unpickler(read_inventaire).load()

    def save(self):
        with open(os.path.join("..", "saves", "inventaire" + EXTENSION), "wb") as wrb_inventaire:
            pickle.Pickler(wrb_inventaire).dump(self.objets)