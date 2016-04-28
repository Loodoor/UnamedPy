# coding=utf-8

from exceptions import ListePleine
import glob
from constantes import *
import debug


class BaseSideAnimator:
    def __init__(self, base_image: ree.surf, velocity: float, vertical: bool):
        self.base_image = base_image
        self.velocity = velocity
        self.decalage = int(self.base_image.get_width() // self.velocity + 1)
        self.output = []
        self.time = 0
        self.vertical = vertical

    def load(self):
        if self.output:
            raise ListePleine

        time_ = 0
        for _ in range(self.decalage):
            surf = ree.create_surface((TILE_SIZE, TILE_SIZE))
            surf.fill((76, 76, 76))
            surf.set_colorkey((76, 76, 76))

            if not self.vertical:
                surf.blit(self.base_image, (time_ - self.base_image.get_width(), 0))
                surf.blit(self.base_image, (time_, 0))
            else:
                surf.blit(self.base_image, (0, time_ - self.base_image.get_height()))
                surf.blit(self.base_image, (0, time_))

            surf.convert_alpha()

            time_ += self.velocity
            time_ %= self.base_image.get_width()
            self.output.append(surf)

    def next(self):
        self.time += self.velocity

    def draw_at(self, ecran: ree.surf, pos: tuple=(-1, -1)):
        ecran.blit(self.output[int(self.time % len(self.output))], pos)


class BaseMultipleSpritesAnimator:
    def __init__(self, path: str):
        self.path = path
        self.anims = []
        if os.path.exists(os.path.join(path, "config.txt")):
            self._config_file = eval(open(os.path.join(path, "config.txt"), "r", encoding="utf-8").read())
        else:
            self._config_file = {}
        self._wait = self._config_file.get("anim_time", ANIM_DEFAULT_SPEED_MSPA)
        self._cur_anim = 0
        self._max_anim = 0
        self._last_time = 0

        self._create_anims()

    def next(self):
        if self._last_time + self._wait <= time.time():
            self._cur_anim += 1
            self._cur_anim %= self._max_anim

            self._last_time = time.time()

    def get_anim(self):
        return self.anims[self._cur_anim]

    def _create_anims(self):
        for img in glob.glob(os.path.join(self.path, "*.png")):
            self.anims.append(ree.load_image(img))
            self._max_anim += 1


class FluidesAnimator(BaseSideAnimator):
    def __init__(self, base_image, velocity: float):
        super().__init__(base_image, velocity, False)

    def get_anim(self):
        return self.output[int(self.time % len(self.output))]


class PlayerAnimator:
    def __init__(self, path: str=""):
        self.path = path
        self.anims = {}
        self.masks = {}
        self._cur_anim = STATES_MOVE.idle
        self.curseur = 0
        self.idle = [PAUSE, ANIM2]
        self.walking = [ANIM1, ANIM2, ANIM3]
        self.running = [ANIM1, ANIM3]
        self.riding = [RIDE1, RIDE2, RIDE3]
        self._count = 0
        self._tot = 0
        self.speed = 1

    def get_state(self) -> int:
        return self._cur_anim

    def set_speed(self, new: int):
        self.speed = new

    def load(self):
        self._create_anims()
        self._create_masks()
        debug.println("Animateur chargé, anims : {}, masks : {}".format(self.anims is not None, self.masks is not None))

    def next(self):
        if not self._count:
            self._cur_anim = STATES_MOVE.walking
        self._tot += 1
        if not self._tot % self.speed:
            self._count += 1

    def set_state(self, state: int):
        self._cur_anim = state  # dans STATES_MOVE

    def get_anim_cursor(self) -> int:
        if self._cur_anim == STATES_MOVE.idle:
            return self._count % len(self.idle)
        elif self._cur_anim == STATES_MOVE.walking:
            return self._count % len(self.walking)
        elif self._cur_anim == STATES_MOVE.riding:
            return self._count % len(self.riding)
        else:
            # self._cur_anim == STATES_MOVE.running
            return self._count % len(self.running)

    def get_sprite_path(self) -> str:
        return self.path

    def get_sprite_pause(self, direc: int) -> ree.surf:
        if direc in self.anims.keys():
            # ici on assume complètement qu'il est pas en mouvement
            return self.anims[direc][self.idle[self.get_anim_cursor()]]
        raise ValueError("La clé '{}' n'existe pas pour le dictionnaire self.anims".format(direc))

    def get_sprite(self, direc: int, anim_curs: int=-1) -> ree.surf:
        if direc in self.anims.keys():
            if anim_curs == -1:
                anim_curs = self.get_anim_cursor()
            move_lst = self.walking if self._cur_anim == STATES_MOVE.walking else self.running if self._cur_anim == STATES_MOVE.running else self.riding if self._cur_anim == STATES_MOVE.riding else self.idle
            return self.anims[direc][move_lst[anim_curs % len(move_lst)]]
        raise ValueError("La clé '{}' n'existe pas pour le dictionnaire self.anims".format(direc))

    def get_mask(self, direc: int, anim_curs: int=-1) -> list:
        if direc in self.masks.keys():
            if anim_curs == -1:
                anim_curs = self.get_anim_cursor()
            move_lst = self.walking if self._cur_anim == STATES_MOVE.walking else self.running if self._cur_anim == STATES_MOVE.running else self.riding if self._cur_anim == STATES_MOVE.riding else self.idle
            return self.masks[direc][move_lst[anim_curs % len(move_lst)]]
        raise ValueError("La clé '{}' n'existe pas pour le dictionnaire self.masks".format(direc))

    def get_sprite_moving_from_dir(self, direc: int):
        return self.get_sprite(direc, self.get_anim_cursor())

    def get_mask_moving_from_dir(self, direc: int):
        return self.get_mask(direc, self.get_anim_cursor())

    def _create_anims(self):
        debug.println(self.path)
        lhaut = [ree.load_image(_, True) for _ in glob.glob(os.path.join(self.path, "haut*.png"))]
        lbas = [ree.load_image(_, True) for _ in glob.glob(os.path.join(self.path, "bas*.png"))]
        lgauche = [ree.load_image(_, True) for _ in glob.glob(os.path.join(self.path, "gauche*.png"))]
        ldroite = [ree.load_image(_, True) for _ in glob.glob(os.path.join(self.path, "droite*.png"))]

        self.anims = {
            HAUT: lhaut,
            BAS: lbas,
            GAUCHE: lgauche,
            DROITE: ldroite
        }

        for li in self.anims.values():
            for ei in li:
                ei.set_colorkey((255, 0, 255))

    def _create_masks(self):
        self.masks = {k: [ree.create_mask_from_surface(e).get_bounding_rects() for e in v] for k, v in self.anims.items()}