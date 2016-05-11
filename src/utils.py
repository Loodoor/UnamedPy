# coding=utf-8

from constantes import *
from indexer import Indexer
from trigger_manager import Trigger, TriggersManager
from zones_attaques_manager import ZonesManager, Zone
import objets_manager
import inventaire
from os import path, sep
from glob import glob
import random
import pickle
import time
import threading
import debug


def unothing(*args, **kwargs):
    return args, kwargs


def ureplace_bool_str(state: bool, by: list):
    if state:
        return by[0]
    return by[1]


def usep_lst_in_smallers(main: list, size: int) -> list:
    work = []
    new_line = []

    for i in range(len(main)):
        if (not i % size or i == len(main) - 1) and new_line:
            work.append(new_line)
            new_line = []
        new_line.append(main[i])

    return work


def udir_to_vect(direction: int) -> tuple:
    if direction == HAUT:
        return 0, -1
    if direction == BAS:
        return 0, 1
    if direction == GAUCHE:
        return -1, 0
    if direction == DROITE:
        return 1, 0


def unegate_vect(vect: tuple) -> tuple:
    return -vect[0], -vect[1]


def ugen_key(seed: float=1234.5) -> float:
    key = 1.0
    fseed = random.random()
    key = (key * fseed) / (seed / 10 ** len(str(seed).split('.')[0])) + seed / 25 ** len(str(seed).split('.')[1]) * ((int(key) << 0x1f) ^ int(key)) + (fseed / seed)
    return key


def uround(nb: int or float, lim: float=0.5):
    if isinstance(nb, int):
        return nb
    return math.floor(nb) if nb <= lim else math.ceil(nb)


def uscreenschot(surface):
    path_ = os.path.join("..", "screenshots", str(len(glob(os.path.join("..", "screenshots", "*.png")))) + ".png")
    ree.save_image(surface, path_)
    debug.println("[UTILS] Screenshot sauvegardée sous '" + path_ + "'")


def uset_image_as_shiney(base) -> object:
    base.lock()
    for pixel in range(base.get_width() * base.get_height()):
        x, y = pixel % base.get_height(), pixel // base.get_height()
        last_color = base.get_at((x, y))
        base.set_at((x, y), (last_color.g, last_color.b, last_color.r, last_color.a))
    base.unlock()
    return base


def ucount_in_list(*args):
    work = {}

    for elem in args:
        if elem not in work.keys():
            work[elem] = 1
        else:
            work[elem] += 1

    return work


def uhas_already_played() -> bool:
    mapping = glob(os.path.join("..", "saves", "*" + EXTENSION))
    if not mapping:
        return False
    return True


def udel_same_occurence(*args) -> list:
    work = []
    last = ""
    for elem in args:
        if elem != last:
            last = elem
            work.append(last)
    return work


def uremove(*files):
    for file in files:
        if path.exists(file):
            os.remove(file)


def deprecated(fonction):
    deprecated.already_affiche = []

    def wrapper(*args):
        if fonction.__name__ not in deprecated.already_affiche:
            print(fonction.__name__, "est déprécié")
        deprecated.already_affiche.append(fonction.__name__)
        fonction(*args)
    return wrapper


def upg_bar(screen, rect_bg: tuple, progress: int=0, bg_color: tuple=(128, 128, 128), fg_color: tuple=(50, 180, 50), esp=BAR_ESP, bg: bool=True, max_progress: int=-1):
    if max_progress != -1:
        progress /= max_progress
        progress *= rect_bg[2] - 2 * esp
    if bg:
        ree.draw_rect(screen, rect_bg, bg_color)
    ree.draw_rect(screen, (rect_bg[0] + esp, rect_bg[1] + esp, progress, rect_bg[3] - esp * 2), fg_color)


class UThreadFunction(threading.Thread):
    def __init__(self, func: callable, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


class Point:
    def __init__(self, *args, **kwargs):
        try:
            self.x = args[0][0] if isinstance(args[0], tuple) else args[0]
        except IndexError:
            self.x = kwargs.get('x') if kwargs.get('x') else 0

        try:
            self.y = args[0][1] if isinstance(args[1], tuple) else args[1]
        except IndexError:
            self.y = kwargs.get('y') if kwargs.get('y') else 0

    def move(self, x: int=0, y: int=0):
        self.x += x
        self.y += y

    def move_tile(self, i: int=0, j: int=0):
        self.move(i * TILE_SIZE, j * TILE_SIZE)

    @property
    def tile(self) -> object:
        return Point(self.x // TILE_SIZE, self.y // TILE_SIZE)

    @tile.setter
    def tile(self, pos: tuple):
        self.x = pos[0] * TILE_SIZE
        self.y = pos[1] * TILE_SIZE

    @property
    def pos(self) -> tuple:
        return self.x, self.y

    @pos.setter
    def pos(self, new: tuple):
        self.x, self.y = new


class UMoment:
    def __init__(self, description_job: str="-"):
        self.time = time.time()
        self.desc = description_job

    def __str__(self):
        return str(self.time) + " - " + self.desc


class ULoader:
    def __init__(self):
        self.path = path.join("..", "saves", "utils" + EXTENSION)
        self.pack_creatures = path.join("..", "assets", "creatures") + sep

    def load(self):
        if not path.exists(self.path):
            self.create()
            debug.println("[ULoader] Chargement terminé")
        else:
            debug.println("[ULoader] Note :", sep='', end=' ')
            with open(self.path, 'rb') as rlast_job_done:
                debug.println(pickle.Unpickler(rlast_job_done).load())
            self.create()

    def create(self):
        # doit être fait AVANT de faire quoi que ce soit !
        uremove(
            path.join("..", "saves", "indexer" + EXTENSION),
            path.join("..", "saves", "triggers" + EXTENSION),
            path.join("..", "saves", "inventaire" + EXTENSION),
            path.join("..", "saves", "zones" + EXTENSION)
        )

        # création des créatures

        # le nom est toujours vide, c'est le joueur qui les choisira à chaque fois
        # l'id doit etre unique
        # la description peut être vide, mais c'est mieux de la remplir

        with open(path.join("..", "assets", "configuration", "creatures" + EXTENSION), "r", encoding="utf-8") as file:
            for line in file.readlines():
                if line[0] != "#":
                    work = line.split('::')
                    type_ = T_NORMAL  # defaut
                    if work[1] == "FEU":
                        type_ = T_FEU
                    if work[1] == "EAU":
                        type_ = T_EAU
                    if work[1] == "PLANTE":
                        type_ = T_PLANTE
                    if work[1] == "ELEC":
                        type_ = T_ELEC
                    if work[1] == "AIR":
                        type_ = T_AIR
                    if work[1] == "NORMAL":
                        type_ = T_NORMAL
                    if work[1] == "TERRE":
                        type_ = T_TERRE
                    if work[1] == "POISON":
                        type_ = T_POISON
                    if work[1] == "LUMIERE":
                        type_ = T_LUMIERE
                    if work[1] == "TENEBRE":
                        type_ = T_TENEBRE
                    Indexer.add_new("", int(work[0]), type_, int(work[2]), self.pack_creatures + work[3] + ".png", work[4], int(work[5]), int(work[6]))

        # Création des triggers
        # toujours définir un ID (str)

        TriggersManager.add_trigger_to_path(Trigger("trigger.test", 0, 10, TRIGGER_INFINITE_CALLS, print, "hello world !", "je suis un test de trigger !"))

        # Création des objets par défaut
        anti_para = objets_manager.Objet("Anti-Para", "L'anti-Para permet d'enlever le statut 'paralysé' d'une de vos créatures",
                                         [0, MAX_ITEM], OBJETS_ID.AntiPara)
        anti_brul = objets_manager.Objet("Anti-Brûle", "L'anti-Brûle permet d'enlever le statut 'brûlé' d'une de vos créatures",
                                         [0, MAX_ITEM], OBJETS_ID.AntiBrule)
        anti_poison = objets_manager.Objet("Anti-Poison", "L'anti-Poison permet d'enlever le statut 'empoisonné' d'une de vos créatures",
                                           [0, MAX_ITEM], OBJETS_ID.AntiPoison)
        att_p = objets_manager.Objet("Attaque+", "L'attaque+ augmente l'attaque d'une de vos créatures (effet à long terme)",
                                     [0, MAX_ITEM], OBJETS_ID.Attaqueplus)
        def_p = objets_manager.Objet("Défense+", "Le défense+ augmente la défense d'une de vos créatures (effet à long terme)",
                                     [0, MAX_ITEM], OBJETS_ID.Defenseplus)
        vit_p = objets_manager.Objet("Vitesse+", "Le vitesse+ augmente la vitesse d'une de vos créatures (effet à long terme)",
                                     [0, MAX_ITEM], OBJETS_ID.Vitesseplus)
        regen_pps_5 = objets_manager.Objet("Elixir", "L'élixir redonne 5 PP à une attaque d'une de vos créatures",
                                           [0, MAX_ITEM], OBJETS_ID.Elixir)
        regen_pps_10 = objets_manager.Objet("Elixir Augmenté", "L'élixir augmenté redonne 10 PP à une attaque d'une de vos créatures",
                                            [0, MAX_ITEM], OBJETS_ID.ElixirAugmente)
        regen_pps_30 = objets_manager.Objet("Super Elixir", "Le super élixir redonne 30 PP à une attaque d'une de vos créatures",
                                            [0, MAX_ITEM], OBJETS_ID.SuperElixir)
        regen_pps_75 = objets_manager.Objet("Hyper Elixir", "L'hyper élixir redonne 75 PP à une attaque d'une de vos créatures",
                                            [0, MAX_ITEM], OBJETS_ID.HyperElixir)
        regen_pps_max = objets_manager.Objet("Elixir Max", "L'élixir max régénère entièrement les PP d'une attaque d'une de vos créatures",
                                             [0, MAX_ITEM], OBJETS_ID.ElixirMax)
        regen_pvs_20 = objets_manager.Objet("Potion Simple", "La potion régénère 20 PV à une de vos créatures",
                                            [0, MAX_ITEM], OBJETS_ID.PotionSimple)
        regen_pvs_60 = objets_manager.Objet("Super Potion", "La super potion régénère 60 PV à une de vos créatures",
                                            [0, MAX_ITEM], OBJETS_ID.SuperPotion)
        regen_pvs_100 = objets_manager.Objet("Hyper Potion", "L'hyper potion régénère 100 PV à une de vos créatures",
                                             [0, MAX_ITEM], OBJETS_ID.HyperPotion)
        regen_pvs_200 = objets_manager.Objet("Méga Potion", "La méga potion régénère 200 PV à une de vos créatures",
                                             [0, MAX_ITEM], OBJETS_ID.MegaPotion)
        regen_pvs_max = objets_manager.Objet("Potion Max", "La potion max régénère entièrement les PV d'une de vos créatures",
                                             [0, MAX_ITEM], OBJETS_ID.PotionMax)
        simple_ball = objets_manager.Objet("Simple Ball", "La simple ball vous permet de capturer une créature. Son taux"
                                                          " de réussite est très faible", [1, MAX_ITEM],
                                           OBJETS_ID.SimpleBall)
        normal_ball = objets_manager.Objet("Normal Ball",
                                           "La normal ball vous permet de capturer une créature. Son taux"
                                           " de réussite est faible, quoique supérieur à celui de la simple ball",
                                           [1, MAX_ITEM], OBJETS_ID.NormalBall)
        sup_ball = objets_manager.Objet("Superior Ball", "La superior ball vous permet de capturer une créature. Son"
                                                         "taux de réussite est assez élevé.", [1, MAX_ITEM],
                                        OBJETS_ID.SuperiorBall)
        ultra_ball = objets_manager.Objet("Ultra Ball", "L'ultra ball a un taux de réussite proche des 100%, mais est "
                                                        "très complexe à fabriquer", [1, MAX_ITEM],
                                          OBJETS_ID.UltraBall)

        objets = [
            [

            ],  # Poche communs
            [
                simple_ball,
                normal_ball,
                sup_ball,
                ultra_ball
            ],  # Poche capturateurs
            [
                anti_para,
                anti_brul,
                anti_poison,
                att_p,
                def_p,
                vit_p,
                regen_pps_5,
                regen_pps_10,
                regen_pps_30,
                regen_pps_75,
                regen_pps_max,
                regen_pvs_20,
                regen_pvs_60,
                regen_pvs_100,
                regen_pvs_200,
                regen_pvs_max
            ],  # Poche médicaments
            [

            ],  # Poche Objets Rares
            [

            ]  # Poche CT/CS
        ]

        inventaire.Inventaire.create_inventory_and_store(objets)

        # Création des zones par défaut

        ZonesManager.add_new_zone_to_path(Zone(ZONE0,
                                               [_.id for _ in Indexer.static_select_all_crea_with_stade(0)[:4]],
                                               (0, 4)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE1,
                                               [_.id for _ in Indexer.static_select_all_crea_with_stade(0)[:8]],
                                               (4, 10)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE2,
                                               [_.id for _ in Indexer.static_select_all_crea_with_stade(0)[:8] +
                                                   Indexer.static_select_all_crea_with_stade(1)[:4]
                                               ],
                                               (8, 22)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE3,
                                               [_.id for _ in Indexer.static_select_all_crea_with_stade(0)[:11] +
                                                   Indexer.static_select_all_crea_with_stade(1)[:6]
                                               ],
                                               (17, 35)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE4,
                                               [_.id for _ in Indexer.static_select_all_crea_with_stade(1)[:14]],
                                               (30, 45)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE5,
                                               [_.id for _ in Indexer.static_select_all_crea_with_stade(1)[:14] +
                                                   Indexer.static_select_all_crea_with_stade(2)[:10] +
                                                   Indexer.static_select_all_crea_with_stade(3)[:5]
                                               ],
                                               (40, 60)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE6,
                                               [_.id for _ in Indexer.static_select_all_crea_with_stade(2)[:] +
                                                   Indexer.static_select_all_crea_with_stade(3)[:9]
                                               ],
                                               (55, 75)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE7,
                                               [_.id for _ in Indexer.static_select_all_crea_with_stade(2)[:] +
                                                   Indexer.static_select_all_crea_with_stade(3)[:14]
                                               ],
                                               (70, 100)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE8,
                                               [_ for _ in range(MAX_CREATURES)],
                                               (90, 120)))
        ZonesManager.add_new_zone_to_path(Zone(ZONE9,
                                               [_ for _ in range(MAX_CREATURES)],
                                               (110, 150)))
        ZonesManager.add_new_zone_to_path(Zone(ZONEa,
                                               [_ for _ in range(MAX_CREATURES)],
                                               (140, 200)))
        ZonesManager.add_new_zone_to_path(Zone(ZONEb,
                                               [_ for _ in range(MAX_CREATURES)],
                                               (180, 240)))
        ZonesManager.add_new_zone_to_path(Zone(ZONEc,
                                               [_ for _ in range(MAX_CREATURES)],
                                               (220, 285)))
        ZonesManager.add_new_zone_to_path(Zone(ZONEd,
                                               [_ for _ in range(MAX_CREATURES)],
                                               (265, 310)))
        ZonesManager.add_new_zone_to_path(Zone(ZONEe,
                                               [_ for _ in range(MAX_CREATURES)],
                                               (290, 360)))
        ZonesManager.add_new_zone_to_path(Zone(ZONEf,
                                               [_ for _ in range(MAX_CREATURES)],
                                               (330, 420)))

        # Fin du boulot !
        with open(self.path, 'wb') as fjob_done:
            pickle.Pickler(fjob_done).dump(UMoment())

    def reload(self):
        self.load()