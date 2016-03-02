# coding=utf-8

from constantes import *
from pickle import Pickler, Unpickler
from gui import GUIBulleWaiting, GUIBulleAsking
import pygame
import debug


# Attention, y a du hardcode dans l'air ^^'
class Adventure:
    def __init__(self, ecran: pygame.Surface, font: pygame.font.SysFont):
        self.user_pseudo = ""
        self.progress = 0
        self.ecran = ecran
        self.font = font
        self.path = os.path.join("..", "saves", "adventure" + EXTENSION)
        self.beginning_text = []
        self.loaded = False
        self.values = {}
        self._first_creature_image = pygame.image.load(os.path.join("..", "assets", "creatures", "feu-01.png")).convert_alpha()
        self._image_prof = pygame.image.load(os.path.join("..", "assets", "aventure", "professeur.png")).convert_alpha()

    def get_progress(self):
        return self.progress

    def has_already_played(self):
        if not self.progress:
            return False
        return True

    def _begin(self):
        ask_for = ""
        name_of_image = ""
        g = GUIBulleWaiting(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "", self.font)
        i = 0
        for texte in self.beginning_text:
            pygame.draw.rect(self.ecran, (50, 180, 50), (0, 0) + self.ecran.get_size())

            if texte[0] == INPUT_CHAR:
                ask_smth = True
                ask_for = texte[texte[1:].index(INPUT_CHAR) + 2:-1]
                g.set_text(texte[1:texte[1:].index(INPUT_CHAR) + 1])
            elif texte[0] == IMAGE_SHOW_CHAR:
                name_of_image = texte.replace(":", "")
                continue
            else:
                ask_smth = False
                if '{' not in texte and '}' not in texte:
                    g.set_text(texte[:-1])
                else:
                    g.set_text(texte[:-1].format(pseudo=self.user_pseudo))

            if "creature image" in name_of_image:
                self.ecran.blit(self._first_creature_image, (
                    (self.ecran.get_width() - self._first_creature_image.get_width()) // 2,
                    (self.ecran.get_height() - self._first_creature_image.get_height()) // 2
                ))
            if "image prof" in name_of_image:
                self.ecran.blit(self._image_prof, (
                    (self.ecran.get_width() - self._image_prof.get_width()) // 2,
                    (self.ecran.get_height() - self._image_prof.get_height() - BULLE_SY) // 2
                ))

            g.update()

            if ask_smth:
                ask_smth = False
                if ask_for == "pseudo":
                    t = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Pseudo : ", self.font)
                    t.update()
                    self.user_pseudo = t.get_text()
                    with open(os.path.join("..", "saves", "pseudo" + EXTENSION), "wb") as pseudo_w:
                        Pickler(pseudo_w).dump(self.user_pseudo)
                elif ask_for == "creature":
                    t = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Nom : ", self.font)
                    t.update()
                    self.values["first creature name"] = t.get_text()
            i += 1

            pygame.display.flip()
        del g

    def next(self):
        if self.loaded:
            if not self.progress:
                self._begin()
            self.progress += 1
        else:
            debug.println("Merci de charger l'AdventureManager avant d'utiliser cette méthode")

    def set_pseudo(self, new: str):
        self.user_pseudo = new

    def get_pseudo(self):
        return self.user_pseudo

    def get_values(self):
        return self.values

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as reader:
                tmp = Unpickler(reader).load()
                self.user_pseudo = tmp['pseudo']
                self.progress = tmp['progress']
        try:
            with open(os.path.join("..", "assets", "aventure", "beginning_text.txt"), "r", encoding="utf-8") as begin_read:
                self.beginning_text = begin_read.readlines()
        except OSError:
            debug.println("Un fichier de sauvegarde n'existe pas. Impossible de continuer.")
            sys.exit(0)
        self.loaded = True

    def save(self):
        with open(self.path, "wb") as writer:
            Pickler(writer).dump({
                "pseudo": self.user_pseudo,
                "progress": self.progress
            })