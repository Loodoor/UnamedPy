# coding=utf-8

from constantes import *
from textentry import TextBox
import time
from glob import glob


class GUIBulle:
    def __init__(self, ecran, pos: tuple, texte: str or list, font):
        self.ecran = ecran
        self.pos = pos
        self.texte = texte
        self.font = font
        self.image = rendering_engine.load_image(os.path.join("..", "assets", "gui", "bulle.png"))
        self.iw, self.ih = self.image.get_size()
        self.txt_renderer = self.font.render(" ", POL_ANTIALISING, (10, 10, 10))
        self.create_text_renderers()

    def set_text(self, new: str or list):
        self.texte = new
        self.create_text_renderers()

    def create_text_renderers(self):
        if not isinstance(self.texte, list):
            self.txt_renderer = self.font.render(self.texte, POL_ANTIALISING, (10, 10, 10))
        else:
            self.txt_renderer = [self.font.render(t, POL_ANTIALISING, (10, 10, 10)) for t in self.texte]

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
    def __init__(self, ecran, pos: tuple, texte: str or list, font, screenshotkey=K_F5):
        super().__init__(ecran, pos, texte, font)
        self.done = False
        self.screenkey = screenshotkey

    def is_done(self):
        return self.done

    def set_text(self, new: str or list):
        self.texte = new
        self.create_text_renderers()
        self.done = False

    def update(self, dt: int=1):
        while not self.done:
            ev = rendering_engine.poll_event()
            if ev.type == KEYDOWN:
                if ev.key != self.screenkey:
                    self.done = True

            self.render()
            rendering_engine.flip()


class GUIBulle2Choices(GUIBulleWaiting):
    def __init__(self, ecran, pos: tuple, texte: str, font,
                 screenshotkey=K_F5):
        super().__init__(ecran, pos, texte, font, screenshotkey)
        self.ok = False

    def update(self, dt: int=1):
        while not self.done:
            ev = rendering_engine.poll_event()
            if ev.type == KEYDOWN:
                if ev.key == K_RETURN:
                    self.ok = True
                if ev.key != self.screenkey:
                    self.done = True

            self.render()
            rendering_engine.flip()
        return self.ok


class GUIBulleAsking(GUIBulleWaiting):
    def __init__(self, ecran, pos: tuple, texte: str, font,
                 screenshotkey=K_F5):
        super().__init__(ecran, pos, texte, font, screenshotkey)
        self.create_text_renderers()
        self.text_box = TextBox(self.ecran, x=self.pos[0] + self.txt_renderer.get_width() // 2 + self.iw // 2,
                                y=self.pos[1] + (self.ih - self.txt_renderer.get_height() - 4) // 2,
                                bgcolor=(120, 120, 120),
                                sy=self.txt_renderer.get_height() + 4,
                                font=self.font)

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

        if self.text_box.is_running():
            self.text_box.update()
        else:
            self.done = True

    def get_text(self):
        return self.text_box.get_text()

    def update(self, dt: int=1):
        while not self.done:
            ev = rendering_engine.poll_event()
            if ev.type == KEYDOWN:
                if ev.key != self.screenkey:
                    self.text_box.event(ev)

            self.render()
            rendering_engine.flip()


class GUISauvegarde:
    def __init__(self, ecran, police):
        self.ecran = ecran
        self.police = police
        self.texte = self.police.render("Sauvegarde en cours ... Merci de patienter :)", POL_ANTIALISING, (0, 0, 0))
        self.waiter = self.police.render("_", POL_ANTIALISING, (0, 0, 0))
        self.waiting = False
        self._time = 0
        self.time_between = 8
        self.start_time = -1
        self.save_time = 3  # secondes
        self.callback = None
        self.firstcall = None
        self.has_started_saving = False
        self.ldroite = [rendering_engine.load_image(_) for _ in
                        glob(os.path.join("..", "assets", "personnages", "first", "droite*.png"))]
        self.cur_anim = 0
        self.fond = rendering_engine.load_image(os.path.join("..", "assets", "gui", "fd_sauvegarde.png"))

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
        self.ecran.blit(self.fond, (SAVE_X, SAVE_Y))
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