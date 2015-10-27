from constantes import *
from indexer import Indexer
from os import path, sep
import pickle
import time


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

    def create(self):
        # création des créatures
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

        with open(self.path, 'wb') as fjob_done:
            pickle.Pickler(fjob_done).dump(UMoment("Ajout des premières créatures"))

    def reload(self):
        self.load()