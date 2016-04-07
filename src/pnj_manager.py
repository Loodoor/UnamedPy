# coding=utf-8

from constantes import *
from gui import PNJSpeaking
from animator import PlayerAnimator


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
    def __init__(self, pos: tuple, type_mvt: list, texte: str, dir_: int=1, sprite: str='first') -> None:
        self.pos = list(pos)
        self.type_mvt = type_mvt
        self.font = rendering_engine.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
        self.cur_scheme = 0
        self.real_pos = self.pos
        self.speed = 4
        self.speak = False
        self.is_moving = False
        self._a_parcouru = 0
        self.dir = dir_
        self.mdt = 0
        self.orientation = BAS
        self.sprites_anim = PlayerAnimator(os.path.join("..", "assets", "pnj", sprite))
        self.perso = None
        self.sprites_anim.set_speed(20)
        self.on_speak = PNJSpeaking(texte, self.font)
        self._rect = tuple(self.get_pos()) + tuple(self.sprites_anim.get_sprite_pause(self.orientation).get_size())

    def _actualise_sprite(self):
        if self.is_moving:
            self.perso = self.sprites_anim.get_sprite_moving_from_dir(self.orientation)
        else:
            self.perso = self.sprites_anim.get_sprite_pause(self.orientation)

    def update(self, ecran, carte_mgr, dt: int=1):
        self.mdt += dt
        self.sprites_anim.next()
        self._actualise_sprite()

        if not self.mdt % 150:
            self.move(carte_mgr)

        self.render(ecran, dt)

    def get_pos(self) -> tuple:
        return self.pos

    def get_rect(self) -> tuple:
        return self._rect

    def move_scheme(self):
        self.cur_scheme += self.dir
        if self.cur_scheme + self.dir < 0:
            self.dir = +1
        if self.cur_scheme + self.dir >= len(self.type_mvt):
            self.dir = -1

    def speaking(self, ecran, dt: int=1):
        return self.on_speak.update(ecran, dt)

    def _changed_case(self) -> bool:
        return not self._a_parcouru % TILE_SIZE

    def move(self, carte_mgr):
        if self._changed_case():
            self.move_scheme()

        tmp = self.type_mvt[self.cur_scheme]

        x, y = tmp
        x *= self.speed
        y *= self.speed
        x += self.pos[0] - carte_mgr.get_of1()
        y += self.pos[1] - carte_mgr.get_of2()
        x1, y1 = x, y
        x2, y2 = x1 + TILE_SIZE, y1
        x3, y3 = x1, y1 + TILE_SIZE
        x4, y4 = x1 + TILE_SIZE, y1 + TILE_SIZE

        self._a_parcouru += self.speed

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
            if carte_mgr.collide_at(x1 / TILE_SIZE, y1 / TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y += TILE_SIZE - decy
                self._a_parcouru += TILE_SIZE - decy
            elif carte_mgr.collide_at(x2 / TILE_SIZE, y2 / TILE_SIZE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y += TILE_SIZE - decy
                    self._a_parcouru += TILE_SIZE - decy

        if self.orientation == GAUCHE:
            if carte_mgr.collide_at(x1 / TILE_SIZE, y1 / TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x += TILE_SIZE - decx
                self._a_parcouru += TILE_SIZE - decx
            elif carte_mgr.collide_at(x3 / TILE_SIZE, y3 / TILE_SIZE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x += TILE_SIZE - decx
                    self._a_parcouru += TILE_SIZE - decx

        if self.orientation == DROITE:
            if carte_mgr.collide_at(x2 / TILE_SIZE, y2 / TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x -= decx
                self._a_parcouru -= decx
            elif carte_mgr.collide_at(x4 / TILE_SIZE, y4 / TILE_SIZE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x -= decx
                    self._a_parcouru -= decx

        if self.orientation == BAS:
            if carte_mgr.collide_at(x3 / TILE_SIZE, y3 / TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y -= decy
                self._a_parcouru -= decy
            elif carte_mgr.collide_at(x4 / TILE_SIZE, y4 / TILE_SIZE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y -= decy
                    self._a_parcouru -= decy

        self.real_pos = (x + carte_mgr.get_of1(), y + carte_mgr.get_of2())

    def render(self, ecran, dt: int=1):
        if 0 <= self.real_pos[0] < FEN_large + self.perso.get_width() and 0 <= self.real_pos[1] < FEN_haut + self.perso.get_height():
            ecran.blit(self.perso, self.real_pos)
        if self.speak:
            self.speak = self.speaking(ecran, dt)

    def player_want_to_talk(self):
        self.speak = True