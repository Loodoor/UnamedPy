import pygame
from pygame.locals import *
import os
from carte import CarteManager
from constantes import *


class PNJ:
    def __init__(self, ecran: pygame.Surface, carte_mgr: CarteManager, pos: list,
                 type_mvt: list, dir: int=1, sprite: str='test.png') -> None:
        self.ecran = ecran
        self.carte_mgr = carte_mgr
        self.pos = pos
        self.type_mvt = type_mvt
        self.cur_scheme = 0
        self.dir = dir
        self.orientation = BAS
        self.sprite = pygame.image.load(os.path.join("..", "assets", "pnj", sprite)).convert_alpha()

    def update(self):
        self.move()
        self.render()

    def move_scheme(self):
        self.cur_scheme += self.dir
        if self.cur_scheme + self.dir < 0:
            self.cur_scheme = len(self.type_mvt) - 1
        if self.cur_scheme + self.dir >= len(self.type_mvt):
            self.cur_scheme = 0

    def move(self):
        self.move_scheme()
        tmp = self.type_mvt[self.cur_scheme]
        actual_x, actual_y = tmp
        actual_x += self.pos[0]
        actual_y += self.pos[1]
        if tmp[0] == 1:
            self.orientation = DROITE
        if tmp[0] == -1:
            self.orientation = GAUCHE
        if tmp[1] == 1:
            self.orientation = HAUT
        if tmp[1] == -1:
            self.orientation = BAS

    def render(self):
        pass