import os
import pygame
from pygame.locals import *
from constantes import *
import random


class Capturer:
    def __init__(self, ecran):
        self.ecran = ecran
        self.ratio = 0  # 100
        self.type_capt = None  # NotImpletedError
        self.creature = {}

    def use(self, sur, pseudo, type, niv, pv, specs):
        if random.randint(0, MAX_RATIO_CAP) >= self.ratio:
            self.creature[CAP_PSEUDO] = pseudo
            self.creature[CAP_NOM] = sur
            self.creature[CAP_TYPE] = type
            self.creature[CAP_NIV] = niv
            self.creature[CAP_PV] = pv
            self.creature[CAP_SPECS] = specs
            return True
        return False

    def who_is_in(self):
        return self.creature