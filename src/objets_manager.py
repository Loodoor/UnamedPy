# coding=utf-8

from constantes import *


class ObjectTable:
    instance = None

    def __init__(self):
        if not ObjectTable.instance or ObjectTable.instance != self:
            ObjectTable.instance = self

        self.table = {
            # ID: dict -> {"on": ("creature" | "adversaire" | "personnage")}
            OBJETS_ID.AntiPara: {"on": RENDER_CREATURES, "spec": SPEC_ETAT, "new": SPEC_ETATS.normal},
            OBJETS_ID.AntiBrule: {"on": RENDER_CREATURES, "spec": SPEC_ETAT, "new": SPEC_ETATS.normal},
            OBJETS_ID.AntiPoison: {"on": RENDER_CREATURES, "spec": SPEC_ETAT, "new": SPEC_ETATS.normal},
            OBJETS_ID.Attaqueplus: {"on": RENDER_CREATURES, "spec": SPEC_ATK, "new": +10},
            OBJETS_ID.Defenseplus: {"on": RENDER_CREATURES, "spec": SPEC_DEF, "new": +10},
            OBJETS_ID.Vitesseplus: {"on": RENDER_CREATURES, "spec": SPEC_VIT, "new": +10},
            OBJETS_ID.Elixir: {"on": RENDER_CREATURES, "spec": SPEC_PPS, "new": +5},
            OBJETS_ID.ElixirAugmente: {"on": RENDER_CREATURES, "spec": SPEC_PPS, "new": +10},
            OBJETS_ID.SuperElixir: {"on": RENDER_CREATURES, "spec": SPEC_PPS, "new": +30},
            OBJETS_ID.HyperElixir: {"on": RENDER_CREATURES, "spec": SPEC_PPS, "new": +75},
            OBJETS_ID.ElixirMax: {"on": RENDER_CREATURES, "spec": SPEC_PPS, "new": +999999},
            OBJETS_ID.PotionSimple: {"on": RENDER_CREATURES, "spec": SPEC_PVS, "new": +20},
            OBJETS_ID.SuperPotion: {"on": RENDER_CREATURES, "spec": SPEC_PVS, "new": +60},
            OBJETS_ID.HyperPotion: {"on": RENDER_CREATURES, "spec": SPEC_PVS, "new": +100},
            OBJETS_ID.MegaPotion: {"on": RENDER_CREATURES, "spec": SPEC_PVS, "new": +200},
            OBJETS_ID.PotionMax: {"on": RENDER_CREATURES, "spec": SPEC_PVS, "new": +999999},
            OBJETS_ID.Chaussures: {"on": RENDER_GAME},
            OBJETS_ID.Velo: {"on": RENDER_GAME},
            OBJETS_ID.SimpleBall: {"on": RENDER_COMBAT, "capture": 0.15},
            OBJETS_ID.NormalBall: {"on": RENDER_COMBAT, "capture": 0.35},
            OBJETS_ID.SuperiorBall: {"on": RENDER_COMBAT, "capture": 0.6},
            OBJETS_ID.UltraBall: {"on": RENDER_COMBAT, "capture": 1}
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
        return None


class ObjectMessenger:
    def __init__(self, depuis: dict, pour: dict, objet: Objet):
        # doit etrer de la forme :
        # {"nom": nom, "renderer": renderer}
        # (pour depuis et pour pour)

        self.depuis = depuis
        self.pour = pour
        self.objet = objet