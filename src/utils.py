from constantes import *
from indexer import Indexer
from trigger_manager import Trigger, TriggersManager
import objets_manager
import inventaire
from os import path, sep
import pickle
import time
import os


def unothing(*args, **kwargs):
    return args, kwargs


def uremove(*files):
    for file in files:
        if path.exists(file):
            os.remove(file)


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
        # création des créatures
        # doit être fait AVANT de faire quoi que ce soit !
        uremove(
            path.join("..", "saves", "indexer" + EXTENSION),
            path.join("..", "saves", "triggers" + EXTENSION),
            path.join("..", "saves", "inventaire" + EXTENSION)
        )

        # le nom est toujours vide, c'est le joueur qui les choisira à chaque fois
        # l'id doit etre unique
        # la description peut être vide, mais c'est mieux de la remplir

        Indexer.add_new("", 0, T_FEU, self.pack_creatures + "feu-01.png",
                        "Cette créature vit en groupe au coeur d'un volcan dont il n'émerge que très rarement.")

        Indexer.add_new("", 1, T_LUMIERE, self.pack_creatures + "lumiere-01-a1.png",
                        "Cette créature très timide se redresse lorsqu'elle se sent menacé, et émet un vif rayon de "
                        "lumière avec ses plaques ventrales pour faire fuir l'ennemi.")
        Indexer.add_new("", 2, T_LUMIERE, self.pack_creatures + "lumiere-01-a2.png",
                        "Cette créature s'est entourée de fourrure isolante pour préparer la métamorphose de son corps. "
                        "Pour se protéger, elle peut émettre de la lumière à travers son cocon et utiliser ses pattes "
                        "qui n'ont pas encore fini d'évoluer.")
        Indexer.add_new("", 3, T_LUMIERE, self.pack_creatures + "lumiere-01-a3.png",
                        "La lumière intense émise par cette créature et les motifs sur ses ailes créent des jeux "
                        "d'ombres monstrueux qui effraient ses prédateurs.")

        Indexer.add_new("", 4, T_TENEBRE, self.pack_creatures + "tenebre-01-a1.png",
                        "Cette créature suit ses proies en glissant silencieusement au sol et sur les murs. "
                        "Quand elle est suffisamment près, elle les avale tout rond.")
        Indexer.add_new("", 5, T_TENEBRE, self.pack_creatures + "tenebre-01-a2.png",
                        "Cette créature avale ses proies en les recouvrant de son corps gluant.")
        Indexer.add_new("", 6, T_TENEBRE, self.pack_creatures + "tenebre-01-a3.png",
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

        objets = [
            [

            ],  # Poche communs
            [

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

        # Fin du boulot !
        with open(self.path, 'wb') as fjob_done:
            pickle.Pickler(fjob_done).dump(UMoment("Ajout des premières créatures, "
                                                   "d'un trigger de test en (0, 0), "
                                                   "et des descriptions des objets"))

    def reload(self):
        self.load()