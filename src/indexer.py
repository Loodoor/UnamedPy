# coding=utf-8

import pickle
from exceptions import CreaturesNonTrouvees
from constantes import *
import textwrap as tw


class Element:
    def __init__(self, name: str, id_: int, type_: int, stade: int, path: str, desc: str, evolve_id: int, evolve_niv: int):
        self.name = name
        self.id = id_
        self.type = type_
        self.path = path
        self.description = desc
        self.stade = stade
        self.vu = False
        self.capture = False
        self.evolve_id = evolve_id
        self.evolve_niv = evolve_niv

    def vu_(self):
        self.vu = True

    def capture_(self):
        self.capture = True

    def get_stade(self):
        return self.stade

    def get_type(self):
        return self.type


class Typeur:
    def __init__(self):
        self.types = {
            T_TENEBRE: {
                'default': "ténèbre",
                'user': '',
                'saw': 0
            },
            T_LUMIERE: {
                'default': "lumière",
                'user': '',
                'saw': 0
            },
            T_FEU: {
                'default': "feu",
                'user': '',
                'saw': 0
            },
            T_NORMAL: {
                'default': "normal",
                'user': '',
                'saw': 0
            },
            T_AIR: {
                'default': "air",
                'user': '',
                'saw': 0
            },
            T_EAU: {
                'default': "eau",
                'user': '',
                'saw': 0
            },
            T_ELEC: {
                'default': "électrique",
                'user': '',
                'saw': 0
            },
            T_PLANTE: {
                'default': "plante",
                'user': '',
                'saw': 0
            },
            T_POISON: {
                'default': "poison",
                'user': '',
                'saw': 0
            },
            T_TERRE: {
                'default': "terre",
                'user': '',
                'saw': 0
            }
        }
        self.path = os.path.join("..", "saves", "types" + EXTENSION)

        self.user_types = {}

    def __create_user_type(self):
        self.user_types = {}
        for k, v in self.types.items():
            self.user_types[k] = v['user']

    def change_name(self, type_: int, new_name: str):
        if type_ in self.types.keys() and not self.types[type_]['user']:
            self.types[type_]['user'] = new_name
        self.__create_user_type()

    def get_name(self, type_: int):
        return self.types[type_]['user']

    def get_default_name(self, type_: int):
        return self.types[type_]['default']

    def get_types(self):
        return self.user_types

    def get_views_on(self, type_: int):
        return self.types[type_]['saw']

    def saw_type(self, type_: int):
        self.types[type_]['saw'] += 1

    @staticmethod
    def count_types():
        return TYPES_NUMBER

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "rb") as type_rb:
                self.types = pickle.Unpickler(type_rb).load()
        self.__create_user_type()

    def save(self):
        with open(self.path, "wb") as type_wb:
            pickle.Pickler(type_wb).dump(self.types)


class Indexer:
    def __init__(self, ecran, police, render_manager):
        self.ecran = ecran
        self.police = police
        self.save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        self.page = 0
        self.max_page = 10
        self.par_page = 10
        self.indexer = []
        self.images_crea = {}
        self.typeur = Typeur()
        self.render_creatures = True
        self.rd_mgr = render_manager
        self.selected_creature = -1
        self.selected_type = -1
        self._btn_types = ree.load_image(os.path.join("..", "assets", "gui", "fd_bouton_types_indexeur.png"))
        self._btn_creatures = ree.load_image(os.path.join("..", "assets", "gui", "fd_bouton_creatures_indexeur.png"))
        self.creas_selected = []
        self._attaque_table = None
        self.fond = ree.load_image(os.path.join("..", "assets", "gui", "fd_indexer.png"))

    @staticmethod
    def static_select_all_crea_with_stade(stade: int):
        save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        if os.path.exists(save_path):
            with open(save_path, "rb") as read_index:
                indexer = pickle.Unpickler(read_index).load()
        else:
            raise CreaturesNonTrouvees

        if 0 <= stade <= 3:
            work = []
            for creature in indexer:
                if creature.get_stade() == stade:
                    work.append(creature)
            return work
        return indexer

    @staticmethod
    def static_select_all_crea_with_type(type_: int):
        save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        if os.path.exists(save_path):
            with open(save_path, "rb") as read_index:
                indexer = pickle.Unpickler(read_index).load()
        else:
            raise CreaturesNonTrouvees

        work = []
        for creature in indexer:
            if creature.get_type() == type_:
                work.append(creature)
        return work

    @staticmethod
    def static_select_all_crea_with_type_and_stade(type_: int, stade: int):
        tmp = Indexer.static_select_all_crea_with_type(type_)
        work = []
        for creature in tmp:
            if creature.get_stade() == stade:
                work.append(creature)
        return work

    @staticmethod
    def add_new(name: str, id_: int, type_: int, stade: int, path: str, desc: str, evolve_id: int, evolve_niv: int):
        save_path = os.path.join("..", "saves", "indexer" + EXTENSION)
        if os.path.exists(save_path):
            with open(save_path, 'rb') as rbin:
                tod = pickle.Unpickler(rbin).load()
                tod.append(Element(name, id_, type_, stade, path, desc, evolve_id, evolve_niv))
                pickle.Pickler(open(save_path, 'wb')).dump(tod)
        else:
            with open(save_path, 'wb') as wbin:
                tod = [Element(name, id_, type_, stade, path, desc, evolve_id, evolve_niv)]
                pickle.Pickler(wbin).dump(tod)

    def get_attacks_table(self):
        return self._attaque_table

    def load(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, "rb") as read_index:
                self.indexer = pickle.Unpickler(read_index).load()
                for elem in self.indexer:
                    img = ree.load_image(elem.path)
                    self.images_crea[elem.id] = ree.rescale(img, (POK_SX_IMAGE_CREA, POK_SY_IMAGE_CREA))
                    yield 1
                self.creas_selected = self.indexer
                yield 1
        else:
            raise CreaturesNonTrouvees
        self.typeur.load()

    def save(self):
        with open(self.save_path, "wb") as save_index:
            pickle.Pickler(save_index).dump(self.indexer)
        self.typeur.save()

    def add_attacks_table(self, table: object):
        self._attaque_table = table

    def add_name_to_crea(self, id_: int, name: str):
        for creature in self.indexer:
            if creature.id == id_:
                creature.name = name.upper()
                break

    def get_image_by_id(self, id_: int):
        return self.images_crea[id_] if id_ in self.images_crea.keys() else ree.create_surface((150, 150))

    def next(self):
        self.page = self.page + 1 if self.page <= self.max_page else self.max_page

    def previous(self):
        self.page = self.page - 1 if self.page - 1 >= 0 else 0

    def get_type_of(self, id_: int):
        for creature in self.indexer:
            if creature.id == id_:
                return creature.type
        return POK_SEARCH_ERROR

    def get_evolve_by_id_level(self, id_: int, current_level: int) -> bool or int:
        for creature in self.indexer:
            if creature.id == id_:
                if creature.evolve_niv == current_level:
                    return creature.evolve_id if creature.evolve_id != -1 else False
                elif creature.evolve_niv == -1:
                    return False
        return False

    def get_typeur(self) -> Typeur:
        return self.typeur

    def get_captured(self, id_: int):
        for creature in self.indexer:
            if creature.id == id_:
                return creature.capture
        return False

    def get_viewed(self, id_: int):
        for creature in self.indexer:
            if creature.id == id_:
                return creature.vu
        return False

    def get_by_id(self, id_: int):
        for creature in self.indexer:
            if creature.id == id_:
                return creature
        return POK_SEARCH_ERROR

    def vu_(self, id_: int):
        for elem in self.indexer:
            if id_ == elem.id:
                elem.vu_()
                self.typeur.saw_type(elem.type)
                break

    def capturer(self, id_: int):
        for elem in self.indexer:
            if id_ == elem.id:
                elem.capture_()
                break

    def select_all_crea_with_stade(self, stade: int):
        if 0 <= stade <= 3:
            work = []
            for creature in self.indexer:
                if creature.get_stade() == stade:
                    work.append(creature)
            return work
        else:
            return self.indexer

    def update(self):
        self.render()

    def render_sel_stade(self):
        while True:
            ree.draw_rect(self.ecran, (POK_X_FENSST, POK_Y_FENSST, POK_SX_FENSST, POK_SY_FENSST), (0, 0, 0))
            selected = 0
            tmp = self.police.render("Stade à sélectionner : " + str(selected), POL_ANTIALISING, (255, 255, 255))

            ev = ree.poll_event()
            if ev == KEYDOWN and ev.unicode.isdigit():
                selected = int(ev.unicode)
            if ev == (KEYDOWN, K_RETURN):
                self.creas_selected = self.select_all_crea_with_stade(selected)
                break

            self.ecran.blit(tmp,
                            (POK_X_FENSST + (POK_SX_FENSST - tmp.get_width()) // 2,
                             POK_Y_FENSST + (POK_SY_FENSST - POK_ESP_Y_ITEM) // 2))

            ree.flip()

    def render(self):
        self.ecran.blit(self.fond, (POK_POSX, POK_POSY))
        titre = self.police.render(NOM_POKEDEX if self.render_creatures else NOM_POKEDEX + " -> Types", POL_ANTIALISING, (255, 255, 255))
        self.ecran.blit(titre, (POK_X_TITRE, POK_Y_TITRE))
        if not self.render_creatures:
            self.ecran.blit(self._btn_creatures, (POK_X_VIEWT, POK_Y_VIEWT))
        else:
            self.ecran.blit(self._btn_types, (POK_X_VIEWT, POK_Y_VIEWT))

        i = 0
        if self.render_creatures:
            for elem in self.creas_selected:
                nom = elem.name
                vu, capture, type_ = elem.vu, elem.capture, self.typeur.get_name(elem.type)

                if not vu and not capture:
                    continue

                self.ecran.blit(self.police.render("Nom : {} - Type : {}".format(nom, type_), POL_ANTIALISING, (255, 255, 255)),
                                (POK_X_NAME_CREA, POK_Y_NAME_CREA + POK_ESP_Y_ITEM * i))

                if self.selected_creature == i and (vu or capture):
                    j = 1

                    self.ecran.blit(self.police.render("Description :", POL_ANTIALISING, (255, 255, 255)),
                                    (POK_X_DESC, POK_Y_DESC))

                    if vu or capture:
                        for txt in tw.wrap(elem.description, width=25):
                            self.ecran.blit(self.police.render(txt, POL_ANTIALISING, (255, 255, 255)),
                                            (POK_X_DESC, POK_Y_DESC + j * POK_ESP_Y_ITEM))
                            j += 1
                        self.ecran.blit(self.police.render("Vu : " + ("oui" if vu else "non") +
                                                           ", capturé : " + ("oui" if capture else "non"),
                                                           POL_ANTIALISING, (255, 255, 255)),
                                        (POK_X_DESC, POK_Y_DESC + j * POK_ESP_Y_ITEM))
                        self.ecran.blit(self.images_crea[elem.id], (
                            POK_X_IMG_CREA,
                            POK_Y_IMG_CREA + (j + 1) * POK_ESP_Y_ITEM)
                        )
                    else:
                        self.ecran.blit(self.police.render(DEFAULT_NAME_UNKNOWN, POL_ANTIALISING, (255, 255, 255)),
                                        (POK_X_DESC, POK_Y_DESC + POK_ESP_Y_ITEM))
                i += 1

        else:
            for t_id, type_name in self.typeur.get_types().items():
                if not type_name:
                    continue
                suffixe = "er  " if i == 0 else "ème"
                chaine = str(t_id + 1)
                texte = self.police.render('- ' + ('0' * 1 if i <= 8 else '') + "{}{} -> '{}', vu {} fois"
                                           .format(chaine, suffixe, type_name, self.typeur.get_views_on(t_id)),
                                           POL_ANTIALISING, (255, 255, 255))
                self.ecran.blit(texte, (POK_X_TYPE, POK_Y_TYPE + i * POK_SY_TYPE))
                i += 1

    def clic(self, xp: int, yp: int):
        if POK_X_VIEWT <= xp <= POK_X_VIEWT + POK_SX_VIEWT and POK_Y_VIEWT <= yp <= POK_Y_VIEWT + POK_SY_VIEWT:
            self.render_creatures = not self.render_creatures
        if self.render_creatures:
            if POK_X_NAME_CREA <= xp <= POK_X_NAME_CREA + 200:
                self.selected_creature = (yp - POK_Y_NAME_CREA) // POK_ESP_Y_ITEM
                self.selected_creature = self.selected_creature if 0 <= self.selected_creature < len(self.indexer) else -1
            """if POK_X_SEL_STADE <= xp <= POK_X_SEL_STADE + POK_SX_SEL_STADE and \
                    POK_Y_SEL_STADE <= yp <= POK_Y_SEL_STADE + POK_SY_SEL_STADE:
                self.render_sel_stade()"""
        if not self.render_creatures:
            if POK_X_TYPE <= xp <= POK_X_TYPE + 200:
                self.selected_type = (yp - POK_Y_TYPE) // POK_SY_TYPE
                self.selected_type = self.selected_type if 0 <= self.selected_type < self.typeur.count_types() else -1