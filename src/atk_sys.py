import os
import pygame
from pygame.locals import *
from constantes import *


def calcul_degats(degats_basiques, specs_atk, specs_def):
    return degats_basiques + specs_atk[SPEC_ATK] / specs_def[SPEC_DEF]


def calcul_esquive(specs_atk, specs_def):
    return True if specs_atk[SPEC_VIT] >= 2 * specs_def[SPEC_VIT] else False