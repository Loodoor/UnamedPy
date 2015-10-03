import pygame
import os
import pickle
from pygame.locals import *
from constantes import *


class Indexer:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont):
        self.ecran = ecran
        self.police = police
        self.save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        self.page = 0
        self.max_page = 10
        self.par_page = 10
        self.indexer = {}

    def load(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "rb") as read_index:
                self.indexer = pickle.Unpickler(read_index).load()

    def save(self):
        with open(self.save_path, "wb") as save_index:
            pickle.Pickler(save_index).dump(self.indexer)

    def next(self):
        self.page = self.page + 1 if self.page <= self.max_page else self.max_page

    def previous(self):
        self.page = self.page - 1 if self.page - 1 >= 0 else 0

    def vu_(self, nom: str):
        self.indexer[nom][VU] = True

    def capture_(self, nom: str):
        self.indexer[nom][CAPTURE] = True

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (180, 20, 180), (POK_POSX, POK_POSY, POK_X_SIZE, POK_Y_SIZE))
        self.ecran.blit(self.police.render("Indexeur", 1, (255, 255, 255)), (POK_X_TITRE, POK_Y_TITRE))