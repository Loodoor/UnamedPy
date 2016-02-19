# coding=utf-8

from constantes import *
import random
from creatures_mgr import Creature


class Capturer:
    def __init__(self, ecran: pygame.Surface):
        self.ecran = ecran
        self.ratio = 0  # 100
        self.type_capt = None  # NotImpletedError
        self.creature = None

    def use(self, creature: Creature):
        if random.randint(0, MAX_RATIO_CAP) >= self.ratio:
            self.creature = creature
            return True
        return False

    def who_is_in(self):
        return self.creature