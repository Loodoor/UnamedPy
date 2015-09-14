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
        self.speed = BASIC_SPEED
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
        self.perso = self.sprites[self.direction][self.anim_cursor+1]
        self.is_moving = True

        x, y = self.pos[0] + self.carte_mgr.get_of1() + self.carte_mgr.get_fov()[0] * TILE_SIZE, \
            self.pos[1] + self.carte_mgr.get_of2() + self.carte_mgr.get_fov()[2] * TILE_SIZE
        x2, y2 = x + x % TILE_SIZE if (x + TILE_SIZE) % TILE_SIZE != x else x, \
                 y + y % TILE_SIZE if (y + TILE_SIZE) % TILE_SIZE != y else y
        x3, y3 = x, y2
        x4, y4 = x2, y

        pos_possibles = [(x, y)]

        if (x, y) == (x2, y2) == (x4, y4) != (x3, y3):
            print('in start x3y3')
            if direction == GAUCHE or direction == DROITE:
                print('in x3y3')
                pos_possibles.append((x3, y3))
        if (x, y) == (x2, y2) == (x3, y3) != (x4, y4):
            print('in start x4y4')
            if direction == HAUT or direction == BAS:
                print('in x4y4')
                pos_possibles.append((x4, y4))
        if (x, y) != (x2, y2) != (x3, y3) != (x4, y4):
            pos_possibles.append((x2, y2))
            pos_possibles.append((x3, y3))
            pos_possibles.append((x4, y4))

        vecteur = (0, 0)

        if direction == HAUT:
            vecteur = (0, -1)
        if direction == BAS:
            vecteur = (0, 1)
        if direction == GAUCHE:
            vecteur = (-1, 0)
        if direction == DROITE:
            vecteur = (1, 0)

        #Détection des collisions
        can_move = False
        for i in pos_possibles:
            nx = i[0] // TILE_SIZE + vecteur[0]
            ny = i[1] // TILE_SIZE + vecteur[1]
            if not COLLIDE(nx, ny, self.carte_mgr.get_carte(), TILECODE):
                can_move = True
            else:
                can_move = False
                break

        if can_move:
            x, y = self.pos[0], self.pos[1]
            x += vecteur[0] * self.speed
            y += vecteur[1] * self.speed
            self.pos = (x, y)

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

    def load(self):
        if os.path.exists(os.path.join("..", "saves", "perso" + EXTENSION)):
            with open(os.path.join("..", "saves", "perso" + EXTENSION), "rb") as read_perso:
                self.pos = pickle.Unpickler(read_perso).load()

    def save(self):
        with open(os.path.join("..", "saves", "perso" + EXTENSION), "wb") as save_perso:
            pickle.Pickler(save_perso).dump(self.pos)