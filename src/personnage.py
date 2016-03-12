# coding=utf-8

import pickle
from constantes import *
from carte import CartesManager
from gui import GUIBulleWaiting
from utils import udir_to_vect, unegate_vect
import inventaire
import glob
from animator import PlayerAnimator


class Personnage:
    def __init__(self, carte, ecran: pygame.Surface, police: pygame.font.Font, choice: str, pos: tuple=(0, 0)):
        self.ecran = ecran
        self.direction = BAS
        self.police = police
        self.speed = BASIC_SPEED
        self.path = os.path.join("..", "saves", "pos" + EXTENSION)
        self.cur_div = DIV_DT_BASIC
        self._choice = choice
        self.player_anim = PlayerAnimator(os.path.join("..", "assets", "personnages", self._choice))
        self.perso = self.player_anim.get_sprite_pause(self.direction)
        self.is_moving = False
        self.pos = list(pos)
        self.carte_mgr = carte
        self.inventaire = inventaire.Inventaire(self.ecran, self.police, self.carte_mgr)
        self.last_case = self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE
        self.same_as_before = False

    def get_skin_path(self):
        return self._choice

    def set_carte_mgr(self, new: CartesManager):
        self.carte_mgr = new

    def inventaire_clic(self, xp: int, yp: int):
        self.inventaire.clic(xp, yp)

    def inventaire_next(self):
        self.inventaire.next()

    def inventaire_previous(self):
        self.inventaire.previous()

    def inventaire_update(self):
        self.inventaire.update((self.pos[0] - self.carte_mgr.get_of1(), self.pos[1] - self.carte_mgr.get_of2()))

    def changed_cur_case(self):
        return not self.same_as_before

    def _actualise_sprite(self):
        if self.is_moving:
            self.perso = self.player_anim.get_sprite_moving_from_dir(self.direction)
        else:
            self.perso = self.player_anim.get_sprite_pause(self.direction)

    def _check_collisions(self, direction: int, vecteur: list, new_speed: float) -> tuple:
        inverse_dir = unegate_vect(vecteur)
        new_of1, new_of2 = inverse_dir[0] * new_speed, inverse_dir[1] * new_speed
        x, y = self.pos[0], self.pos[1]
        x += -self.carte_mgr.get_of1() + vecteur[0] * new_speed
        y += -self.carte_mgr.get_of2() + vecteur[1] * new_speed

        # Détection des collisions
        x1, y1 = x, y
        x2, y2 = x1 + TILE_SIZE, y1
        x3, y3 = x1, y1 + TILE_SIZE
        x4, y4 = x1 + TILE_SIZE, y1 + TILE_SIZE

        if direction == HAUT:
            if self.carte_mgr.collide_at(x1 / TILE_SIZE, y1 / TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y += TILE_SIZE - decy
                new_of2 -= TILE_SIZE - decy
            elif self.carte_mgr.collide_at(x2 / TILE_SIZE, y2 / TILE_SIZE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y += TILE_SIZE - decy
                    new_of2 -= TILE_SIZE - decy

        if direction == GAUCHE:
            if self.carte_mgr.collide_at(x1 / TILE_SIZE, y1 / TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x += TILE_SIZE - decx
                new_of1 -= TILE_SIZE - decx
            elif self.carte_mgr.collide_at(x3 / TILE_SIZE, y3 / TILE_SIZE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x += TILE_SIZE - decx
                    new_of1 -= TILE_SIZE - decx

        if direction == DROITE:
            if self.carte_mgr.collide_at(x2 / TILE_SIZE, y2 / TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x -= decx
                new_of1 += decx
            elif self.carte_mgr.collide_at(x4 / TILE_SIZE, y4 / TILE_SIZE):
                if y % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    x -= decx
                    new_of1 += decx

        if direction == BAS:
            if self.carte_mgr.collide_at(x3 / TILE_SIZE, y3 / TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y -= decy
                new_of2 += decy
            elif self.carte_mgr.collide_at(x4 / TILE_SIZE, y4 / TILE_SIZE):
                if x % TILE_SIZE:
                    decx, decy = x % TILE_SIZE, y % TILE_SIZE
                    y -= decy
                    new_of2 += decy

        return x, y, new_of1, new_of2

    def move(self, direction: int=AUCUNE, dt: int=1):
        self.direction = direction
        self.player_anim.next()
        self._actualise_sprite()
        self.is_moving = True

        self._move_player(direction, dt)

        tmp_obj = self.carte_mgr.get_object_at(
            (self.pos[0] - self.carte_mgr.get_of1()) // TILE_SIZE,
            (self.pos[1] - self.carte_mgr.get_of2()) // TILE_SIZE
        )
        if tmp_obj and tmp_obj != OBJET_GET_ERROR:
            g = GUIBulleWaiting(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Youpi ! Vous venez de trouver " +
                                str(tmp_obj[0].nombre()) + " " + str(tmp_obj[0].name()) + " !",
                                self.police)
            g.update()
            del g
            self.inventaire.find_object(tmp_obj)

        if self.last_case == (self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE):
            self.same_as_before = True if not self.same_as_before else self.same_as_before
        else:
            self.same_as_before = False

        self.last_case = self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE

        self.carte_mgr.check_changing_map((self.pos[0] - self.carte_mgr.get_of1()) // TILE_SIZE,
                                          (self.pos[1] - self.carte_mgr.get_of2()) // TILE_SIZE)

    def _move_player(self, direction: int=HAUT, dt: int=1):
        new_speed = self.speed * (dt / 50) / self.cur_div

        vecteur = udir_to_vect(direction)

        x, y, new_of1, new_of2 = self._check_collisions(direction, vecteur, new_speed)

        if len(self.carte_mgr.get_carte()) * TILE_SIZE < FEN_haut and len(self.carte_mgr.get_carte()[0]) * TILE_SIZE < FEN_large:
            self.pos = (x + self.carte_mgr.get_of1(), y + self.carte_mgr.get_of2())
        elif len(self.carte_mgr.get_carte()) * TILE_SIZE < FEN_haut and len(self.carte_mgr.get_carte()[0]) * TILE_SIZE >= FEN_large:
            self.pos = (self.pos[0], y + self.carte_mgr.get_of2())
            self.carte_mgr.move_of1(new_of1)
        elif len(self.carte_mgr.get_carte()) * TILE_SIZE >= FEN_haut and len(self.carte_mgr.get_carte()[0]) * TILE_SIZE < FEN_large:
            self.pos = (x + self.carte_mgr.get_of1(), self.pos[1])
            self.carte_mgr.move_of2(new_of2)
        else:
            self.carte_mgr.move_of1(new_of1)
            self.carte_mgr.move_of2(new_of2)

        if self.changed_cur_case():
            self.carte_mgr.call_trigger_at(int(x // TILE_SIZE), int(y // TILE_SIZE))

    def is_moving_or_not(self):
        return self.is_moving

    def end_move(self):
        self.is_moving = False
        self.player_anim.pause()

    def walk(self):
        self.cur_div = DIV_DT_BASIC

    def run(self):
        self.cur_div = DIV_DT_COURSE if self.cur_div != DIV_DT_COURSE else DIV_DT_BASIC

    def ride(self):
        self.cur_div = DIV_DT_VELO if self.cur_div != DIV_DT_VELO else DIV_DT_BASIC

    def get_dir(self):
        return self.direction

    def update(self):
        if not self.is_moving:
            self.player_anim.pause()
            self._actualise_sprite()
        else:
            self.player_anim.next()
        self.render()

    def render(self):
        self.ecran.blit(self.perso, self.pos)

    def get_pos(self):
        return tuple(int(i) for i in self.pos)

    def get_pos_in_tiles(self):
        pos_px = self.get_pos()
        return (pos_px[0] - self.carte_mgr.get_of1()) // TILE_SIZE, (pos_px[1] - self.carte_mgr.get_of2()) // TILE_SIZE

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as read_perso:
                self.pos = pickle.Unpickler(read_perso).load()
        else:
            # on charge une position par défaut
            self.pos = DEFAULT_POS_AT_BEGINNING
        self.inventaire.load()
        self.player_anim.set_speed(20)

    def save(self):
        with open(self.path, "wb") as save_perso:
            pickle.Pickler(save_perso).dump(self.pos)
        self.inventaire.save()


class OthPersonnagesManager:
    def __init__(self, ecran: pygame.Surface):
        self.ecran = ecran
        self._others = {}
        self._sprites = {}
        for dir_ in glob.glob(os.path.join("..", "assets", "personnages", "*")):
            directory = os.path.split(dir_)[1]
            self._sprites[directory] = {}
            self._sprites[directory][BAS] = [
                pygame.image.load(i).convert_alpha() for i in glob.glob(os.path.join(dir_, "bas*.png"))
            ]
            self._sprites[directory][HAUT] = [
                pygame.image.load(i).convert_alpha() for i in glob.glob(os.path.join(dir_, "haut*.png"))
            ]
            self._sprites[directory][GAUCHE] = [
                pygame.image.load(i).convert_alpha() for i in glob.glob(os.path.join(dir_, "gauche*.png"))
            ]
            self._sprites[directory][DROITE] = [
                pygame.image.load(i).convert_alpha() for i in glob.glob(os.path.join(dir_, "droite*.png"))
            ]

    def add_new(self, id_: float, avatar: str, pseudo: str):
        self._others[id_] = {}
        self._others[id_]['avatar'] = avatar
        self._others[id_]['pseudo'] = pseudo
        self._others[id_]['state'] = PAUSE

    def move_this(self, perso: dict):
        id_ = perso['id']
        if id_ not in self._others.keys():
            self.add_new(id_, perso['avatar'], perso['pseudo'])
        self._others[id_]["pos"] = perso['pos']
        self._others[id_]['direction'] = perso['dir']

    def draw_them(self):
        if self._others:
            for id_, perso in self._others.items():
                self.ecran.blit(self._sprites[perso["avatar"]][perso['direction']][perso['state']], perso['pos'])