import os
import pickle
from glob import glob
import pygame
from pygame.locals import *
from constantes import *


class CarteManager:
    def __init__(self, ecran: pygame.Surface):
        self.ecran = ecran
        self.carte = []
        self.map_path = os.path.join("..", "saves", "map" + EXTENSION)
        self.fov = [0, FIRST_BASIC_FOV, 0, FIRST_BASIC_FOV2]
        self.offsets = [0, 0]
        self.images = {}
        self.lassets = []

    def get_of1(self):
        return self.offsets[0]

    def get_of2(self):
        return self.offsets[1]

    def get_ofs(self):
        return self.offsets

    def get_fov(self):
        return self.fov

    def get_carte(self):
        return self.carte

    def move_of1(self, dir: int=1):
        self.offsets[0] += dir
        if not self.offsets[0] % TILE_SIZE:
            if self.fov[0] - dir >= 0:
                self.offsets[0] %= TILE_SIZE
                self.fov[0] -= dir

    def move_of2(self, dir: int=1):
        self.offsets[1] += dir
        if not self.offsets[1] % TILE_SIZE:
            if self.fov[2] - dir >= 0:
                self.offsets[1] %= TILE_SIZE
                self.fov[2] -= dir

    def load(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "rb") as map_rdb:
                self.carte = pickle.Unpickler(map_rdb).load()
        else:
            print("An error occurred. The map seems to doesn't exist")

        for i in glob("..//assets//tiles//*.png"):
            self.images[i[18:-4]] = pygame.image.load(i).convert_alpha()
            self.lassets.append(i[18:-4])

    def save(self):
        with open(self.map_path, "wb") as map_wb:
            pickle.Pickler(map_wb).dump(self.carte)

    def update(self):
        self.render()

    def render(self):
        tmp_map = [ligne[self.fov[0]:self.fov[1]] for ligne in self.carte[self.fov[2]:self.fov[3]]]
        for y in range(len(tmp_map)):
            for x in range(len(tmp_map[y])):
                objet = self.carte[y][x]
                xpos, ypos = x * TILE_SIZE + self.offsets[0], y * TILE_SIZE + self.offsets[1]
                if not isinstance(objet, list):
                    self.ecran.blit(self.images[objet], (xpos, ypos))
                else:
                    for z in range(len(objet)):
                        tile = objet[z]
                        self.ecran.blit(self.images[tile], (xpos, ypos))