import os
import pygame
from pygame.locals import *
from constantes import *


class PNJSpeaking:
    def __init__(self, texte: str, ecran: pygame.Surface, font: pygame.font.SysFont, color: tuple=(240, 240, 240)):
        self.texte = texte
        self.ecran = ecran
        self.font = font

        self.clignote = False
        self.mdt = 0

        self.color = color
        self.txt_renderer = self.font.render(self.texte, 1, (10, 10, 10))
        self.bulle = pygame.image.load(os.path.join("..", "assets", "gui", "bulle.png")).convert_alpha()

    def update(self, dt: int=1):
        self.render(dt)

    def render(self, dt: int=1):
        self.ecran.blit(self.bulle, (PNJ_TXT_XPOS, PNJ_TXT_YPOS))
        self.ecran.blit(self.txt_renderer, (PNJ_TXT_XPOS + PNJ_TXT_ALIGN_X, PNJ_TXT_YPOS + PNJ_TXT_ALIGN_Y))

        if self.clignote:
            self.ecran.blit(self.font.render("_", 1, (10, 10, 10)), (PNJ_TXT_X_CLIGNO, PNJ_TXT_Y_CLIGNO))

        self.mdt += dt
        self.mdt %= 2
        self.clignote = True if 0 <= self.mdt < 0.5 else False