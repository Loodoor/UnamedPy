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
        return str(self.quantite[0]) + " / " + str(self.quantite[1])

    def aide(self):
        return self.texte

    def jeter_tout(self):
        self.quantite[0] = 0

    def jeter(self):
        self.quantite[0] -= 1

    def use(self):
        if self.quantite[0] > 0:
            self.quantite[0] -= 1
            self.action.execute()
            return True
        return False