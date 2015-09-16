class ObjectAction:
    def __init__(self, fonction, *params):
        self.fonc = fonction
        self.params = params

    def execute(self):
        self.fonction(*self.params)


class Objet:
    def __init__(self, nom: str, texte: str, quantite: list, action: ObjectAction):
        self.nom = nom
        self.texte = texte
        self.quantite = quantite
        self.action = action

    def name(self):
        return self.nom

    def aide(self):
        return self.texte

    def use(self):
        if self.quantite[0] > 0:
            self.quantite -= 1
            self.action.execute()
            raise NotImplementedError
            # return True
        return False