import os
import pygame
import pickle
from constantes import *
from glob import glob


class Personnage:
    def __init__(self, ecran, carte_mgr, pos=(0, 0)):
        self.ecran = ecran
        self.direction = BAS
        self.anim_cursor = PAUSE
        self.max_anim_cursor = 2
        self.speed = BASIC_SPEED
        self.cur_div = DIV_DT_BASIC
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

    def move(self, direction=HAUT, dt=1):
        self.direction = direction
        self.perso = self.sprites[self.direction][self.anim_cursor + 1]
        self.is_moving = True

        vecteur = (0, 0)

        if direction == HAUT:
            vecteur = (0, -1)
        if direction == BAS:
            vecteur = (0, 1)
        if direction == GAUCHE:
            vecteur = (-1, 0)
        if direction == DROITE:
            vecteur = (1, 0)

        x, y = self.pos[0], self.pos[1]
        x += -self.carte_mgr.get_of1() + vecteur[0] * (self.speed * 1)  # (dt / 1000))
        y += -self.carte_mgr.get_of2() + vecteur[1] * (self.speed * 1)  # (dt / 1000))

        #Détection des collisions
        x1, y1 = int(x) + self.carte_mgr.get_fov()[0] * TILE_SIZE, \
            int(y) + self.carte_mgr.get_fov()[2] * TILE_SIZE
        x2, y2 = x1 + TILE_SIZE, y1
        x3, y3 = x1, y1 + TILE_SIZE
        x4, y4 = x1 + TILE_SIZE, y1 + TILE_SIZE

        if direction == HAUT:
            if COLLIDE(x1 // TILE_SIZE, y1 // TILE_SIZE, self.carte_mgr.get_carte(), TILECODE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y += TILE_SIZE - decy
            if COLLIDE(x2 // TILE_SIZE, y2 // TILE_SIZE, self.carte_mgr.get_carte(), TILECODE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y += TILE_SIZE - decy

        if direction == GAUCHE:
            if COLLIDE(x1 // TILE_SIZE, y1 // TILE_SIZE, self.carte_mgr.get_carte(), TILECODE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x += TILE_SIZE - decx
            if COLLIDE(x3 // TILE_SIZE, y3 // TILE_SIZE, self.carte_mgr.get_carte(), TILECODE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x += TILE_SIZE - decx

        if direction == DROITE:
            if COLLIDE(x2 // TILE_SIZE, y2 // TILE_SIZE, self.carte_mgr.get_carte(), TILECODE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x -= decx
            if COLLIDE(x4 // TILE_SIZE, y4 // TILE_SIZE, self.carte_mgr.get_carte(), TILECODE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x -= decx

        if direction == BAS:
            if COLLIDE(x3 // TILE_SIZE, y3 // TILE_SIZE, self.carte_mgr.get_carte(), TILECODE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y -= decy
            if COLLIDE(x4 // TILE_SIZE, y4 // TILE_SIZE, self.carte_mgr.get_carte(), TILECODE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y -= decy

        self.pos = (x + self.carte_mgr.get_of1(), y + self.carte_mgr.get_of2())

    def end_move(self):
        self.is_moving = False

    def update(self):
        if not self.is_moving:
            self.perso = self.sprites[self.direction][PAUSE]
        else:
            self.anim_cursor = (self.anim_cursor + 1) % self.max_anim_cursor
        self.render()

    def render(self):
        self.ecran.blit(self.perso, self.pos)

    def get_pos(self):
        return self.pos

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "perso" + EXTENSION)):
            with open(os.path.join("..", "saves", "perso" + EXTENSION), "rb") as read_perso:
                self.pos = pickle.Unpickler(read_perso).load()

    def save(self):
        with open(os.path.join("..", "saves", "perso" + EXTENSION), "wb") as save_perso:
            pickle.Pickler(save_perso).dump(self.pos)