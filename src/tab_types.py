import os
import pygame
from constantes import *
from pygame.locals import *
import pickle


class Storage:
    def __init__(self):
        self.tab = [[] for _ in range(MAX_T_NBR + 1)]
        self.tab[T_FEU][T_FEU] = 1
        self.tab[T_FEU][T_EAU] = 0.5
        self.tab[T_FEU][T_PLANTE] = 2
        self.tab[T_FEU][T_ELEC] = 1
        self.tab[T_FEU][T_AIR] = 1
        self.tab[T_FEU][T_NORMAL] = 1
        self.tab[T_FEU][T_TERRE] = 0.75
        self.tab[T_FEU][T_PLASMA] = 0.75
        self.tab[T_FEU][T_LUMIERE] = 1
        self.tab[T_FEU][T_TENEBRE] = 0

    def stronger(self, type_moi, type_adv):
        return True if self.tab[type_moi][type_adv] > 1 else False