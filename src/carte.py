# coding=utf-8

import pickle, _pickle
from urllib import request
from glob import glob
from constantes import *
from trigger_manager import TriggersManager
from exceptions import ErreurContenuCarte
from utils import udel_same_occurence
from pnj_manager import PNJ, CROSS_MOVE, HORIZONTAL_MOVE, STANDART_MOVE, VERTICAL_MOVE
from animator import FluidesAnimator, BaseMultipleSpritesAnimator
from random import randint
from urllib import error
import socket
import debug
import light as light_module


def maps_retriver(site: str):
    files = []
    try:
        tmp = request.urlopen(site + "/provider/list").read().decode()
        data = str(tmp).replace('false', 'False').replace('true', 'True').replace('null', 'None')
        debug.println("Récupération de la liste des mondes ({}) ...".format(site + '/provider/list'))
        files = eval(data)
        debug.println("Contenu du fichier : {}".format(files))
    except (socket.gaierror, error.URLError):
        debug.println("Pas de connexion internet || Le fichier / site n'exsite pas")
    except PermissionError:
        debug.println("Le jeu n'a pas les droits suffisants pour télécharger la liste de maps")
    finally:
        yield 1

    if files:
        for world in files:
            directory = os.path.join("..", "assets", "map", "world{}".format(world['wid']))

            if not os.path.exists(directory):
                # création du dossier du monde s'il n'exise pas !
                os.mkdir(directory)

            tmp = request.urlopen(site + "/provider/world/{}".format(world['wid'])).read().decode()
            data = str(tmp).replace('false', 'False').replace('true', 'True').replace('null', 'None')
            maps = eval(data)

            with open(os.path.join(directory, 'config.txt'), 'w') as file:
                file.write(str(
                    {
                        "name": maps['name']
                    }
                ))

            for id_, carte in maps['maps'].items():
                dl_path = os.path.join(directory, "map{}{}".format(id_, EXTENSION))
                try:
                    with open(dl_path, "w") as file:
                        file.write(str(carte))
                except PermissionError:
                    debug.println("Le jeu n'a pas les droits suffisants pour télécharger les maps")
                except OSError:
                    debug.println("Le chemin d'enregistrement des cartes n'est pas correct ({})".format(dl_path))
    yield 1


def parse_monoline_layer(layer: list, size: tuple) -> list:
    carte = []
    sx, sy = size

    if isinstance(layer, list):
        for y in range(sy):
            line = []
            for x in range(sx):
                if layer:
                    tile = str(layer[x + y * sx])
                else:
                    tile = "9990"
                line.append(tile)
            carte.append(line)
    elif isinstance(layer, dict):
        # on fait une map vide avant !
        for x in range(sx):
            line = []
            for y in range(sy):
                line.append("9990")
            carte.append(line)

        for pos, tile in layer.items():
            real_x, real_y = int(pos) % sx, int(pos) // sx
            carte[real_y][real_x] = str(tile)

    return carte


def parse_layers_to_map(*layers) -> list:
    carte = []

    for y in range(len(layers[0])):
        line = []
        for x in range(len(layers[0][y])):
            case = []
            for layer in layers:
                case.append(layer[y][x])
            line.append(case)
        carte.append(line)

    return carte


def parse_pnjs_dict(pnjs: dict) -> list:
    work = []

    for id_, pnj_details in pnjs.items():
        if pnj_details["type_mvt"] == "0":
            type_mvt = STANDART_MOVE
        elif pnj_details["type_mvt"] == "1":
            type_mvt = CROSS_MOVE
        elif pnj_details["type_mvt"] == "2":
            type_mvt = VERTICAL_MOVE
        else:  # if pnj_details["type_mvt"] == "3":
            type_mvt = HORIZONTAL_MOVE

        work.append(
            PNJ(
                (pnj_details["pos"]["i"], pnj_details["pos"]["j"]),
                type_mvt,
                pnj_details["text"],
                pnj_details["dir"],
                  # pnj_details["image"]
            )
        )

    return work


def parse_lights_dict(lights: dict) -> list:
    work = []

    for id_, light_details in lights.items():
        work.append(
            light_module.PreRenderedLight(
                id_,
                (light_details["pos"]["i"] * TILE_SIZE, light_details["pos"]["j"] * TILE_SIZE),
                light_details["size"],
                (light_details["color"]["r"], light_details["color"]["g"], light_details["color"]["b"]),
                variation=light_details["variation"],
                threshold=light_details["threshold"]
            )
        )

    return work


def load_map_from_id(id_: int, wid: int):
    try:
        # pickled version
        carte = pickle.Unpickler(
            open(os.path.join("..", "assets", "map", "world{}".format(wid), "map" + str(id_) + EXTENSION), 'rb')).load()
    except _pickle.UnpicklingError:
        # json version
        with open(os.path.join("..", "assets", "map", "world{}".format(wid), "map" + str(id_) + EXTENSION), "r") as file:
            content = file.read()
        content = eval(content)

        try:
            _object = content['objects'] if content['objects'] else {}
        except KeyError:
            _object = {}

        try:
            _zid = content['zid']
        except KeyError:
            _zid = 0

        try:
            _pnjs = parse_pnjs_dict(content['pnjs'])
        except KeyError:
            _pnjs = []

        try:
            _maplinks = content["maplinks"] if content['maplinks'] else {}
        except KeyError:
            _maplinks = {}

        try:
            _triggers = content['triggers'] if content['triggers'] else {}
        except KeyError:
            _triggers = {}

        try:
            _id = content['id']
        except KeyError:
            _id = MAP_DEFAULT

        try:
            _lights = parse_lights_dict(content['lights'])
        except KeyError:
            _lights = []

        try:
            _name = content['name']
        except KeyError:
            _name = "DEFAULT MAP NAME"

        carte = SubCarte(
            parse_layers_to_map(
                parse_monoline_layer(content['layer3'], (int(content['width']), int(content['height']))),
                parse_monoline_layer(content['layer2'], (int(content['width']), int(content['height']))),
                parse_monoline_layer(content['layer1'], (int(content['width']), int(content['height'])))
            ),
            _object,
            _maplinks,
            _zid,
            _pnjs,
            _triggers,
            _id,
            _name,
            _lights
        )

    return carte


class SubCarte:
    """
    chaque carte crée ses propres PNJ et s'occupe de les afficher
    chaque carte s'occupe aussi de gérer ses objets (au sol), et les chemins vers d'autres cartes
    elles gérent aussi leur ZID
    """
    def __init__(self, carte: list, objets: dict, maplinks: dict, zid: int, pnjs: list,
                 triggers: dict, id_: int, name: str, lights: list=None):
        self.carte = carte
        self.objets = objets
        self.maplinks = maplinks
        self.zid = zid
        self.pnjs = pnjs
        self.triggers = triggers
        self.id = id_
        self.lights = lights
        self.name = name

    def create_pnj(self, pnj: PNJ):
        self.pnjs.append(pnj)

    def get_all(self):
        return self.carte

    def get_name(self):
        return self.name

    def get_at(self, x: int, y: int):
        return self.carte[y][x]

    def get_objects(self):
        return self.objets

    def get_lights(self):
        return self.lights

    def get_pnjs(self):
        return self.pnjs

    def spawn_at(self, x: int, y: int):
        for _, content in self.maplinks.items():
            if int(content["i"]) == x and int(content["j"]) == y and int(content["type"]) == 0:
                return True
        return False

    def building_at(self, x: int, y: int):
        for _, content in self.maplinks.items():
            if int(content["i"]) == x and int(content["j"]) == y and int(content["type"]) == 1:
                return True
        return False

    def get_spawn_pos_with_tag(self, tag: str):
        for _, content in self.maplinks.items():
            if int(content["type"]) == 0 and content["spawn_tag"] == tag:
                return content["i"], content["j"]
        return None

    def get_building_id_tag_at(self, x: int, y: int):
        if self.building_at(x, y):
            for _, content in self.maplinks.items():
                if int(content["i"]) == x and int(content["j"]) == y and int(content["type"]) == 1:
                    return content["destination"]["map_id"], content["destination"]["spawn_tag"]
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
            return True if COLLIDE_ITEM(self.carte[int(y)][int(x)][1]) else False
        return True

    def trigger_at(self, x: int, y: int):
        return (x, y) in self.triggers.keys()

    def call_trigger_at(self, x: int, y: int, triggers_mgr: TriggersManager):
        if self.trigger_at(x, y):
            triggers_mgr.call_trigger_with_id(self.triggers[x, y], self.id)
            return True
        return False

    def has_object(self, x: int, y: int):
        return True if (x, y) in self.objets.keys() else False

    def drop_object_at(self, x: int, y: int, obj, from_poche):
        if (x, y) not in self.objets:
            self.objets[x, y] = [obj, from_poche]
        else:
            self.drop_object_at(x, y - 1, obj, from_poche)

    def get_tiles_composing(self) -> list:
        work = []
        for line in self.carte:
            for layer in line:
                for case in layer:
                    if case not in work:
                        work.append(case)
        return work


class CartesManager:
    def __init__(self, ecran, renderer_manager, police):
        self.ecran = ecran
        self.rd_mgr = renderer_manager
        self.police = police
        self.map_path = os.path.join("..", "saves", "map" + EXTENSION)
        self.world_path = os.path.join("..", "saves", "world" + EXTENSION)
        self._fd_nom_map = rendering_engine.load_image(os.path.join("..", "assets", "gui", "fd_nom_map.png"))
        self.map = MAP_DEFAULT
        self.world = WORLD_DEFAULT  # default
        self.offsets = [0, 0]
        self.images = {}
        self.lassets = []
        self.triggers_mgr = TriggersManager()
        self.current_carte = None
        self.carte = []
        self.callback_end_rendering = []
        self.loaded = False
        self.has_changed_map = False
        self.time_changed_map = 0
        self.perso = None
        self.water_animator = None
        self.specials_blocs = None
        self.lights = []

    def add_perso(self, new):
        if not self.perso:
            self.perso = new

    def _load_animators(self):
        self.water_animator = FluidesAnimator(self.images[TILE_EAU], ANIM_SPEED_EAU)
        self.water_animator.load()

    def _load_lights(self):
        self.lights = self.current_carte.get_lights()
        for _light in self.lights:
            _light.load()

    def general_load(self):
        for i in glob(os.path.join("..", "assets", "tiles", "*")):
            # chargement automatique des tiles, leur nom déterminent si elles sont bloquantes ou non
            # chargement d'une tile simple
            if os.path.isfile(i):
                self.images[os.path.split(i)[1][:-4]] = rendering_engine.load_image(i)
                self.lassets.append(os.path.split(i)[1][:-4])
            # chargement d'une animation
            elif os.path.isdir(i):
                self.images[i.split(os.sep)[-1]] = BaseMultipleSpritesAnimator(i)
                self.lassets.append(i.split(os.sep)[-1])
        self._load_animators()

        with open(os.path.join("..", "assets", "configuration", "tiles.umd"), "r") as file:
            self.specials_blocs = eval(file.read())

        self.loaded = True

    def load(self):
        if not self.loaded:
            self.general_load()

        if os.path.exists(self.map_path):
            with open(self.map_path, "rb") as map_reader:
                self.map = pickle.Unpickler(map_reader).load()

        if os.path.exists(self.world_path):
            with open(self.world_path, "rb") as world_reader:
                self.world = pickle.Unpickler(world_reader).load()

        self.current_carte = load_map_from_id(self.map, self.world)
        self.carte = self.current_carte.get_all()
        self.adjust_offset()

        self._load_lights()

    def adjust_offset(self):
        x = (FEN_large - len(self.carte[0]) * TILE_SIZE) // 2 if FEN_large >= len(self.carte[0]) * TILE_SIZE else 0
        y = (FEN_haut - len(self.carte) * TILE_SIZE) // 2 if FEN_haut >= len(self.carte) * TILE_SIZE else 0
        self.offsets = [x, y]

    def save(self):
        with open(self.map_path, "wb") as file:
            pickle.Pickler(file).dump(self.current_carte.id)
        with open(self.world_path, "wb") as file:
            pickle.Pickler(file).dump(self.world)
        self.triggers_mgr.save()

    def collide_at(self, x, y):
        if self.current_carte.get_building_id_tag_at(x, y) == BUILDING_GET_ERROR:
            return self.current_carte.collide_at(x, y)
        return True

    def check_changing_map(self, x, y):
        if self.current_carte.get_building_id_tag_at(x, y) != BUILDING_GET_ERROR:
            self.change_map(*self.current_carte.get_building_id_tag_at(x, y))

    def change_map(self, new_id: int, tag: str):
        self.has_changed_map = True
        self.time_changed_map = 0
        depuis = self.current_carte.id
        pickle.Pickler(open(os.path.join("..", "assets", "map", "world{}".format(self.world), "map" + str(depuis) + EXTENSION), "wb")).dump(self.current_carte)

        self.current_carte = load_map_from_id(new_id, self.world)
        self.carte = self.current_carte.get_all()
        tmp = self.current_carte.get_spawn_pos_with_tag(tag)

        if not tmp:
            raise ReferenceError("Il manque un point d'entrée sur la map {} pour la map d'id {}".format(new_id, depuis))
        spawn_tiles_pos = [p * TILE_SIZE for p in tmp]

        if FEN_large > len(self.carte[0]) * TILE_SIZE and FEN_haut > len(self.carte) * TILE_SIZE:
            self.adjust_offset()
        elif FEN_large > len(self.carte[0] * TILE_SIZE) and FEN_haut <= len(self.carte) * TILE_SIZE:
            if spawn_tiles_pos[1] < (self.current_carte.size()[1] * TILE_SIZE) // 2:
                origin_view = spawn_tiles_pos[0] - FEN_large // 2, (self.current_carte.size()[1] - FEN_haut) // 2
            else:
                origin_view = spawn_tiles_pos[0] - FEN_large // 2, (FEN_haut - self.current_carte.size()[1]) // 2
            self.offsets = [
                -origin_view[0],
                -origin_view[1]
            ]
        elif FEN_large <= len(self.carte[0] * TILE_SIZE) and FEN_haut > len(self.carte) * TILE_SIZE:
            if spawn_tiles_pos[0] < (self.current_carte.size()[0] * TILE_SIZE) // 2:
                origin_view = (self.current_carte.size()[0] - FEN_large) // 2, spawn_tiles_pos[1] - FEN_haut // 2
            else:
                origin_view = (FEN_large - self.current_carte.size()[0]) // 2, spawn_tiles_pos[1] - FEN_haut // 2
            self.offsets = [
                -origin_view[0],
                -origin_view[1]
            ]
        else:
            origin_view = spawn_tiles_pos[0] - FEN_large // 2, spawn_tiles_pos[1] - FEN_haut // 2
            self.offsets = [
                -origin_view[0],
                -origin_view[1]
            ]
        self.perso.pos = tmp[0] * TILE_SIZE + self.offsets[0], tmp[1] * TILE_SIZE + self.offsets[1]

    def drop_object_at(self, x: int, y: int, obj, from_poche):
        self.current_carte.drop_object_at(int(x) // TILE_SIZE, int(y) // TILE_SIZE, obj, from_poche)

    def update(self, dt: float=1.0):
        self.render(dt)
        self._update_anims()

    def _draw_tile_at(self, at_x: int, at_y: int, tile: str):
        if tile == TILE_EAU:
            self.ecran.blit(self.water_animator.get_anim(), (at_x, at_y))
            if tile not in self.callback_end_rendering:
                self.callback_end_rendering.append(tile)
        else:
            if isinstance(self.images[tile], rendering_engine.get_surface_class()):
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

    def draw_top_layer(self):
        for y in range(len(self.carte)):
            for x in range(len(self.carte[y])):
                tile = self.carte[y][x][0]
                xpos, ypos = x * TILE_SIZE + self.offsets[0], y * TILE_SIZE + self.offsets[1]

                if xpos < -TILE_SIZE or xpos > FEN_large or ypos < -TILE_SIZE or ypos > FEN_haut or tile == '9990':
                    # optimisation
                    continue

                self._draw_tile_at(xpos, ypos, tile)

        for _light in self.current_carte.get_lights():
            _light.blit(self.ecran, self)

        # doit toujours être dessiné en dernier !
        if self.has_changed_map:
            self.time_changed_map += 1
            self.ecran.blit(self._fd_nom_map, (MAP_FD_NAME_MAP_X, MAP_FD_NAME_MAP_Y))
            self.ecran.blit(self.police.render(self.current_carte.get_name(), POL_ANTIALISING, (10, 10, 10)),
                            (MAP_FD_NAME_MAP_X + 10, MAP_FD_NAME_MAP_Y + (self._fd_nom_map.get_height() - 20) // 2))
            if self.time_changed_map >= MAX_TIME_CHANGED_MAP:
                self.time_changed_map = 0
                self.has_changed_map = False

    def render(self, dt: float=1.0):
        objects_at = self.current_carte.get_objects()
        rendering_engine.draw_rect(self.ecran, (0, 0, FEN_large, FEN_haut), (0, 0, 0))

        for y in range(len(self.carte)):
            for x in range(len(self.carte[y])):
                objet = self.carte[y][x]
                xpos, ypos = x * TILE_SIZE + self.offsets[0], y * TILE_SIZE + self.offsets[1]

                if xpos < -TILE_SIZE or xpos > FEN_large or ypos < -TILE_SIZE or ypos > FEN_haut:
                    # optimisation
                    continue

                if not isinstance(objet, list):
                    raise ErreurContenuCarte
                else:
                    for tile in udel_same_occurence(*objet[::-1]):
                        if tile != "9990":
                            self._draw_tile_at(xpos, ypos, tile)

                if DEBUG_LEVEL >= 1:
                    if self.current_carte.building_at(x, y):
                        rendering_engine.draw_rect(self.ecran, (xpos, ypos, TILE_SIZE, TILE_SIZE), (255, 0, 0))
                    if self.current_carte.spawn_at(x, y):
                        rendering_engine.draw_rect(self.ecran, (xpos, ypos, TILE_SIZE, TILE_SIZE), (0, 0, 255))

                # objets
                if (x, y) in objects_at:
                    self.ecran.blit(self.images[TILE_POKEOBJ], (xpos, ypos))

        for _pnj in self.current_carte.get_pnjs():
            _pnj.update(self.ecran, self, dt)

    def get_tile_code_at(self, x: int, y: int, layer: int=1):
        return self.carte[int(y)][int(x)][layer] if 0 <= x < len(self.carte[0]) and 0 <= y < len(self.carte) else TILE_GET_ERROR

    def get_of1(self):
        return int(self.offsets[0])

    def get_of2(self):
        return int(self.offsets[1])

    def get_ofs(self):
        return [int(i) for i in self.offsets]

    def get_carte(self):
        return self.current_carte.get_all()

    def get_zid(self):
        return self.current_carte.get_zid()

    def get_object_at(self, x: int, y: int):
        if self.current_carte.has_object(x, y):
            object_ = self.current_carte.get_object_at(x, y)
            return object_ if object_ != OBJET_GET_ERROR else None
        return None

    def get_pnjs(self):
        return self.current_carte.get_pnjs()

    def move_of1(self, dir_: int):
        self.offsets[0] += dir_

    def move_of2(self, dir_: int):
        self.offsets[1] += dir_

    def has_trigger(self, x: int=0, y: int=0):
        return self.current_carte.trigger_at(x, y)

    def call_trigger_at(self, x: int, y: int):
        if not self.current_carte.call_trigger_at(x, y, self.triggers_mgr):
            if self.carte[y][x][2] in TILES_RDM_CREATURES and randint(*LUCK_RDM_CREA) >= LUCK_CREA_APPEAR:
                # combat !
                self.rd_mgr.change_renderer_for(RENDER_COMBAT)


class CarteRenderer:
    def __init__(self, ecran, carte_mgr: CartesManager):
        self.ecran = ecran
        self.carte_mgr = carte_mgr
        self.carte_img = rendering_engine.load_image(os.path.join("..", "assets", "aventure", "worldmap.png"))
        self.carte_mgr = rendering_engine.rescale(self.carte_img, (MAP_RDR_SX, MAP_RDR_SY))

    def update(self):
        self.render()

    def render(self):
        self.ecran.blit(self.carte_mgr, (MAP_RDR_POSX, MAP_RDR_POSY))