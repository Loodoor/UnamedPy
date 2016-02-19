# coding=utf-8

import pickle
from glob import glob
import pygame
from constantes import *
from trigger_manager import TriggersManager
from exceptions import FonctionnaliteNonImplementee, CarteInexistante, ErreurContenuCarte
from utils import udel_same_occurence
from animator import FluidesAnimator, BaseMultipleSpritesAnimator
from random import randint


class SubCarte:
    """
    chaque carte crée ses propres PNJ et s'occupe de les afficher
    chaque carte s'occupe aussi de gérer ses objets (au sol), et les chemins vers d'autres cartes
    elles gérent aussi leur ZID
    """
    def __init__(self):
        self.carte = []
        self.objets = {}
        self.buildings = {}
        self.zid = -1
        self.pnjs = []
        self.path_ = ""

    def load(self, path_: str):
        if os.path.exists(path_):
            with open(path_, "rb") as map_reader:
                self.path_ = path_
                self.carte, self.objets, self.buildings, self.zid = \
                    pickle.Unpickler(map_reader).load()
        else:
            raise CarteInexistante(path_)

    def save(self):
        with open(self.path_, "wb") as map_saver:
            pickle.Pickler(map_saver).dump([self.carte, self.objets, self.buildings, self.zid])

    def create_pnj(self):
        self.pnjs.append(-1)
        raise FonctionnaliteNonImplementee

    def add_building(self, x: int, y: int, id_: int):
        self.buildings[x, y] = id_

    def get_all(self):
        return self.carte

    def get_at(self, x: int, y: int):
        return self.carte[y][x]

    def get_objects(self):
        return self.objets

    def building_at(self, x: int, y: int):
        return True if (x, y) in self.buildings.keys() else False

    def get_building_id_at(self, x: int, y: int):
        if self.building_at(x, y):
            return self.buildings[x, y]
        return BUILDING_GET_ERROR

    def get_zid(self):
        return self.zid

    def size(self):
        return len(self.carte[0]), len(self.carte)

    def get_object_at(self, x: int, y: int):
        if (x, y) in self.objets.keys():
            work = self.objets[x, y]
            del self.objets[x, y]
            return work
        return OBJET_GET_ERROR

    def set_all(self, new: list):
        self.carte = new

    def set_at(self, x: int, y: int, new):
        self.carte[y][x] = new

    def collide_at(self, x: int, y: int):
        if 0 <= int(y) < len(self.carte) and 0 <= int(x) < len(self.carte[0]):
            return True if COLLIDE_ITEM(self.carte[int(y)][int(x)][0]) else False
        return True

    def trigger_at(self, x: int, y: int):
        return True if len(self.carte[y][x]) == 6 else False

    def call_trigger_at(self, x: int, y: int, triggers_mgr: TriggersManager):
        if self.trigger_at(x, y):
            triggers_mgr.call_trigger_with_id(self.carte[y][x][TRIGGER])
            return True
        return False

    def has_object(self, x: int, y: int):
        return True if (x, y) in self.objets.keys() else False

    def drop_object_at(self, x: int, y: int, obj, from_poche):
        if (x, y) not in self.objets:
            self.objets[x, y] = [obj, from_poche]
        else:
            self.drop_object_at(x, y - 1, obj, from_poche)


class CartesManager:
    def __init__(self, ecran: pygame.Surface, renderer_manager):
        self.ecran = ecran
        self.rd_mgr = renderer_manager
        self.map_path = os.path.join("..", "saves", "map", "map" + EXTENSION)
        self.maps = {}
        self.fov = [0, FIRST_BASIC_FOV, 0, FIRST_BASIC_FOV2]
        self.offsets = [0, 0]
        self.images = {}
        self.lassets = []
        self.triggers_mgr = TriggersManager()
        self.current_carte = SubCarte()
        self.carte = []
        self.callback_end_rendering = []
        self.loaded = False
        self.water_animator = None

    def _load_animators(self):
        self.water_animator = FluidesAnimator(self.images[TILE_EAU], ANIM_SPEED_EAU)
        self.water_animator.load()

    def general_load(self):
        for i in glob(os.path.join("..", "assets", "tiles", "*")):
            # chargement automatique des tiles, leur nom déterminent si elles sont bloquantes ou non
            # chargement d'une tile simple
            if os.path.isfile(i):
                self.images[os.path.split(i)[1][:-4]] = pygame.image.load(i).convert_alpha()
                self.lassets.append(os.path.split(i)[1][:-4])
            # chargement d'une animation
            elif os.path.isdir(i):
                self.images[i.split(os.sep)[-1]] = BaseMultipleSpritesAnimator(i, wait=ANIM_DEFAULT_SPEED_MSPA)
                self.lassets.append(i.split(os.sep)[-1])
        self._load_animators()
        self.loaded = True

    def load(self):
        if not self.loaded:
            self.general_load()
        if os.path.exists(self.map_path):
            with open(self.map_path, "rb") as map_reader:
                self.maps = pickle.Unpickler(map_reader).load()
            self.current_carte.load(os.path.join(*self.maps[MAP_ENTRY_POINT]))
            self.carte = self.current_carte.get_all()
            self.adjust_offset()
        else:
            raise CarteInexistante(self.map_path)

    def adjust_offset(self):
        x = (FEN_large - len(self.carte[0]) * TILE_SIZE) // 2 if FEN_large > len(self.carte[0]) * TILE_SIZE else 0
        y = (FEN_haut - len(self.carte) * TILE_SIZE) // 2 if FEN_haut > len(self.carte) * TILE_SIZE else 0
        self.offsets = [x, y]

    def save(self):
        self.triggers_mgr.save()

    def collide_at(self, x, y):
        if self.current_carte.get_building_id_at(x, y) == BUILDING_GET_ERROR:
            return self.current_carte.collide_at(x, y)
        self.change_map(os.path.join("..", "saves", "maps", "map" + self.current_carte.get_building_id_at(x, y) + EXTENSION))
        return False

    def change_map(self, new_path: str):
        self.current_carte.save()
        self.current_carte = SubCarte()
        self.current_carte.load(new_path)
        self.carte = self.current_carte.get_all()
        self.adjust_offset()

    def drop_object_at(self, x: int, y: int, obj, from_poche):
        self.current_carte.drop_object_at(int(x) // TILE_SIZE, int(y) // TILE_SIZE, obj, from_poche)

    def update(self):
        self.render()

    def _draw_tile_at(self, at_x: int, at_y: int, tile: str):
        if tile == TILE_EAU:
            self.ecran.blit(self.water_animator.get_anim(), (at_x, at_y))
            if tile not in self.callback_end_rendering:
                self.callback_end_rendering.append(tile)
        else:
            if isinstance(self.images[tile], pygame.Surface):
                self.ecran.blit(self.images[tile], (at_x, at_y))
            elif isinstance(self.images[tile], BaseMultipleSpritesAnimator):
                self.ecran.blit(self.images[tile].get_anim(), (at_x, at_y))
                if tile not in self.callback_end_rendering:
                    self.callback_end_rendering.append(tile)

    def _update_anims(self):
        for anim in self.callback_end_rendering:
            if anim == TILE_EAU:
                self.water_animator.next()
            else:
                self.images[anim].next()
        self.callback_end_rendering = []

    def render(self):
        tmp_map = [ligne[int(self.fov[0]):int(self.fov[1])] for ligne in self.carte[int(self.fov[2]):int(self.fov[3])]]
        objects_at = self.current_carte.get_objects()
        if self.current_carte.size()[0] < FEN_large // TILE_SIZE and self.current_carte.size()[1] < FEN_haut // TILE_SIZE:
            pygame.draw.rect(self.ecran, (0, 0, 0), (0, 0) + self.ecran.get_size())
        for y in range(len(tmp_map)):
            for x in range(len(tmp_map[y])):
                objet = self.carte[y][x]
                xpos, ypos = x * TILE_SIZE + self.offsets[0], y * TILE_SIZE + self.offsets[1]
                if not isinstance(objet, list):
                    raise ErreurContenuCarte
                else:
                    if len(objet) <= 5:
                        for tile in udel_same_occurence(*objet[::-1]):
                            self._draw_tile_at(xpos, ypos, tile)
                    else:
                        for tile in udel_same_occurence(*objet[-2::-1]):
                            self._draw_tile_at(xpos, ypos, tile)
                if (x, y) in objects_at:
                    self.ecran.blit(self.images[TILE_POKEOBJ], (xpos, ypos))
        self._update_anims()

    def get_tile_code_at(self, x: int, y: int):
        return self.carte[y][x] if 0 <= x < len(self.carte[0]) and 0 <= y < len(self.carte) else TILE_GET_ERROR

    def get_of1(self):
        return self.offsets[0]

    def get_of2(self):
        return self.offsets[1]

    def get_ofs(self):
        return self.offsets

    def get_fov(self):
        return self.fov

    def get_fov_carte(self):
        return [ligne[int(self.fov[0]):int(self.fov[1])] for ligne in self.current_carte[int(self.fov[2]):int(self.fov[3])]]

    def get_carte(self):
        return self.current_carte.get_all()

    def get_zid(self):
        return self.current_carte.get_zid()

    def get_object_at(self, x: int, y: int):
        if self.current_carte.has_object(x, y):
            object_ = self.current_carte.get_object_at(x, y)
            return object_ if object_ != OBJET_GET_ERROR else None
        return None

    def move_of1(self, dir_: int=1):
        self.offsets[0] += dir_
        if not self.offsets[0] % TILE_SIZE:
            if self.fov[0] - dir_ >= 0:
                self.offsets[0] %= TILE_SIZE
                self.fov[0] -= dir_

    def move_of2(self, dir_: int=1):
        self.offsets[1] += dir_
        if not self.offsets[1] % TILE_SIZE:
            if self.fov[2] - dir_ >= 0:
                self.offsets[1] %= TILE_SIZE
                self.fov[2] -= dir_

    def has_trigger(self, x: int=0, y: int=0):
        return self.current_carte.trigger_at(x, y)

    def call_trigger_at(self, x: int, y: int):
        if not self.current_carte.call_trigger_at(x, y, self.triggers_mgr):
            if self.carte[y][x][0] in TILES_RDM_CREATURES and randint(*LUCK_RDM_CREA):
                # combat !
                self.rd_mgr.change_renderer_for(RENDER_COMBAT)


class CarteRenderer:
    def __init__(self, ecran: pygame.Surface, carte_mgr: CartesManager):
        self.ecran = ecran
        self.carte_mgr = carte_mgr
        self.carte_img = os.path.join("..", "assets", "gui", "carte.png")

    def update(self):
        self.render()

    def render(self):
        pygame.draw.rect(self.ecran, (20, 180, 20), (MAP_RDR_POSX, MAP_RDR_POSY, MAP_RDR_SX, MAP_RDR_SY))
        self.ecran.blit(self.carte_mgr, (MAP_RDR_CARTEX, MAP_RDR_CARTEX))