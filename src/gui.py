import os
import pygame
from pygame.locals import *
from pnj_manager import PNJ
from constantes import *


class PNJSpeaking:
    def __init__(self, texte: str, ecran: pygame.Surface, font: pygame.font.SysFont, pnj: PNJ=None, color: tuple=(240, 240, 240)):
        self.texte = texte
        self.ecran = ecran
        self.pnj = pnj
        self.font = font

        self.color = color
        self.txt_renderer = self.font.render(self.texte, 1, (10, 10, 10))
        self.bulle = pygame.image.load(os.path.join("..", "assets", "gui", "bulle.png")).convert_alpha()

    def update(self):
        self.render()

    def render(self):
        self.ecran.blit(self.bulle, (PNJ_TXT_XPOS, PNJ_TXT_YPOS))
        self.ecran.blit(self.txt_renderer, (PNJ_TXT_XPOS + PNJ_TXT_ALIGN_X, PNJ_TXT_YPOS + PNJ_TXT_ALIGN_Y))