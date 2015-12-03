# coding=utf-8

from constantes import *


class ObjectAction:
    def __init__(self, fonction, *params):
        self.fonc = fonction
        self.params = params

    def execute(self):
        self.fonc(*self.params)


class Objet:
    def __init__(self, nom: str, texte: str, quantite: list, action: ObjectAction):
        self.nom = nom
        self.texte = texte
        self.quantite = quantite
        self.action = action

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
        return Objet(self.nom, self.texte, tmp, self.action)

    def jeter(self):
        if self.quantite[0] > 0:
            self.quantite[0] -= 1
            return Objet(self.nom, self.texte, [1, MAX_ITEM], self.action)
        return GLOBAL_ERROR

    def use(self):
        if self.quantite[0] > 0:
            self.quantite[0] -= 1
            self.action.execute()
            return True
        return False