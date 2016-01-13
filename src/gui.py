# coding=utf-8

import pygame
from pygame.locals import *
from constantes import *
from textentry import TextBox
import time
from glob import glob
from utils import uscreenschot


class GUIBulle:
    def __init__(self, ecran: pygame.Surface, pos: tuple, texte: str or list, font: pygame.font.SysFont):
        self.ecran = ecran
        self.pos = pos
        self.texte = texte
        self.font = font
        self.image = pygame.image.load(os.path.join("..", "assets", "gui", "bulle.png")).convert_alpha()
        self.iw, self.ih = self.image.get_size()
        self.txt_renderer = self.font.render("", 1, (10, 10, 10))
        self.create_text_renderers()

    def set_text(self, new: str or list):
        self.texte = new
        self.create_text_renderers()

    def create_text_renderers(self):
        if not isinstance(self.texte, list):
            self.txt_renderer = self.font.render(self.texte, 1, (10, 10, 10))
        else:
            self.txt_renderer = [self.font.render(t, 1, (10, 10, 10)) for t in self.texte]

    def update(self, dt: int=1):
        self.render()

    def render(self):
        self.ecran.blit(self.image, self.pos)
        if not isinstance(self.txt_renderer, list):
            self.ecran.blit(self.txt_renderer, (self.pos[0] + self.iw // 2 - self.txt_renderer.get_width() // 2,
                                                self.pos[1] + self.ih // 2 - self.txt_renderer.get_height() // 2))
        else:
            i = 0
            for trender in self.txt_renderer:
                self.ecran.blit(trender, (self.pos[0] + self.iw // 2 - trender.get_width() // 2,
                                          self.pos[1] + self.ih // 2 -
                                                (trender.get_height() * len(self.txt_renderer)) + i * GUI_Y_ESP))
                i += 1


class GUIBulleWaiting(GUIBulle):
    def __init__(self, ecran: pygame.Surface, pos: tuple, texte: str or list, font: pygame.font.SysFont, screenshotkey=K_F5):
        super().__init__(ecran, pos, texte, font)
        self.done = False
        self.screenkey = screenshotkey

    def is_done(self):
        return self.done

    def set_text(self, new: str or list):
        super(self).set_text(new)
        self.done = False

    def update(self, dt: int=1):
        while not self.done:
            ev = pygame.event.poll()
            if ev.type == KEYDOWN:
                if ev.key != self.screenkey:
                    self.done = True
                else:
                    uscreenschot(self.ecran)

            self.render()
            pygame.display.flip()


class GUIBulleAsking(GUIBulleWaiting):
    def __init__(self, ecran: pygame.Surface, pos: tuple, texte: str, font: pygame.font.SysFont,
                 screenshotkey=K_F5):
        super().__init__(ecran, pos, texte, font, screenshotkey)
        self.create_text_renderers()
        self.text_box = TextBox(self.ecran, x=self.pos[0] + (self.iw - 120 + self.txt_renderer.get_width()) // 2,
                                y=self.pos[1] + (self.ih - 35) // 2, bgcolor=(120, 120, 120))

    def render(self):
        super(self).render()
        if self.text_box.is_running():
            self.text_box.update()
        else:
            self.done = True

    def get_text(self):
        return self.text_box.get_text()

    def update(self, dt: int=1):
        while not self.done:
            ev = pygame.event.poll()
            if ev.type == KEYDOWN:
                if ev.key != self.screenkey:
                    self.done = True
                else:
                    uscreenschot(self.ecran)

            self.render()
            pygame.display.flip()


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
        self.ldroite = [pygame.image.load(_).convert_alpha() for _ in
                        glob(os.path.join("..", "assets", "personnage", "droite*.png"))]
        self.cur_anim = 0

    def reinit(self):
        self.waiting = False
        self._time = 0
        self.start_time = -1
        self.save_time = 3  # secondes
        self.callback = None
        self.firstcall = None
        self.has_started_saving = False
        self.cur_anim = 0

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
        if not self._time % (self.time_between * 2):
            self.cur_anim = self.cur_anim + 1 if self.cur_anim + 1 < len(self.ldroite) else 0
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
        self.ecran.blit(self.ldroite[self.cur_anim],
                        (0 + (SAVE_SX + self.ldroite[0].get_width()) // 2,
                        SAVE_Y + SAVE_X_PERSO_DECALAGE)
        )