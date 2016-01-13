# coding=utf-8

from constantes import *
from pickle import Pickler, Unpickler
from gui import GUIBulleWaiting, GUIBulleAsking
import pygame


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

    def _begin(self):
        g = GUIBulleWaiting(self.ecran, (0, 0), "", self.font)
        for texte in self.beginning_text:
            if texte[0] == INPUT_CHAR:
                ask_smth = True
                ask_for = texte[texte[1:].index(INPUT_CHAR) + 1:]
                g.set_text(texte[1:texte[1:].index(INPUT_CHAR) + 2])
            else:
                ask_smth = False
                g.set_text(texte)
            g.update()

            if ask_smth:
                if ask_for == "pseudo":
                    t = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Pseudo : ", self.font)
                    t.update()
                    self.user_pseudo = t.get_text()
        del g

    def next(self):
        if self.loaded:
            if not self.progress:
                self._begin()
            self.progress += 1
        else:
            print("Merci de charger l'AdventureManager avant d'utiliser cette méthode")

    def set_pseudo(self, new: str):
        self.user_pseudo = new

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as reader:
                tmp = Unpickler(reader).load()
                self.user_pseudo = tmp['pseudo']
                self.progress = tmp['progress']
        try:
            with open(os.path.join("..", "assets", "aventure", "beginning_text.txt")) as begin_read:
                self.beginning_text = begin_read.readlines()
        except OSError:
            print("Un fichier de sauvegarde n'existe pas. Impossible de continuer.")
            sys.exit(0)
        self.loaded = True

    def save(self):
        with open(self.path, "wb") as writer:
            Pickler(writer).dump({
                "pseudo": self.user_pseudo,
                "progress": self.progress
            })