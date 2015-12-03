# coding=utf-8

import os
import pygame
import pickle
from constantes import *
from glob import glob
from carte import CartesManager
import inventaire


class Personnage:
    def __init__(self, ecran: pygame.Surface, carte_mgr: CartesManager, police: pygame.font.Font, pos: tuple=(0, 0)):
        self.ecran = ecran
        self.direction = BAS
        self.police = police
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
        self.inventaire = inventaire.Inventaire(self.ecran, self.police, self.carte_mgr)
        self.last_case = self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE
        self.same_as_before = False

    def inventaire_clic(self, xp: int, yp: int):
        self.inventaire.clic(xp, yp)

    def inventaire_next(self):
        self.inventaire.next()

    def inventaire_previous(self):
        self.inventaire.previous()

    def inventaire_update(self):
        self.inventaire.update(tuple(self.pos))

    def changed_cur_case(self):
        return not self.same_as_before

    def move(self, direction: int=AUCUNE, dt: int=1):
        self.direction = direction
        self.perso = self.sprites[self.direction][self.anim_cursor + 1]
        self.is_moving = True

        self.move_in_fov(direction, dt)

        tmp_obj = self.carte_mgr.get_object_at(self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE)
        if tmp_obj and tmp_obj != OBJET_GET_ERROR:
            self.inventaire.find_object(tmp_obj)

        if self.last_case == (self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE):
            self.same_as_before = True if not self.same_as_before else self.same_as_before
        else:
            self.same_as_before = False

        self.last_case = self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE

    def move_with_fov(self, direction: int=HAUT, dt: int=1):
        new_speed = self.speed * (dt / 10) / self.cur_div

        vecteur = (0, 0)

        if direction == HAUT:
            vecteur = (0, -1)
        if direction == BAS:
            vecteur = (0, 1)
        if direction == GAUCHE:
            vecteur = (-1, 0)
        if direction == DROITE:
            vecteur = (1, 0)

        last_x, last_y = self.pos

        x, y = self.pos[0], self.pos[1]
        x += -self.carte_mgr.get_of1() + vecteur[0] * new_speed
        y += -self.carte_mgr.get_of2() + vecteur[1] * new_speed

        if x < 0 or y < 0 \
                or x - self.sprites[self.direction][self.anim_cursor + 1].get_width() > self.ecran.get_width() \
                or y - self.sprites[self.direction][self.anim_cursor + 1].get_height() > self.ecran.get_height():
            return

        #Détection des collisions
        x1, y1 = x + self.carte_mgr.get_fov()[0] * TILE_SIZE, \
            y + self.carte_mgr.get_fov()[2] * TILE_SIZE
        x2, y2 = x1 + TILE_SIZE, y1
        x3, y3 = x1, y1 + TILE_SIZE
        x4, y4 = x1 + TILE_SIZE, y1 + TILE_SIZE

        if direction == HAUT:
            if self.carte_mgr.collide_at(x1 // TILE_SIZE, y1 // TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y += TILE_SIZE - decy
            if self.carte_mgr.collide_at(x2 // TILE_SIZE, y2 // TILE_SIZE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y += decy

        if direction == GAUCHE:
            if self.carte_mgr.collide_at(x1 // TILE_SIZE, y1 // TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x += TILE_SIZE - decx
            if self.carte_mgr.collide_at(x3 // TILE_SIZE, y3 // TILE_SIZE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x += decx

        if direction == DROITE:
            if self.carte_mgr.collide_at(x2 // TILE_SIZE, y2 // TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x -= decx
            if self.carte_mgr.collide_at(x4 // TILE_SIZE, y4 // TILE_SIZE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x -= decx

        if direction == BAS:
            if self.carte_mgr.collide_at(x3 // TILE_SIZE, y3 // TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y -= decy
            if self.carte_mgr.collide_at(x4 // TILE_SIZE, y4 // TILE_SIZE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y -= decy

        self.carte_mgr.move_of1(x - last_x)
        self.carte_mgr.move_of2(y - last_y)

    def move_in_fov(self, direction: int=HAUT, dt: int=1):
        new_speed = self.speed * (1 / dt * 10) / self.cur_div

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
        x += -self.carte_mgr.get_of1() + vecteur[0] * new_speed
        y += -self.carte_mgr.get_of2() + vecteur[1] * new_speed

        if x < 0 or y < 0 or x > self.ecran.get_width() + 1 or y > self.ecran.get_height() + 1:
            return

        #Détection des collisions
        x1, y1 = x + self.carte_mgr.get_fov()[0] * TILE_SIZE, \
            y + self.carte_mgr.get_fov()[2] * TILE_SIZE
        x2, y2 = x1 + TILE_SIZE, y1
        x3, y3 = x1, y1 + TILE_SIZE
        x4, y4 = x1 + TILE_SIZE, y1 + TILE_SIZE

        if direction == HAUT:
            if self.carte_mgr.collide_at(x1 // TILE_SIZE, y1 // TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y += TILE_SIZE - decy
            if self.carte_mgr.collide_at(x2 // TILE_SIZE, y2 // TILE_SIZE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y += decy

        if direction == GAUCHE:
            if self.carte_mgr.collide_at(x1 // TILE_SIZE, y1 // TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x += TILE_SIZE - decx
            if self.carte_mgr.collide_at(x3 // TILE_SIZE, y3 // TILE_SIZE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x += decx

        if direction == DROITE:
            if self.carte_mgr.collide_at(x2 // TILE_SIZE, y2 // TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x -= decx
            if self.carte_mgr.collide_at(x4 // TILE_SIZE, y4 // TILE_SIZE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x -= decx

        if direction == BAS:
            if self.carte_mgr.collide_at(x3 // TILE_SIZE, y3 // TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y -= decy
            if self.carte_mgr.collide_at(x4 // TILE_SIZE, y4 // TILE_SIZE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y -= decy

        self.pos = (x + self.carte_mgr.get_of1(), y + self.carte_mgr.get_of2())
        if self.changed_cur_case():
            self.carte_mgr.call_trigger_at(int(x // TILE_SIZE) + self.carte_mgr.get_fov()[0],
                                           int(y // TILE_SIZE) + self.carte_mgr.get_fov()[2])

    def isMoving(self):
        return self.is_moving

    def end_move(self):
        self.is_moving = False

    def run(self):
        self.cur_div = DIV_DT_COURSE if self.cur_div != DIV_DT_COURSE else DIV_DT_BASIC

    def ride(self):
        self.cur_div = DIV_DT_VELO if self.cur_div != DIV_DT_VELO else DIV_DT_BASIC

    def update(self):
        if not self.is_moving:
            self.perso = self.sprites[self.direction][PAUSE]
        else:
            self.anim_cursor = (self.anim_cursor + 1) % self.max_anim_cursor
        self.render()

    def render(self):
        self.ecran.blit(self.perso, self.pos)

    def get_pos(self):
        return tuple([int(i) for i in self.pos])

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "perso" + EXTENSION)):
            with open(os.path.join("..", "saves", "perso" + EXTENSION), "rb") as read_perso:
                self.pos = pickle.Unpickler(read_perso).load()
        else:
            # on charge une position par défaut
            self.pos = DEFAULT_POS_AT_BEGINNING
        self.inventaire.load()

    def save(self):
        with open(os.path.join("..", "saves", "perso" + EXTENSION), "wb") as save_perso:
            pickle.Pickler(save_perso).dump(self.pos)
        self.inventaire.save()