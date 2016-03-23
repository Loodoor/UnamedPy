# coding=utf-8

from exceptions import ListePleine
import glob
from constantes import *


class BaseSideAnimator:
    def __init__(self, base_image: object, velocity: float, vertical: bool):
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
            surf = rendering_engine.create_surface((TILE_SIZE, TILE_SIZE))
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

    def _draw(self):
        self.time += self.velocity

    def draw_at(self, ecran: object, pos: tuple=(-1, -1)):
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
            self.anims.append(rendering_engine.load_image(img).convert_alpha())
            self._max_anim += 1


class FluidesAnimator(BaseSideAnimator):
    def __init__(self, base_image, velocity: float):
        super().__init__(base_image, velocity, False)

    def next(self):
        self._draw()

    def get_anim(self):
        return self.output[int(self.time % len(self.output))]


class PlayerAnimator:
    def __init__(self, path: str):
        self.path = path
        self.anims = {}
        self._cur_anim = PAUSE
        self._correspondances = {
            PAUSE: ANIM1,
            ANIM1: ANIM2,
            ANIM2: ANIM1
        }
        self._moves = {key: value for key, value in self._correspondances.items() if key != PAUSE}
        self._speed = 1
        self._count = 0

        self._create_anims()

    def set_speed(self, speed: int):
        self._speed = speed

    def pause(self):
        self._cur_anim = PAUSE

    def next(self):
        self._count += 1
        if not self._count % self._speed:
            self._cur_anim += 1
            self._count = 1

    def get_anim_cursor(self):
        return self._cur_anim % 3

    def get_sprite_pause(self, direc: int):
        if direc in self.anims.keys():
            # ici on assume complètement qu'il est en mouvement
            return self.anims[direc][PAUSE]
        raise ValueError("La clé '{}' n'existe pas pour le dictionnaire self.anims".format(direc))

    def get_sprite(self, direc: int, anim_curs: int):
        if direc in self.anims.keys():
            if anim_curs < len(self.anims):
                return self.anims[direc][anim_curs]
            raise ValueError("L'animation demandée n'existe pas (n°{})".format(anim_curs))
        raise ValueError("La clé '{}' n'existe pas pour le dictionnaire self.anims".format(direc))

    def get_sprite_moving_from_dir(self, direc: int):
        if direc in self.anims.keys():
            # ici on assume complètement qu'il est en mouvement
            return self.anims[direc][(self.get_anim_cursor() % 2) + 1]
        raise ValueError("La clé '{}' n'existe pas pour le dictionnaire self.anims".format(direc))

    def _create_anims(self):
        lhaut = [rendering_engine.load_image(_).convert_alpha() for _ in glob.glob(os.path.join(self.path, "haut*.png"))]
        lbas = [rendering_engine.load_image(_).convert_alpha() for _ in glob.glob(os.path.join(self.path, "bas*.png"))]
        lgauche = [rendering_engine.load_image(_).convert_alpha() for _ in glob.glob(os.path.join(self.path, "gauche*.png"))]
        ldroite = [rendering_engine.load_image(_).convert_alpha() for _ in glob.glob(os.path.join(self.path, "droite*.png"))]

        self.anims = {
            HAUT: lhaut,
            BAS: lbas,
            GAUCHE: lgauche,
            DROITE: ldroite
        }