# coding=utf-8

from constantes import *
from gui import GUIBulleWaiting
from animator import PlayerAnimator
import ree
from utils import Point


STANDART_MOVE = [
    (0, -1),
    (0, -1),
    (1, 0),
    (1, 0),
    (0, 1),
    (0, 1),
    (-1, 0),
    (-1, 0)
]
CROSS_MOVE = [
    (0, 1),
    (0, 1),
    (-1, 0),
    (-1, 0),
    (1, 0),
    (1, 0),
    (0, 1),
    (0, 1),
    (0, -1),
    (0, -1),
    (1, 0),
    (1, 0),
    (-1, 0),
    (-1, 0),
    (0, 1),
    (0, 1)
]
VERTICAL_MOVE = [
    (0, 1),
    (0, 1),
    (0, 1),
    (0, -1),
    (0, -1),
    (0, -1)
]
HORIZONTAL_MOVE = [
    (1, 0),
    (1, 0),
    (1, 0),
    (-1, 0),
    (-1, 0),
    (-1, 0)
]
STATIC_MOVE = [
    (0, 0)
]


class PNJ:
    def __init__(self, pos: tuple, type_mvt: list, texte: str, dir_: int=1, sprite: str='dad', then: callable=None) -> None:
        self.pos = Point(*[t * TILE_SIZE for t in pos])
        self.type_mvt = type_mvt
        self.font = ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
        self.cur_scheme = 0
        self.real_pos = Point()
        self.speed = TILE_SIZE
        self.speak = False
        self.is_moving = False
        self._a_parcouru = 0
        self.dir = dir_
        self.mdt = 0
        self.orientation = BAS
        self.sprites_anim = PlayerAnimator(os.path.join("..", "assets", "pnj", sprite))
        self.sprites_anim.load()
        self.sprites_anim.set_speed(20)
        self.perso = None
        self.texte = texte
        self.on_speak = None
        self.then = then
        self._screenshot = None

    def _actualise_sprite(self):
        self.perso = self.sprites_anim.get_sprite(self.orientation)

    def update(self, ecran, carte_mgr, dt: int=1):
        self.real_pos.x = carte_mgr.get_of1() + self.pos.x
        self.real_pos.y = carte_mgr.get_of2() + self.pos.y

        self.mdt += dt
        self._actualise_sprite()
        self.sprites_anim.next()

        if not self.mdt % 20:
            self.move(carte_mgr)
            self.pos.x = self.real_pos.x - carte_mgr.get_of1()
            self.pos.y = self.real_pos.y - carte_mgr.get_of2()

        self.render(ecran)

    def get_pos(self) -> tuple:
        return self.pos.pos

    def get_rect(self) -> tuple:
        return ree.create_rect(self.pos.x, self.pos.y, PERSO_SIZE_X, PERSO_SIZE_Y)

    def move_scheme(self):
        self.cur_scheme += self.dir
        if self.cur_scheme + self.dir >= len(self.type_mvt):
            self.cur_scheme = 0

    def speaking(self, dt: int=1):
        return bool(self.on_speak.update(dt))

    def _changed_case(self) -> bool:
        return not self._a_parcouru % TILE_SIZE and self._a_parcouru != 0

    def move(self, carte_mgr):
        if self._changed_case():
            self.move_scheme()

        tmp = self.type_mvt[self.cur_scheme]

        x, y = tmp
        x *= self.speed
        y *= self.speed
        x += self.real_pos.x - carte_mgr.get_of1()
        y += self.real_pos.y - carte_mgr.get_of2()
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
            self.orientation = BAS
        if tmp[1] < 0:
            self.orientation = HAUT

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

        self.real_pos.x = x + carte_mgr.get_of1()
        self.real_pos.y = y + carte_mgr.get_of2()

    def render(self, ecran):
        if 0 <= self.real_pos.x < FEN_large + self.perso.get_width() and 0 <= self.real_pos.y < FEN_haut + self.perso.get_height():
            ecran.blit(self.perso, self.real_pos.pos)

    def player_want_to_talk(self, ecran):
        self.speak = True
        self.on_speak = GUIBulleWaiting(ecran, (PNJ_TXT_XPOS, PNJ_TXT_YPOS), self.texte, self.font)
        self.speak = self.speaking()
        if self.then:
            self.then()