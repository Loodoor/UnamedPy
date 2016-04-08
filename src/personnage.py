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
    def __init__(self, carte, ecran, police, choice: str, pos: tuple=(0, 0)):
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

    def _check_collisions(self, direction: int, vecteur: list, new_speed: float, pnjs: list) -> tuple:
        inverse_dir = unegate_vect(vecteur)
        new_of1, new_of2 = inverse_dir[0] * new_speed, inverse_dir[1] * new_speed
        x, y = self.pos[0], self.pos[1]
        x += -self.carte_mgr.get_of1() + vecteur[0] * new_speed
        y += -self.carte_mgr.get_of2() + vecteur[1] * new_speed
        tile_code = self.carte_mgr.get_tile_code_at(x // TILE_SIZE, y // TILE_SIZE)

        # pré-traitement avec les tiles de jump
        jump_dict = self.carte_mgr.specials_blocs['jumping']
        if tile_code in jump_dict["content"]:
            tile_specs = jump_dict[tile_code]
            if tile_specs["from"] == "RIGHT" and direction == GAUCHE:
                if tile_specs["to"] == "LEFT":
                    x -= TILE_SIZE
            if tile_specs["from"] == "LEFT" and direction == DROITE:
                if tile_specs["to"] == "RIGHT":
                    x += TILE_SIZE
            if tile_specs["from"] == "TOP" and direction == BAS:
                if tile_specs["to"] == "BOTTOM":
                    y += TILE_SIZE
            if tile_specs["from"] == "BOTTOM" and direction == HAUT:
                if tile_specs["to"] == "TOP":
                    y -= TILE_SIZE

        # Détection des collisions avec les tiles et les pnjs (d'une pierre 2 coups :D)
        pnjs_rect = [pnj.get_rect() for pnj in pnjs]

        def colliding(i: int, j: int):
            carte = self.carte_mgr.collide_at(i, j)
            pnj = rendering_engine.create_rect(int(i) * TILE_SIZE, int(j) * TILE_SIZE, TILE_SIZE, TILE_SIZE).collidelist(pnjs_rect)
            return carte or pnj != -1

        x1, y1 = x, y
        x2, y2 = x1 + TILE_SIZE, y1
        x3, y3 = x1, y1 + TILE_SIZE
        x4, y4 = x1 + TILE_SIZE, y1 + TILE_SIZE

        if direction == HAUT:
            if colliding(x1 / TILE_SIZE, y1 / TILE_SIZE) or (colliding(x2 / TILE_SIZE, y2 / TILE_SIZE) and x % TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                y += TILE_SIZE - decy
                new_of2 -= TILE_SIZE - decy

        if direction == GAUCHE:
            if colliding(x1 / TILE_SIZE, y1 / TILE_SIZE) or (self.carte_mgr.collide_at(x3 / TILE_SIZE, y3 / TILE_SIZE) and y % TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x += TILE_SIZE - decx
                new_of1 -= TILE_SIZE - decx

        if direction == DROITE:
            if colliding(x2 / TILE_SIZE, y2 / TILE_SIZE) or (colliding(x4 / TILE_SIZE, y4 / TILE_SIZE) and y % TILE_SIZE):
                decx, decy = x % TILE_SIZE, y % TILE_SIZE
                x -= decx
                new_of1 += decx

        if direction == BAS:
            if colliding(x3 / TILE_SIZE, y3 / TILE_SIZE) or (colliding(x4 / TILE_SIZE, y4 / TILE_SIZE) and x % TILE_SIZE):
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
        del tmp_obj

        self.same_as_before = self.last_case == ((self.pos[0] - self.carte_mgr.get_of1()) // TILE_SIZE, (self.pos[1] - self.carte_mgr.get_of2()) // TILE_SIZE)

        self.last_case = (self.pos[0] - self.carte_mgr.get_of1()) // TILE_SIZE, (self.pos[1] - self.carte_mgr.get_of2()) // TILE_SIZE

        self.carte_mgr.check_changing_map((self.pos[0] - self.carte_mgr.get_of1()) // TILE_SIZE,
                                          (self.pos[1] - self.carte_mgr.get_of2()) // TILE_SIZE)

    def _move_player(self, direction: int=HAUT, dt: int=1):
        new_speed = self.speed * (dt / 50) / self.cur_div

        vecteur = udir_to_vect(direction)
        pnjs = self.carte_mgr.get_pnjs()

        x, y, new_of1, new_of2 = self._check_collisions(direction, vecteur, new_speed, pnjs)

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
    def __init__(self, ecran):
        self.ecran = ecran
        self._others = {}
        self._sprites = {}
        for dir_ in glob.glob(os.path.join("..", "assets", "personnages", "*")):
            directory = os.path.split(dir_)[1]
            self._sprites[directory] = {}
            self._sprites[directory][BAS] = [
                rendering_engine.load_image(i) for i in glob.glob(os.path.join(dir_, "bas*.png"))
            ]
            self._sprites[directory][HAUT] = [
                rendering_engine.load_image(i) for i in glob.glob(os.path.join(dir_, "haut*.png"))
            ]
            self._sprites[directory][GAUCHE] = [
                rendering_engine.load_image(i) for i in glob.glob(os.path.join(dir_, "gauche*.png"))
            ]
            self._sprites[directory][DROITE] = [
                rendering_engine.load_image(i) for i in glob.glob(os.path.join(dir_, "droite*.png"))
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