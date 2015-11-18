# coding=utf-8

import os
import pygame
from pygame.locals import *
from constantes import *
import time


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
        ev = pygame.event.get()
        self.render(dt)
        if ev != KEYUP:
            return True
        return False

    def render(self, dt: int=1):
        self.ecran.blit(self.bulle, (PNJ_TXT_XPOS, PNJ_TXT_YPOS))
        self.ecran.blit(self.txt_renderer, (PNJ_TXT_XPOS + PNJ_TXT_ALIGN_X, PNJ_TXT_YPOS + PNJ_TXT_ALIGN_Y))

        if self.clignote:
            self.ecran.blit(self.font.render("_", 1, (10, 10, 10)), (PNJ_TXT_X_CLIGNO, PNJ_TXT_Y_CLIGNO))

        self.mdt += dt
        self.mdt %= 2
        self.clignote = True if 0 <= self.mdt < 0.5 else False


class GUISauvegarde:
    def __init__(self, ecran: pygame.Surface, police: pygame.font.SysFont):
        self.ecran = ecran
        self.police = police
        self.texte = self.police.render("Sauvegarde en cours ... Merci de patienter :)", 1, (0, 0, 0))
        self.waiter = self.police.render("_", 1, (0, 0, 0))
        self.waiting = False
        self._time = 0
        self.time_between = 8
        self.start_time = -1
        self.save_time = 3  # secondes
        self.callback = None
        self.firstcall = None
        self.has_started_saving = False

    def reinit(self):
        self.waiting = False
        self._time = 0
        self.time_between = 10
        self.start_time = -1
        self.save_time = 3  # secondes
        self.callback = None
        self.firstcall = None
        self.has_started_saving = False

    def start_saving(self, firstcall: callable, callback: callable):
        firstcall()
        self.callback = callback
        self.start_time = time.time()
        self.has_started_saving = True

    def is_saving(self):
        return self.has_started_saving

    def is_saved_finished(self):
        return True if time.time() > self.start_time + self.save_time else False

    def update(self):
        self._time += 0.5
        if not self._time % self.time_between:
            self.waiting = not self.waiting
        if time.time() >= self.start_time + self.save_time:
            self.callback() if self.callback is not None else None
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (50, 180, 180), (SAVE_X, SAVE_Y, SAVE_SX, SAVE_SY))
        self.ecran.blit(self.texte,
                        (SAVE_X + (SAVE_SX - self.texte.get_width()) // 2,
                         SAVE_Y + 10))
        if self.waiting:
            self.ecran.blit(self.waiter, (4 + SAVE_X + (SAVE_SX + self.texte.get_width()) // 2,
                                           SAVE_Y + 10))