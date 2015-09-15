import os
import pygame
from constantes import *
from pygame.locals import *
import pickle


class Storage:
    def __init__(self):
        self.tab = [[] for _ in range(MAX_T_NBR + 1)]

    def stronger(self, type):
        return True