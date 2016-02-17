# coding=utf-8

from constantes import *


class ObjectTable:
    instance = None

    def __init__(self):
        if not ObjectTable.instance or ObjectTable.instance != self:
            ObjectTable.instance = self

        self.table = {
            # ID: dict -> {"on": ("inventaire" | "creature" | "adversaire" | "personnage")}
            "AntiPara": {"on": "creature"},
            "AntiBrule": {"on": "creature"},
            "AntiPoison": {"on": "creature"},
            "Attaqueplus": {"on": "creature"},
            "Defenseplus": {"on": "creature"},
            "Vitesseplus": {"on": "creature"},
            "PPplus": {"on": "creature"},
            "Elixir": {"on": "creature"},
            "ElixirAugmente": {"on": "creature"},
            "SuperElixir": {"on": "creature"},
            "HyperElixir": {"on": "creature"},
            "ElixirMax": {"on": "creature"},
            "PVplus": {"on": "creature"},
            "PotionSimple": {"on": "creature"},
            "SuperPotion": {"on": "creature"},
            "HyperPotion": {"on": "creature"},
            "MegaPotion": {"on": "creature"},
            "PotionMax": {"on": "creature"},
            "Chaussures": {"on": "personnage"},
            "Velo": {"on": "personnage"},
            "SimpleBall": {"on": "adversaire"},
            "NormalBall": {"on": "adversaire"},
            "SuperiorBall": {"on": "adversaire"},
            "UltraBall": {"on": "adversaire"}
        }

    @staticmethod
    def add_object(object_id: str, action_on: dict):
        ObjectTable.instance.table.update({object_id: action_on})

    @staticmethod
    def get_object_action(object_id: str):
        if object_id in ObjectTable.instance.table.keys():
            return ObjectTable.instance.table[object_id]
        raise ValueError("La clé '{}' n'existe pas pour 'ObjectTable.instance.table'".format(object_id))


class Objet:
    def __init__(self, nom: str, texte: str, quantite: list, action_id: str):
        self.nom = nom
        self.texte = texte
        self.quantite = quantite
        self.action_id = action_id

    def name(self):
        return self.nom

    def nombre(self):
        return self.quantite[0]

    def tot_quantite(self):
        return str(self.quantite[0])

    def aide(self):
        return self.texte

    def jeter_tout(self):
        tmp, self.quantite[0] = self.quantite, 0
        return Objet(self.nom, self.texte, tmp, self.action_id)

    def jeter(self):
        if self.quantite[0] > 0:
            self.quantite[0] -= 1
            return Objet(self.nom, self.texte, [1, MAX_ITEM], self.action_id)
        return GLOBAL_ERROR

    def use(self) -> bool:
        if self.quantite[0] > 0:
            self.quantite[0] -= 1
            return ObjectTable.get_object_action(self.action_id)
        return False


class ObjectMessenger:
    def __init__(self, depuis: dict, pour: dict, objet: Objet):
        # doit etrer de la forme :
        # {"nom": nom, "renderer": renderer}
        # (pour depuis et pour pour)

        self.depuis = depuis
        self.pour = pour
        self.objet = objet