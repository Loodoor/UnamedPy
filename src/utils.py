# coding=utf-8

from constantes import *
from indexer import Indexer
from trigger_manager import Trigger, TriggersManager
from zones_attaques_manager import ZonesManager, Zone
import pygame
import objets_manager
import inventaire
from os import path, sep
from glob import glob
import pickle
import time
import os


def unothing(*args, **kwargs):
    return args, kwargs


def uround(nb: int or float):
    if isinstance(nb, int):
        return nb
    return math.floor(nb) if nb >= 0.5 else math.ceil(nb)


def uscreenschot(surface: pygame.Surface):
    path_ = os.path.join("..", "screenshots", str(len(glob(os.path.join("..", "screenshots", "*.png")))) + ".png")
    pygame.image.save(surface, path_)
    print("Screenshot sauvegardée sous '" + path_ + "'")


def uset_image_as_shiney(base: pygame.Surface) -> pygame.Surface:
    base.lock()
    for pixel in range(base.get_width() * base.get_height()):
        x, y = pixel % base.get_height(), pixel // base.get_height()
        last_color = base.get_at((x, y))
        new_color = pygame.Color(last_color.g, last_color.b, last_color.r, last_color.a)
        base.set_at((x, y), new_color)
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
    if not mapping or (mapping and os.path.join("..", "saves", "map" + EXTENSION) in mapping and len(mapping) == 1):
        return False
    return True


def udel_same_occurence(*args) -> list:
    work = []
    last = ""
    for i in range(len(args)):
        if args[i] == last:
            pass
        else:
            last = args[i]
            work.append(last)
    return work


def uremove(*files):
    for file in files:
        if path.exists(file):
            os.remove(file)


def upg_bar(screen, rect_bg: tuple, progress: int=0, bg_color: tuple=(128, 128, 128), fg_color: tuple=(50, 180, 50)):
    pygame.draw.rect(screen, bg_color, rect_bg)
    pygame.draw.rect(screen, fg_color, (rect_bg[0] + BAR_ESP, rect_bg[1] + BAR_ESP, progress, rect_bg[3] - BAR_ESP * 2))


class UMoment:
    def __init__(self, description_job: str=""):
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
            print("J'ai fini mon travail")
        else:
            print("Le fichier indiquant une manipulation existe déjà.\nRemarque(s) :")
            with open(self.path, 'rb') as rlast_job_done:
                print(pickle.Unpickler(rlast_job_done).load())
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

        Indexer.add_new("", 0, T_FEU, 0, self.pack_creatures + "feu-01.png",
                        "Cette créature vit en groupe au coeur d'un volcan dont elle n'émerge que très rarement.")

        Indexer.add_new("", 1, T_LUMIERE, 0, self.pack_creatures + "lumiere-01-a1.png",
                        "Cette créature très timide se redresse lorsqu'elle se sent menacée, et émet un vif rayon de "
                        "lumière avec ses plaques ventrales pour faire fuir l'ennemi.")
        Indexer.add_new("", 2, T_LUMIERE, 1, self.pack_creatures + "lumiere-01-a2.png",
                        "Cette créature s'est entourée de fourrure isolante pour préparer la métamorphose de son corps. "
                        "Pour se protéger, elle peut émettre de la lumière à travers son cocon et utiliser ses pattes "
                        "qui n'ont pas encore fini d'évoluer.")
        Indexer.add_new("", 3, T_LUMIERE, 2, self.pack_creatures + "lumiere-01-a3.png",
                        "La lumière intense émise par cette créature et les motifs sur ses ailes créent des jeux "
                        "d'ombres monstrueux qui effraient ses prédateurs.")

        Indexer.add_new("", 4, T_TENEBRE, 0, self.pack_creatures + "tenebre-01-a1.png",
                        "Cette créature suit ses proies en glissant silencieusement au sol et sur les murs. "
                        "Quand elle est suffisamment près, elle les avale tout rond.")
        Indexer.add_new("", 5, T_TENEBRE, 1, self.pack_creatures + "tenebre-01-a2.png",
                        "Cette créature avale ses proies en les recouvrant de son corps gluant.")
        Indexer.add_new("", 6, T_TENEBRE, 2, self.pack_creatures + "tenebre-01-a3.png",
                        "Cette créature jaillit de l'ombre pour saisir ses proies jusqu'à plusieurs mètres de distance.")

        # Création des triggers
        # toujours définir un ID (str)

        TriggersManager.add_trigger_to_path(Trigger("trigger.test", 0, 0, TRIGGER_INFINITE_CALLS, print, "hello world !", "je suis un test de trigger !"))

        # Création des objets par défaut

        anti_para = objets_manager.Objet("Anti-Para", "L'anti-Para permet d'enlever le statut 'paralysé' d'une de vos créatures",
                                         [0, MAX_ITEM], objets_manager.ObjectAction(print, "test anti para"))
        anti_brul = objets_manager.Objet("Anti-Brûle", "L'anti-Brûle permet d'enlever le statut 'brûlé' d'une de vos créatures",
                                         [0, MAX_ITEM], objets_manager.ObjectAction(print, "test anti brule"))
        anti_poison = objets_manager.Objet("Anti-Poison", "L'anti-Poison permet d'enlever le statut 'empoisonné' d'une de vos créatures",
                                           [0, MAX_ITEM], objets_manager.ObjectAction(print, "test anti poison"))
        att_p = objets_manager.Objet("Attaque+", "L'attaque+ augmente l'attaque d'une de vos créatures (effet à long terme)",
                                     [0, MAX_ITEM], objets_manager.ObjectAction(print, "test attaque+"))
        def_p = objets_manager.Objet("Défense+", "Le défense+ augmente la défense d'une de vos créatures (effet à long terme)",
                                     [0, MAX_ITEM], objets_manager.ObjectAction(print, "test defense+"))
        vit_p = objets_manager.Objet("Vitesse+", "Le vitesse+ augmente la vitesse d'une de vos créatures (effet à long terme)",
                                     [0, MAX_ITEM], objets_manager.ObjectAction(print, "test vitesse+"))
        pps_p = objets_manager.Objet("PP+", "Le PP+ augmente le nombre de PP max d'une attaque d'une de vos créatures (effet à long terme)",
                                     [0, MAX_ITEM], objets_manager.ObjectAction(print, "test pps+"))
        regen_pps_5 = objets_manager.Objet("Elixir", "L'élixir redonne 5 PP à une attaque d'une de vos créatures",
                                           [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 5"))
        regen_pps_10 = objets_manager.Objet("Elixir Augmenté", "L'élixir augmenté redonne 10 PP à une attaque d'une de vos créatures",
                                            [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 10"))
        regen_pps_30 = objets_manager.Objet("Super Elixir", "Le super élixir redonne 30 PP à une attaque d'une de vos créatures",
                                            [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 30"))
        regen_pps_75 = objets_manager.Objet("Hyper Elixir", "L'hyper élixir redonne 75 PP à une attaque d'une de vos créatures",
                                            [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps 75"))
        regen_pps_max = objets_manager.Objet("Elixir Max", "L'élixir max régénère entièrement les PP d'une attaque d'une de vos créatures",
                                             [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pps max"))
        pvs_p = objets_manager.Objet("PV+", "Le PV+ augmente le nombre de PV d'une de vos créatures (effet à long terme)",
                                     [0, MAX_ITEM], objets_manager.ObjectAction(print, "test pvs"))
        regen_pvs_20 = objets_manager.Objet("Potion Simple", "La potion régénère 20 PV à une de vos créatures",
                                            [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 20"))
        regen_pvs_60 = objets_manager.Objet("Super Potion", "La super potion régénère 60 PV à une de vos créatures",
                                            [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 60"))
        regen_pvs_100 = objets_manager.Objet("Hyper Potion", "L'hyper potion régénère 100 PV à une de vos créatures",
                                             [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 100"))
        regen_pvs_200 = objets_manager.Objet("Méga Potion", "La méga potion régénère 200 PV à une de vos créatures",
                                             [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs 200"))
        regen_pvs_max = objets_manager.Objet("Potion Max", "La potion max régénère entièrement les PV d'une de vos créatures",
                                             [0, MAX_ITEM], objets_manager.ObjectAction(print, "test regen pvs max"))
        chaussures = objets_manager.Objet("Chaussures", "Les chaussures vous permettent de vous déplacer plus vite",
                                          [1, 1], objets_manager.ObjectAction(print, "test chaussures"))
        velo = objets_manager.Objet("Velo", "Le vélo vous permet de vous déplacer encore vite qu'avec les Chaussures",
                                    [0, 1], objets_manager.ObjectAction(print, "test velo"))
        simple_ball = objets_manager.Objet("Simple Ball", "La simple ball vous permet de capturer une créature. Son taux"
                                                          " de réussite est très faible", [0, MAX_ITEM],
                                           objets_manager.ObjectAction(print, "test simple ball"))
        normal_ball = objets_manager.Objet("Normal Ball",
                                           "La normal ball vous permet de capturer une créature. Son taux"
                                           " de réussite est faible, quoique supérieur à celui de la simple ball",
                                           [0, MAX_ITEM], objets_manager.ObjectAction(print, "test normal ball"))
        sup_ball = objets_manager.Objet("Superior Ball", "La superior ball vous permet de capturer une créature. Son"
                                                         "taux de réussite est assez élevé.", [0, MAX_ITEM],
                                           objets_manager.ObjectAction(print, "test superior ball"))
        ultra_ball = objets_manager.Objet("Ultra Ball", "L'ultra ball a un taux de réussite proche des 100%, mais est "
                                                        "très complexe à fabriquer", [0, MAX_ITEM],
                                          objets_manager.ObjectAction(print, "test ultra ball"))

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
                pps_p,
                regen_pps_5,
                regen_pps_10,
                regen_pps_30,
                regen_pps_75,
                regen_pps_max,
                pvs_p,
                regen_pvs_20,
                regen_pvs_60,
                regen_pvs_100,
                regen_pvs_200,
                regen_pvs_max
            ],  # Poche médicaments
            [
                velo,
                chaussures
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
            pickle.Pickler(fjob_done).dump(UMoment("Ajout des premières créatures, "
                                                   "d'un trigger de test en (0, 0), "
                                                   "de nouveaux objets, "
                                                   "refonte des zones id, "
                                                   "et des zones de base"))

    def reload(self):
        self.load()