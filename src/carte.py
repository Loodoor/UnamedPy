# coding=utf-8

import os
import pickle
from glob import glob
import pygame
from pygame.locals import *
from constantes import *
from trigger_manager import TriggersManager


class none:
    pass


class CarteManager:
    def __init__(self, ecran: pygame.Surface, renderer_manager):
        self.ecran = ecran
        self.carte = []
        self.map_path = os.path.join("..", "saves", "map" + EXTENSION)
        self.fov = [0, FIRST_BASIC_FOV, 0, FIRST_BASIC_FOV2]
        self.offsets = [0, 0]
        self.images = {}
        self.lassets = []
        self.triggers_mgr = TriggersManager()
        self.rd_mgr = renderer_manager

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

    def get_fov_carte(self):
        return [ligne[int(self.fov[0]):int(self.fov[1])] for ligne in self.carte[int(self.fov[2]):int(self.fov[3])]]

    def get_zid_at(self, at: tuple=(-1, -1)):
        return self

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

    def has_trigger(self, x: int=0, y: int=0):
        return True if len(self.carte[y + self.fov[2]][x + self.fov[0]]) == 6 else False

    def get_trigger(self, x: int=0, y: int=0):
        if self.has_trigger(x, y):
            self.triggers_mgr.call_trigger_at_pos(x, y)

    def load(self):
        if os.path.exists(self.map_path):
            with open(self.map_path, "rb") as map_rdb:
                self.carte = pickle.Unpickler(map_rdb).load()
        else:
            print("An error occurred. The map seems to doesn't exist")
        self.triggers_mgr.load()

        for i in glob("..//assets//tiles//*.png"):
            # chargement automatique des tiles, leur nom déterminent si elles sont bloquantes ou non
            self.images[i[18:-4]] = pygame.image.load(i).convert_alpha()
            self.lassets.append(i[18:-4])

    def save(self):
        with open(self.map_path, "wb") as map_wb:
            pickle.Pickler(map_wb).dump(self.carte)
        self.triggers_mgr.save()

    def update(self):
        self.render()

    def render(self):
        tmp_map = [ligne[int(self.fov[0]):int(self.fov[1])] for ligne in self.carte[int(self.fov[2]):int(self.fov[3])]]
        for y in range(len(tmp_map)):
            for x in range(len(tmp_map[y])):
                objet = self.carte[y][x]
                xpos, ypos = x * TILE_SIZE + self.offsets[0], y * TILE_SIZE + self.offsets[1]
                if not isinstance(objet, list):
                    self.ecran.blit(self.images[objet], (xpos, ypos))
                else:
                    if len(objet) <= 5:
                        for tile in objet[::-1]:
                            self.ecran.blit(self.images[tile], (xpos, ypos))
                    else:
                        for tile in objet[-2::-1]:
                            self.ecran.blit(self.images[tile], (xpos, ypos))


class CarteRenderer:
    def __init__(self, ecran: pygame.Surface, carte_mgr: CarteManager):
        self.ecran = ecran
        self.carte_mgr = carte_mgr
        self.carte_img = os.path.join("..", "assets", "gui", "carte.png")

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (20, 180, 20), (MAP_RDR_POSX, MAP_RDR_POSY, MAP_RDR_SX, MAP_RDR_SY))
        self.ecran.blit(self.carte_mgr, (MAP_RDR_CARTEX, MAP_RDR_CARTEX))