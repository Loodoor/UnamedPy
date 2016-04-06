# coding=utf-8

from constantes import *
from gui import PNJSpeaking


STANDART_MOVE = [
    (0, 0),
    (0, -1),
    (0, -2),
    (1, -2),
    (2, -2),
    (3, -2),
    (3, -1),
    (3, 0),
    (2, 0),
    (1, 0)
]
CROSS_MOVE = [
    (0, 0),
    (0, 1),
    (0, 2),
    (-1, 2),
    (-2, 2),
    (-1, 2),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 3),
    (0, 2),
    (1, 2),
    (2, 2),
    (1, 2),
    (0, 2),
    (0, 1)
]
VERTICAL_MOVE = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3)
]
HORIZONTAL_MOVE = [
    (0, 0),
    (1, 0),
    (2, 0),
    (3, 0)
]


class PNJ:
    def __init__(self, pos: tuple, type_mvt: list, texte: str, dir_: int=1, sprite: str='bas.png') -> None:
        self.pos = list(pos)
        self.type_mvt = type_mvt
        self.font = rendering_engine.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
        self.cur_scheme = 0
        self.real_pos = self.pos
        self.speak = False
        self.dir = dir_
        self.mdt = 0
        self.orientation = BAS
        self.sprite = rendering_engine.load_image(os.path.join("..", "assets", "pnj", sprite))
        self.on_speak = PNJSpeaking(texte, self.font)

    def update(self, ecran, carte_mgr, dt: int=1):
        self.mdt += dt
        self.mdt %= 150
        if not self.mdt:
            self.move(carte_mgr)
        self.render(ecran, dt)

    def get_pos(self):
        return self.pos

    def move_scheme(self):
        self.cur_scheme += self.dir
        if self.cur_scheme + self.dir < 0:
            self.dir = +1
        if self.cur_scheme + self.dir >= len(self.type_mvt):
            self.dir = -1

    def speaking(self, ecran, dt: int=1):
        return self.on_speak.update(ecran, dt)

    def move(self, carte_mgr):
        self.move_scheme()

        tmp = self.type_mvt[self.cur_scheme]

        actual_x, actual_y = tmp
        actual_x *= TILE_SIZE
        actual_y *= TILE_SIZE
        actual_x += self.pos[0]
        actual_y += self.pos[1]

        if tmp[0] > 0:
            self.orientation = DROITE
        if tmp[0] < 0:
            self.orientation = GAUCHE
        if tmp[1] > 0:
            self.orientation = HAUT
        if tmp[1] < 0:
            self.orientation = BAS

        # Détection des collisions
        if self.orientation == HAUT:
            if carte_mgr.collide_at(actual_x // TILE_SIZE, actual_y // TILE_SIZE):
                actual_y += TILE_SIZE
                self.dir = -self.dir

        if self.orientation == GAUCHE:
            if carte_mgr.collide_at(actual_x // TILE_SIZE, actual_y // TILE_SIZE):
                actual_x += TILE_SIZE
                self.dir = -self.dir

        if self.orientation == DROITE:
            if carte_mgr.collide_at(actual_x // TILE_SIZE, actual_y // TILE_SIZE):
                actual_x -= TILE_SIZE
                self.dir = -self.dir

        if self.orientation == BAS:
            if carte_mgr.collide_at(actual_x // TILE_SIZE, actual_y // TILE_SIZE):
                actual_y -= TILE_SIZE
                self.dir = -self.dir

        self.real_pos = (actual_x, actual_y)

    def render(self, ecran, dt: int=1):
        ecran.blit(self.sprite, self.real_pos)
        if self.speak:
            self.speak = self.speaking(ecran, dt)

    def player_want_to_talk(self):
        self.speak = True