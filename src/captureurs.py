import os
import pygame
from glob import glob
from pygame.locals import *
from constantes import *


class Capturer:
    def __init__(self, ecran):
        self.ecran = ecran
        self.ratio = 0  # 100
        self.type_capt = ALL_TYPE