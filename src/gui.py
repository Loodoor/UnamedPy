# coding=utf-8

from constantes import *
from textentry import TextBox
import time
from glob import glob
import textwrap as tw
import debug


class GUIBulle:
    def __init__(self, ecran, pos: tuple, texte: str, font: ree.font, show_bulle: bool=True):
        self.ecran = ecran
        self.pos = pos
        self.texte = texte
        self.font = font
        self.image = ree.load_image(os.path.join("..", "assets", "gui", "bulle.png"))
        self.iw, self.ih = self.image.get_size()
        self.txt_renderer = [self.font.render(" ", POL_ANTIALISING, (10, 10, 10))]
        self.show_bulle = show_bulle
        self.create_text_renderers()

    def set_text(self, new: str or list):
        self.texte = new
        self.create_text_renderers()

    def create_text_renderers(self):
        if not isinstance(self.texte, list):
            char_w = self.font.render("M", POL_ANTIALISING, (10, 10, 10)).get_width()
            available_len = (self.image.get_width() - 20) / char_w
            self.txt_renderer = [self.font.render(line, POL_ANTIALISING, (10, 10, 10)) for line in tw.wrap(self.texte, int(available_len))]
        else:
            self.txt_renderer = [self.font.render(t, POL_ANTIALISING, (10, 10, 10)) for t in self.texte]

    def reinit_color(self):
        self.image = ree.load_image(os.path.join("..", "assets", "gui", "bulle.png"))

    def set_color(self, color: str):
        try:
            self.image = ree.load_image(os.path.join("..", "assets", "gui", "bulle_{}.png".format(color)))
        except OSError:
            debug.println("[GUI] La couleur demandée n'est pas trouvable pour la gui bulle ('{}')".format(color))

    def update(self, dt: int=1):
        self.render()

    def update_one_frame(self, ev: ree.Event):
        self.update()

    def render(self):
        if self.show_bulle:
            self.ecran.blit(self.image, self.pos)
        line_height = self.txt_renderer[0].get_height()
        for i, trender in enumerate(self.txt_renderer):
            self.ecran.blit(
                trender,
                (
                    self.pos[0] + self.iw // 2 - trender.get_width() // 2,
                    self.pos[1] + self.ih // 2 - (line_height * len(self.txt_renderer)) // 2 + i * GUI_Y_ESP
                )
            )


class GUIBulleWaiting(GUIBulle):
    def __init__(self, ecran, pos: tuple, texte: str or list, font: ree.font, show_bulle: bool=True,
                 screenshotkey=K_F5):
        super().__init__(ecran, pos, texte, font, show_bulle)
        self.done = False
        self.screenkey = screenshotkey

    def is_done(self):
        return self.done

    def set_text(self, new: list):
        self.texte = new
        self.create_text_renderers()
        self.done = False

    def update_one_frame(self, ev: ree.Event):
        if ev != (KEYDOWN, self.screenkey) and ev == KEYDOWN:
            self.done = True
        self.render()

    def update(self, dt: int=1):
        while not self.done:
            ev = ree.poll_event()
            if ev != (KEYDOWN, self.screenkey) and ev == KEYDOWN:
                self.done = True

            self.render()
            ree.flip()


class GUIBulle2Choices(GUIBulleWaiting):
    def __init__(self, ecran, pos: tuple, texte: str or list, font: ree.font, show_bulle: bool=True,
                 screenshotkey=K_F5):
        super().__init__(ecran, pos, texte, font, screenshotkey, show_bulle)
        self.ok = False

    def is_ok(self):
        return self.ok

    def update_one_frame(self, ev: ree.Event):
        if ev == (KEYUP, K_RETURN):
            self.ok = True
        if ev != (KEYUP, self.screenkey):
            self.done = True
        self.render()

    def update(self, dt: int=1):
        while not self.done:
            ev = ree.poll_event()
            if ev == (KEYUP, K_RETURN):
                self.ok = True
            if ev != (KEYUP, self.screenkey):
                self.done = True

            self.render()
            ree.flip()
        return self.ok


class GUIBulleAsking(GUIBulleWaiting):
    def __init__(self, ecran, pos: tuple, texte: str or list, font: ree.font, show_bulle: bool=True,
                 screenshotkey=K_F5):
        super().__init__(ecran, pos, texte, font, screenshotkey, show_bulle)
        self.create_text_renderers()
        self.text_box = TextBox(self.ecran,
                                x=self.pos[0] + self.iw // 2 - 120 // 2,
                                y=self.pos[1] + (self.ih + sum(i.get_height() for i in self.txt_renderer)) // 2 + 6,
                                bgcolor=(120, 120, 120),
                                sy=self.txt_renderer[0].get_height() + 4,
                                font=self.font)

    def render(self):
        if self.show_bulle:
            self.ecran.blit(self.image, self.pos)
        for i, trender in enumerate(self.txt_renderer):
            self.ecran.blit(
                trender,
                (
                    self.pos[0] + self.iw // 2 - trender.get_width() // 2,
                    self.pos[1] + self.ih // 2 - (trender.get_height() * len(self.txt_renderer)) // 2 + i * GUI_Y_ESP
                )
            )

        if self.text_box.is_running():
            self.text_box.update()
        else:
            self.done = True

    def get_text(self):
        return self.text_box.get_text()

    def update_one_frame(self, ev: ree.Event):
        if ev != (KEYDOWN, self.screenkey) and ev == KEYDOWN:
            self.text_box.event(ev)
        self.render()

    def update(self, dt: int=1):
        while not self.done:
            ev = ree.poll_event()
            if ev != (KEYDOWN, self.screenkey) and ev == KEYDOWN:
                self.text_box.event(ev)

            self.render()
            ree.flip()


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
        self.ldroite = [ree.load_image(_) for _ in
                        glob(os.path.join("..", "assets", "pnj", "dad", "droite*.png"))]
        self.cur_anim = 0
        self.fond = ree.load_image(os.path.join("..", "assets", "gui", "fd_sauvegarde.png"))

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
            self.cur_anim += 1
            self.cur_anim %= len(self.ldroite)
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