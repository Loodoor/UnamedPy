import os
import pygame
from pygame.locals import *
import pickle
from constantes import *
from glob import glob


class Personnage:
    def __init__(self, ecran, carte_mgr, pos=(0, 0)):
        self.ecran = ecran
        self.direction = BAS
        self.anim_cursor = PAUSE
        self.max_anim_cursor = 2
        self.lhaut = [pygame.image.load(_).convert_alpha() for _ in glob(os.path.join("..", "assets", "personnage", "haut*.png"))]
        self.lbas = [pygame.image.load(_).convert_alpha() for _ in glob(os.path.join("..", "assets", "personnage", "bas*.png"))]
        self.lgauche = [pygame.image.load(_).convert_alpha() for _ in glob(os.path.join("..", "assets", "personnage", "gauche*.png"))]
        self.ldroite = [pygame.image.load(_).convert_alpha() for _ in glob(os.path.join("..", "assets", "personnage", "droite*.png"))]
        self.sprites = {
            HAUT: self.lhaut,
            BAS: self.lbas,
            GAUCHE: self.lgauche,
            DROITE: self.ldroite
        }
        self.perso = self.sprites[self.direction][self.anim_cursor]

        self.is_moving = False
        self.pos = list(pos)
        self.carte_mgr = carte_mgr

    def move(self, direction=HAUT):
        self.direction = direction
        self.perso = self.sprites[self.direction][ANIM1]
        self.is_moving = True

        #Détection des collisions

    def update(self):
        if not self.is_moving:
            self.perso = self.sprites[self.direction][PAUSE]
        else:
            self.anim_cursor = (self.anim_cursor + 1) % self.max_anim_cursor
        self.render()

    def render(self):
        self.ecran.blit(self.perso, self.pos)

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "perso" + EXTENSION)):
            with open(os.path.join("..", "saves", "perso" + EXTENSION), "rb") as read_perso:
                self.pos = pickle.Unpickler(read_perso).load()

    def save(self):
        with open(os.path.join("..", "saves", "perso" + EXTENSION), "wb") as save_perso:
            pickle.Pickler(save_perso).dump(self.pos)