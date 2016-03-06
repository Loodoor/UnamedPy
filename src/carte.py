# coding=utf-8

import pickle
from glob import glob
from constantes import *
from trigger_manager import TriggersManager
from exceptions import CarteInexistante, ErreurContenuCarte
from utils import udel_same_occurence
from pnj_manager import PNJ
from animator import FluidesAnimator, BaseMultipleSpritesAnimator
from random import randint
import debug


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
        self.spawns = {}
        self.path_ = ""

    def load(self, path_: str):
        if os.path.exists(path_):
            with open(path_, "rb") as map_reader:
                self.path_ = path_
                load = pickle.Unpickler(map_reader).load()
                try:
                    self.carte, self.objets, self.buildings, self.zid, self.pnjs, self.spawns = load
                except ValueError:
                    self.carte, self.objets, self.buildings, self.zid, self.pnjs = load
                    debug.println("[!] Impossible de charger les spawn pour cette map")
                del load
        else:
            raise CarteInexistante(path_)

    def save(self):
        with open(self.path_, "wb") as map_saver:
            pickle.Pickler(map_saver).dump([self.carte, self.objets, self.buildings, self.zid, self.pnjs, self.spawns])

    def create_pnj(self, pnj: PNJ):
        self.pnjs.append(pnj)

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

    def get_spawn_pos_with_id(self, id_: int):
        for pos, map_id in self.spawns.items():
            if map_id == id_:
                return pos
        return None

    def get_building_id_at(self, x: int, y: int):
        if self.building_at(x, y):
            return str(self.buildings[x, y])
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
            triggers_mgr.call_trigger_with_id(self.carte[y][x][TRIGGER], self.path_)
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
        self.map_path = os.path.join("..", "assets", "map", "map" + EXTENSION)
        self.maps = {}
        self.offsets = [0, 0]
        self.images = {}
        self.lassets = []
        self.triggers_mgr = TriggersManager()
        self.current_carte = SubCarte()
        self.carte = []
        self.callback_end_rendering = []
        self.loaded = False
        self.perso = None
        self.water_animator = None

    def add_perso(self, new):
        if not self.perso:
            self.perso = new

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
                self.images[i.split(os.sep)[-1]] = BaseMultipleSpritesAnimator(i)
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
        x = (FEN_large - len(self.carte[0]) * TILE_SIZE) // 2 if FEN_large >= len(self.carte[0]) * TILE_SIZE else 0
        y = (FEN_haut - len(self.carte) * TILE_SIZE) // 2 if FEN_haut >= len(self.carte) * TILE_SIZE else 0
        self.offsets = [x, y]

    def save(self):
        self.triggers_mgr.save()

    def collide_at(self, x, y):
        if self.current_carte.get_building_id_at(x, y) == BUILDING_GET_ERROR:
            return self.current_carte.collide_at(x, y)
        return True

    def check_changing_map(self, x, y):
        if self.current_carte.get_building_id_at(x, y) != BUILDING_GET_ERROR:
            self.change_map(os.path.join("..", "assets", "map", "map" + self.current_carte.get_building_id_at(x, y) + EXTENSION))

    def change_map(self, new_path: str):
        depuis = os.path.split(self.current_carte.path_)[1].split('.')[0][3:]
        self.current_carte.save()
        self.current_carte = SubCarte()
        self.current_carte.load(new_path)
        self.carte = self.current_carte.get_all()
        tmp = self.current_carte.get_spawn_pos_with_id(depuis)
        if FEN_large > len(self.carte[0]) * TILE_SIZE and FEN_haut > len(self.carte) * TILE_SIZE:
            self.adjust_offset()
            if not tmp:
                raise ReferenceError("Il manque un point d'entrée sur la map {}".format(new_path))
            self.perso.pos = tmp[0] * TILE_SIZE + self.offsets[0], tmp[1] * TILE_SIZE + self.offsets[1]
        else:
            spawn_tiles_pos = [p * TILE_SIZE for p in tmp]
            origin_view = spawn_tiles_pos[0] - FEN_large // 2, spawn_tiles_pos[1] - FEN_haut // 2
            self.offsets = [
                -origin_view[0],
                -origin_view[1]
            ]
            self.perso.pos = tmp[0] * TILE_SIZE - origin_view[0], tmp[1] * TILE_SIZE - origin_view[1]

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
        pygame.draw.rect(self.ecran, (0, 0, 0), (0, 0) + self.ecran.get_size())
        objects_at = self.current_carte.get_objects()
        if self.current_carte.size()[0] < FEN_large // TILE_SIZE and self.current_carte.size()[1] < FEN_haut // TILE_SIZE:
            pygame.draw.rect(self.ecran, (0, 0, 0), (0, 0) + self.ecran.get_size())
        for y in range(len(self.carte)):
            for x in range(len(self.carte[y])):
                objet = self.carte[y][x]
                xpos, ypos = x * TILE_SIZE + self.offsets[0], y * TILE_SIZE + self.offsets[1]
                if xpos < -TILE_SIZE or xpos > FEN_large or ypos < -TILE_SIZE or ypos > FEN_haut:
                    continue
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

    def get_carte(self):
        return self.current_carte.get_all()

    def get_zid(self):
        return self.current_carte.get_zid()

    def get_object_at(self, x: int, y: int):
        if self.current_carte.has_object(x, y):
            object_ = self.current_carte.get_object_at(x, y)
            return object_ if object_ != OBJET_GET_ERROR else None
        return None

    def move_of1(self, dir_: int):
        self.offsets[0] += dir_

    def move_of2(self, dir_: int):
        self.offsets[1] += dir_

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