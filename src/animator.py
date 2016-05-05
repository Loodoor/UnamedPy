# coding=utf-8

from exceptions import ListePleine, CinematiqueIntrouvable
import debug
from gui import *


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
        try:
            with open(os.path.join(path, "config" + EXTENSION), "r", encoding="utf-8") as file:
                self._config_file = eval(file.read())
        except OSError:
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
        for img in glob(os.path.join(self.path, "*.png")):
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
        lhaut = [ree.load_image(_, True) for _ in glob(os.path.join(self.path, "haut*.png"))]
        lbas = [ree.load_image(_, True) for _ in glob(os.path.join(self.path, "bas*.png"))]
        lgauche = [ree.load_image(_, True) for _ in glob(os.path.join(self.path, "gauche*.png"))]
        ldroite = [ree.load_image(_, True) for _ in glob(os.path.join(self.path, "droite*.png"))]

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


class Fading:
    def __init__(self, duration: float, ecran: ree.surf, *args):
        self.type = "in" if "in" in args else "out"
        self.duration = int(duration * 1000)
        self._time = 0
        self.ecran = ecran
        self.modifier = 255 / self.duration * 10
        self._surfaces = []
        self._count = 0
        self._playing = False
        self._load()
        self._diviseur = self.duration / len(self._surfaces) * 10

    def _load(self):
        for i in range(self.duration // 10):
            surf = ree.create_surface((FEN_large, FEN_haut), ree.get_alpha_channel(), 32)
            surf.convert_alpha()
            surf.fill((0, 0, 0, int(i * self.modifier)))
            self._surfaces.append(surf)
        if self.type == "in":
            self._surfaces = self._surfaces[::-1]

    def playing(self) -> bool:
        return self._playing

    def current(self) -> str:
        return self.type

    def reverse(self):
        self._surfaces = self._surfaces[::-1]

    def reinit(self):
        self._count = 0
        self._time = 0
        self._playing = False

    def start(self):
        self._playing = True

    def render(self):
        self.ecran.blit(self._surfaces[int(self._count)], (0, 0))
        if self._time >= self._count * self._diviseur:
            self._count += self.modifier
        if self._count >= len(self._surfaces):
            self._count = len(self._surfaces) - 1

    def update(self, dt: float):
        self._time += dt
        if self._time >= self.duration:
            self._playing = False
            return
        self.render()


class CinematiqueCreator:
    def __init__(self, ecran: ree.surf, path: str):
        self.ecran = ecran
        self.path = path
        self._images = {}
        self._sounds = {}
        self._conf = {}
        self._loaded = False
        self._running = False
        self.font = ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
        self._current = None
        self._clock = ree.create_clock()
        self._time = 0
        self._playing_music = False
        self._displaying_text = False
        self._text = None
        self._fade = None

    def load(self):
        if not self._loaded:
            try:
                with open(self.path, "r", encoding="utf-8") as conf:
                    self._conf = eval(conf.read())
                for file in glob(os.path.join(self._conf["frames_folder"], "*.*")):
                    self._images[os.path.basename(file)] = ree.load_image(file)
                for file in glob(os.path.join(self._conf["musics_folder"], "*.*")):
                    self._sounds[os.path.basename(file)] = ree.load_music_object(file)
                self._current = self._conf["frames_order"][0]
                self._fade = Fading(self._conf["fade_duration"], self.ecran, "in")
            except OSError:
                raise CinematiqueIntrouvable("Avec le path suivant :", self.path)
            self._loaded = True

    def _process_event(self, ev: ree.Event):
        if ev == ree.QUIT:
            exit(1)
        if ev == ree.KEYDOWN:
            self._next()

    def _render(self, ev: ree.Event, dt: float):
        self.ecran.blit(self._images[self._conf["frames"][self._current]["image"]], self._conf["frames"][self._current]["position"])

        # fadeout
        if self._conf["frames"][self._current].get("fadeout", False) and self._time >= self._conf["frames"][self._current].get("duration", 99999) * 1000 - self._conf["fade_duration"] * 1000:
            if self._fade.current() == "in" and not self._fade.playing():
                self._fade.reverse()
            if not self._fade.playing():
                self._fade.reinit()
                self._fade.start()
        # début affichage texte
        if self._time >= self._conf["frames"][self._current]["text"].get("at_time", 0) * 1000 and not self._displaying_text:
            self._displaying_text = True
            if self._conf["frames"][self._current]["text"].get("type", "plain") == "plain":
                self._text = GUIBulle(
                    self.ecran,
                    (POS_BULLE_X, POS_BULLE_Y),
                    self._conf["frames"][self._current]["text"].get("content", ""),
                    self.font,
                    self._conf["frames"][self._current]["text"].get("with_gui", True)
                )
                if self._conf["frames"][self._current]["text"].get("with_gui", True):
                    cl = self._conf["frames"][self._current]["text"].get("color", None)
                    if cl:
                        self._text.set_color(cl)
        # fin affichage texte
        if self._time >= self._conf["frames"][self._current]["text"].get("end_at", 0) * 1000 and self._displaying_text and \
                self._conf["frames"][self._current]["text"].get("end_at", -1) != -1:
            self._displaying_text = False
            self._text = None

        if self._displaying_text and self._text:
            self._text.update_one_frame(ev)
        if self._fade.playing():
            self._fade.update(dt)

    def _next(self):
        self._time = 0
        last = self._current

        err = False
        try:
            self._current = self._conf["frames_order"][self._conf["frames_order"].index(self._current) + 1]
        except IndexError:
            err = True
            self._running = False

        # continuation de la musique
        if self._playing_music and not self._conf["frames"][self._current].get("last_music_continue_here", False):
            self._sounds[self._conf["frames"][last]["music"]].stop()
        # fadein
        if self._conf["frames"][self._current].get("fadein", False) and not err:
            if self._fade.current() == "out" and not self._fade.playing():
                self._fade.reverse()
            if not self._fade.playing():
                self._fade.reinit()
                self._fade.start()
        # music
        if self._conf["frames"][self._current].get("music", False) and not err:
            self._playing_music = True
            self._sounds[self._conf["frames"][self._current]["music"]].play()

    def play(self):
        self._running = True

        debug.println(self._time)

        # on a besoin d'une configuration pour faire tourner la cinématique
        while self._running and self._conf:
            dt = self._clock.tick()  # le dt est en ms
            self._time += dt

            ev = ree.poll_event()
            self._process_event(ev)

            if self._time >= self._conf["frames"][self._current].get("duration", 0) * 1000:
                self._next()

            self._render(ev, dt)

            ree.flip()